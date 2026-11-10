"""CLI: python -m trainingsplan <befehl>

  analyse  – Trainings-/Gesundheitsdaten aus intervals.icu auswerten
  sync     – Plan (angepasst) nach intervals.icu übertragen
             (ohne --apply nur Vorschau, nichts wird geschrieben)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from .analyse import Bewertung, bewerte
from .anpassen import passe_an
from .intervals_icu import IntervalsClient, IntervalsError
from .plan import Einheit, lade_plan

AMPEL = {"gruen": "🟢 GRÜN – Plan wie geplant",
         "gelb": "🟡 GELB – Umfang/Intensität reduziert",
         "rot": "🔴 ROT – Erholung priorisiert"}


def _daten(client: IntervalsClient, heute: date) -> tuple[list[dict], list[dict]]:
    von = heute - timedelta(days=60)
    return client.wellness(von, heute), client.activities(von, heute)


def bericht(b: Bewertung, vorher: list[Einheit], nachher: list[Einheit], heute: date) -> str:
    z = [f"# Trainingsauswertung {heute.isoformat()}", "", f"**Status:** {AMPEL[b.status]}"
         + (" (gut erholt)" if b.frisch else ""), "", "## Kennzahlen", ""]
    namen = {"ctl": "Fitness (CTL)", "atl": "Ermüdung (ATL)", "tsb": "Form (TSB)",
             "form_pct": "Form %", "ramp_rate": "Ramp Rate", "hrv_7d": "HRV 7 Tage",
             "hrv_basis": "HRV Basis", "hrv_z": "HRV z-Wert", "ruhepuls_7d": "Ruhepuls 7 Tage",
             "ruhepuls_basis": "Ruhepuls Basis", "schlaf_h_7d": "Schlaf Ø h (7 T.)",
             "load_7d": "Load letzte 7 Tage", "load_wochenschnitt_4w": "Load Ø/Woche (4 W.)",
             "acwr": "Akut:Chronisch", "fatigue_3d": "Müdigkeit (3 T.)",
             "soreness_3d": "Muskelkater (3 T.)", "stress_3d": "Stress (3 T.)"}
    z += ["| Kennzahl | Wert |", "|---|---|"]
    z += [f"| {namen.get(k, k)} | {v} |" for k, v in b.kennzahlen.items()]
    z += ["", "## Auffälligkeiten", ""]
    z += [f"- {s.text}" for s in b.signale] or ["- keine"]
    alt = {e.external_id: e for e in vorher}
    geaendert = [e for e in nachher if e.angepasst]
    z += ["", "## Planänderungen", ""]
    if not geaendert:
        z.append("- keine")
    for e in geaendert:
        o = alt.get(e.external_id) or next((x for x in vorher if x.datum == e.datum), e)
        z.append(f"- **{e.datum:%a %d.%m.}** {o.name}: {o.dauer_min:.0f} min"
                 f"{f' / {o.load:.0f} TSS' if o.load else ''} → {e.name}: {e.dauer_min:.0f} min"
                 f"{f' / {e.load:.0f} TSS' if e.load else ''} ({'; '.join(e.angepasst)})")
    z += ["", "_Hinweis: Faustregeln auf Basis deiner intervals.icu-Daten, kein ärztlicher Rat._", ""]
    return "\n".join(z)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="trainingsplan", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("befehl", choices=["analyse", "sync"])
    p.add_argument("--plan", default="plaene/trainingsplan.json", help="Plan als .json oder .csv")
    p.add_argument("--heute", type=date.fromisoformat, default=date.today())
    p.add_argument("--horizont", type=int, default=7, help="Tage, die angepasst werden")
    p.add_argument("--ohne-anpassung", action="store_true", help="Plan unverändert hochladen")
    p.add_argument("--apply", action="store_true", help="wirklich nach intervals.icu schreiben")
    p.add_argument("--bericht", default="berichte", help="Ordner für Markdown-Berichte")
    a = p.parse_args(argv)

    try:
        client = IntervalsClient()
        wellness, akt = _daten(client, a.heute)
    except IntervalsError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    b = bewerte(wellness, akt, a.heute)

    plan = lade_plan(a.plan) if Path(a.plan).exists() else []
    if a.befehl == "sync" and not plan:
        print(f"Fehler: Plan {a.plan} nicht gefunden", file=sys.stderr)
        return 2
    neu = plan if a.ohne_anpassung else passe_an(plan, b, a.heute, a.horizont)
    text = bericht(b, plan, neu, a.heute)
    print(text)
    Path(a.bericht).mkdir(parents=True, exist_ok=True)
    (Path(a.bericht) / f"{a.heute.isoformat()}.md").write_text(text, encoding="utf-8")

    if a.befehl == "sync":
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
