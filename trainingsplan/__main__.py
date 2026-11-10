"""CLI: python -m trainingsplan <befehl>

  analyse  – Trainings-/Gesundheitsdaten aus intervals.icu auswerten
  sync     – Plan aus Datei (angepasst) nach intervals.icu übertragen
  anpassen – bereits in intervals.icu geplante Einheiten anpassen
  stufentest – Rad-/Lauf-Stufentest einplanen (--rad DATUM, --lauf DATUM);
             ein vorhandener Test am selben Tag (z.B. FTP-Test) wird ersetzt
  (sync/anpassen ohne --apply: nur Vorschau, nichts wird geschrieben)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from .analyse import Bewertung, bewerte
from .anpassen import passe_an
from .intervals_icu import IntervalsClient, IntervalsError
from .plan import Einheit, einheit_aus_event, lade_plan
from .stufentest import lauf_stufentest, rad_stufentest

AMPEL = {"gruen": "🟢 GRÜN – Plan wie geplant",
         "gelb": "🟡 GELB – Umfang/Intensität reduziert",
         "rot": "🔴 ROT – Erholung priorisiert"}


def _daten(client: IntervalsClient, heute: date,
           basis_ab: date | None = None) -> tuple[list[dict], list[dict]]:
    von = min(heute - timedelta(days=60), basis_ab or heute)
    return client.wellness(von, heute), client.activities(von, heute)


def bericht(b: Bewertung, vorher: list[Einheit], nachher: list[Einheit], heute: date) -> str:
    z = [f"# Trainingsauswertung {heute.isoformat()}", "", f"**Status:** {AMPEL[b.status]}"
         + (" (gut erholt)" if b.frisch else ""), "", "## Kennzahlen", ""]
    namen = {"ctl": "Fitness (CTL)", "atl": "Ermüdung (ATL)", "tsb": "Form (TSB)",
             "form_pct": "Form %", "ramp_rate": "Ramp Rate", "hrv_7d": "HRV 7 Tage",
             "hrv_basis": "HRV Basis", "hrv_z": "HRV z-Wert", "ruhepuls_7d": "Ruhepuls 7 Tage",
             "ruhepuls_basis": "Ruhepuls Basis", "schlaf_h_7d": "Schlaf Ø h (7 T.)",
             "load_7d": "Load letzte 7 Tage", "load_wochenschnitt_4w": "Load Ø/Woche (4 W.)",
             "acwr": "Akut:Chronisch", "load_normalwoche": "Load Ø Normalwoche",
             "normalwochen": "Normalwochen im Vergleich", "pausewochen": "Pausenwochen (ignoriert)", "fatigue_3d": "Müdigkeit (3 T.)",
             "soreness_3d": "Muskelkater (3 T.)", "stress_3d": "Stress (3 T.)"}
    z += ["| Kennzahl | Wert |", "|---|---|"]
    z += [f"| {namen.get(k, k)} | {v} |" for k, v in b.kennzahlen.items() if k != "hinweis"]
    if "hinweis" in b.kennzahlen:
        z += ["", f"_{b.kennzahlen['hinweis']}_"]
    z += ["", "## Auffälligkeiten", ""]
    z += [f"- {s.text}" for s in b.signale] or ["- keine"]
    geaendert = [e for e in nachher if e.angepasst]
    z += ["", "## Planänderungen", ""]
    if not geaendert:
        z.append("- keine")
    for e in geaendert:
        o = next((x for x in vorher if x.external_id == e.external_id and x.datum == e.datum), e)
        z.append(f"- **{e.datum:%a %d.%m.}** {o.name}: {o.dauer_min:.0f} min"
                 f"{f' / {o.load:.0f} TSS' if o.load else ''} → {e.name}: {e.dauer_min:.0f} min"
                 f"{f' / {e.load:.0f} TSS' if e.load else ''} ({'; '.join(e.angepasst)})")
    z += ["", "_Hinweis: Faustregeln auf Basis deiner intervals.icu-Daten, kein ärztlicher Rat._", ""]
    return "\n".join(z)


def _stufentest(client: IntervalsClient, a) -> int:
    tests = []
    if a.rad:
        tests.append(rad_stufentest(a.rad))
    if a.lauf:
        tests.append(lauf_stufentest(a.lauf))
    if not tests:
        print("Fehler: --rad und/oder --lauf mit Datum angeben", file=sys.stderr)
        return 2
    for t in tests:
        vorhanden = [einheit_aus_event(e) for e in client.events(t.datum, t.datum)
                     if e.get("category") == "WORKOUT"]
        sport = {"Ride": ("Ride", "VirtualRide"), "Run": ("Run", "VirtualRun")}[t.typ]
        alt = next((e for e in vorhanden if e.typ in sport and e.intensitaet == "test"), None)
        ev = t.to_event()
        aktion = f"ersetzt '{alt.name}'" if alt else "neu angelegt"
        print(f"--- {t.datum:%a %d.%m.} {t.name} ({t.dauer_min:.0f} min) – {aktion}\n{t.beschreibung}\n")
        if not a.apply:
            continue
        if alt:
            client.update_event(alt.event_id, {k: ev[k] for k in
                                ("name", "description", "moving_time", "icu_training_load")})
        else:
            client.upsert_events([ev])
    print("✔ übernommen." if a.apply else "Vorschau – mit --apply übernehmen.")
    return 0


def _woche(client: IntervalsClient, a) -> int:
    """Testwochen 09.-22.11.2026 (24-h-Schwimmen am Fr/Sa): Einheiten verschieben/entfernen und die
    Einheiten der Woche eintragen (idempotent über external_id und Namen)."""
    from . import wochenplan
    evs = client.events(date(2026, 11, 9), date(2026, 11, 30))
    finde = lambda tag, name: [e for e in evs if e["start_date_local"][:10] == tag and e.get("name") == name]
    weg = [(e, grund) for tag, name, grund in wochenplan.ENTFERNEN for e in finde(tag, name)]
    versch = [(e, neu, felder) for alt, name, neu, felder in wochenplan.VERSCHIEBEN for e in finde(alt, name)
              if alt != neu or felder]
    neu = wochenplan.DIESE_WOCHE + wochenplan.naechste_woche_events()
    for e, grund in weg:
        print(f"Entfernen:  {e['start_date_local'][:10]} {e['name']} – {grund}")
    for e, nd, felder in versch:
        print(f"Verschieben: {e['start_date_local'][:10]} -> {nd} {felder.get('name', e['name'])}")
    for e in neu:
        print(f"Eintragen:  {e['start_date_local'][:10]} {e['name']} ({e.get('type', e['category'])})")
    if not a.apply:
        print("Vorschau – mit --apply in intervals.icu schreiben.")
        return 0
    for e, _ in weg:
        client.delete_event(e["id"])
    for e, nd, felder in versch:
        client.update_event(e["id"], {"start_date_local": f"{nd}T00:00:00", **felder})
    client.upsert_events(neu)
    print("✔ Wochen angepasst.")
    return 0


def _saison(client: IntervalsClient, a) -> int:
    """Saisonplan (Wochenziele, Phasen-Notizen) in den Kalender schreiben; der Hauptwettkampf
    muss im Kalender schon stehen.
    Mit --alten-plan-loeschen werden vorher alle Einträge einer angewendeten Plan-Vorlage
    (Wochenziele, Notizen, Workouts mit plan_applied) entfernt."""
    from . import saison
    von, bis = date(2026, 11, 16), date(2027, 9, 13)
    weit = (date(2026, 10, 1), date(2028, 1, 1))
    alle = client.events(*weit, category="TARGET,NOTE,WORKOUT,RACE_A")
    vorlage = [e for e in alle if e.get("plan_applied")
               and not str(e.get("external_id") or "").startswith("saison-")]
    print(f"Vorlagenplan: {len(vorlage)} Einträge "
          f"({', '.join(f'{k} {sum(1 for e in vorlage if e['category'] == k)}' for k in ('TARGET', 'NOTE', 'WORKOUT'))})")
    if a.apply and a.alten_plan_loeschen:
        for e in vorlage:
            client.delete_event(e["id"])
        vorlage_ids = {e["id"] for e in vorlage}
        alle = [e for e in alle if e["id"] not in vorlage_ids]
    bestehend = [e for e in alle if von <= date.fromisoformat(e["start_date_local"][:10]) <= bis]
    ziele = {(e["start_date_local"][:10], e.get("type")): e for e in bestehend
             if e.get("category") == "TARGET"}
    notizen = {e["start_date_local"][:10] for e in bestehend if e.get("category") == "NOTE"
               and not str(e.get("external_id") or "").startswith("saison-note-")}  # fremde Notizen
    neu, aendern = [], []
    for ev in saison.ziel_events():
        alt = ziele.get((ev["start_date_local"][:10], ev["type"]))
        if alt:
            if alt.get("load_target") != ev["load_target"]:
                aendern.append((alt["id"], ev["load_target"]))
        else:
            neu.append(ev)
    notiz = saison.notiz_events(notizen)
    gewollt = {n["external_id"] for n in saison.notiz_events(set())}  # alle gewünschten, auch schon vorhandene
    veraltet = [e for e in alle if e["category"] == "NOTE"
                and str(e.get("external_id") or "").startswith("saison-note-")
                and e["external_id"] not in gewollt]
    print("Woche      Soll-TSS")
    for tag, tss, rec in saison.WOCHEN:
        print(f"{tag}  {tss:6d}{' E' if rec else '  '}")
    print(f"\n{len(aendern)} Wochenziele werden geändert, {len(neu)} neu angelegt, "
          f"{len(notiz)} Notizen, {len(veraltet)} veraltete Notizen entfernt, Hauptwettkampf {saison.RENNTAG} bleibt unverändert.")
    if not a.apply:
        print("Vorschau – mit --apply in intervals.icu schreiben "
              "(--alten-plan-loeschen entfernt zusätzlich den Vorlagenplan).")
        return 0
    for eid, load in aendern:
        client.update_event(eid, {"load_target": load})
    for e in veraltet:
        client.delete_event(e["id"])
    client.upsert_events(neu + notiz + saison.rennen_events())
    print("✔ Saisonplan eingetragen.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="trainingsplan", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("befehl", choices=["analyse", "sync", "anpassen", "stufentest", "saison", "woche"])
    p.add_argument("--basis-ab", type=date.fromisoformat,
                   help="Vergleichszeitraum ab Datum (z.B. 2026-08-01): Normalwochen statt 4 Wochen")
    p.add_argument("--alten-plan-loeschen", action="store_true",
                   help="saison: Einträge einer angewendeten Plan-Vorlage vorher löschen")
    p.add_argument("--uebersicht", action="store_true",
                   help="saison: Übersicht nach plaene/saisonuebersicht.md schreiben (ohne Kalenderzugriff)")
    p.add_argument("--rad", type=date.fromisoformat, help="stufentest: Datum Rad-Stufentest")
    p.add_argument("--lauf", type=date.fromisoformat, help="stufentest: Datum Lauf-Stufentest")
    p.add_argument("--plan", default="plaene/trainingsplan.json", help="Plan als .json oder .csv")
    p.add_argument("--heute", type=date.fromisoformat, default=date.today())
    p.add_argument("--horizont", type=int, default=7, help="Tage, die angepasst werden")
    p.add_argument("--ohne-anpassung", action="store_true", help="Plan unverändert hochladen")
    p.add_argument("--apply", action="store_true", help="wirklich nach intervals.icu schreiben")
    p.add_argument("--bericht", default="berichte", help="Ordner für Markdown-Berichte")
    a = p.parse_args(argv)

    if a.befehl == "saison" and a.uebersicht:
        from . import saison
        text = saison.uebersicht_markdown()
        pfad = Path("plaene/saisonuebersicht.md")
        pfad.parent.mkdir(exist_ok=True)
        pfad.write_text(text, encoding="utf-8")
        print(text)
        return 0
    try:
        client = IntervalsClient()
        if a.befehl == "stufentest":
            return _stufentest(client, a)
        if a.befehl == "saison":
            return _saison(client, a)
        if a.befehl == "woche":
            return _woche(client, a)
        wellness, akt = _daten(client, a.heute, a.basis_ab)
    except IntervalsError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    b = bewerte(wellness, akt, a.heute, a.basis_ab)

    if a.befehl == "anpassen":
        try:
            evs = client.events(a.heute, a.heute + timedelta(days=a.horizont - 1))
        except IntervalsError as exc:
            print(f"Fehler: {exc}", file=sys.stderr)
            return 2
        plan = sorted((einheit_aus_event(e) for e in evs if e.get("category") == "WORKOUT"),
                      key=lambda e: e.datum)
    else:
        plan = lade_plan(a.plan) if Path(a.plan).exists() else []
    if a.befehl == "sync" and not plan:
        print(f"Fehler: Plan {a.plan} nicht gefunden", file=sys.stderr)
        return 2
    neu = plan if a.ohne_anpassung else passe_an(plan, b, a.heute, a.horizont)
    text = bericht(b, plan, neu, a.heute)
    print(text)
    Path(a.bericht).mkdir(parents=True, exist_ok=True)
    (Path(a.bericht) / f"{a.heute.isoformat()}.md").write_text(text, encoding="utf-8")

    if a.befehl == "anpassen":
        geaendert = [e for e in neu if e.angepasst and e.event_id]
        if not a.apply:
            print(f"Vorschau: {len(geaendert)} Einheiten würden geändert. Mit --apply übernehmen.")
            return 0
        for e in geaendert:
            ev = e.to_event()
            felder = {k: ev[k] for k in ("name", "description", "moving_time", "icu_training_load")
                      if k in ev}
            try:
                client.update_event(e.event_id, felder)
            except IntervalsError as exc:
                print(f"Fehler bei {e.datum} {e.name}: {exc}", file=sys.stderr)
                return 2
        print(f"✔ {len(geaendert)} Einheiten in intervals.icu angepasst.")
    elif a.befehl == "sync":
        kommend = [e for e in neu if e.datum >= a.heute]
        if not a.apply:
            print(f"Vorschau: {len(kommend)} Einheiten würden übertragen. Mit --apply hochladen.")
            return 0
        try:
            res = client.upsert_events([e.to_event() for e in kommend])
        except IntervalsError as exc:
            print(f"Fehler beim Upload: {exc}", file=sys.stderr)
            return 2
        print(f"✔ {len(res)} Einheiten in intervals.icu angelegt/aktualisiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
