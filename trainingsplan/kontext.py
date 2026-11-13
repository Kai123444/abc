"""Kontext aus intervals.icu: Einstiegsnotiz und Kaltstart-Ausgabe.

Alles Wissen über den Athleten steht in intervals.icu (Profil-Notizen, Phasen, Wochenziele, Rennen, Bibliothek,
Wellness-Kommentare). `python -m trainingsplan kontext` stellt es ohne Chat-Verlauf zusammen; die Einstiegsnotiz
"00 START HIER" erklärt, wo was steht und wie gearbeitet wird.
"""

from __future__ import annotations

from datetime import date, timedelta

START_NOTIZ = """00 START HIER (Stand 11.11.2026). Wer den Athleten coacht, liest zuerst diese Notiz, dann Profil 1 bis 6, dann die aktuelle Phase und die Woche.

WO STEHT WAS (alles in intervals.icu)
- Profil 1-6 (11.-13.11.): Kennwerte, Historie, Verfügbarkeit, Ausrüstung, Ziele, Ernährung, Supplements, Erholung, Offene Punkte, Verlauf, Entscheidungen, Pace-Zonen, Werkzeuge.
- Phasen als Zeitspannen im Kalender: Phase 0 bis 4, Taper und Höchstform, Spätsaison. Dazu am 23.11.: Wochenstruktur und Kontrolle, Krafttraining Kraftraum, Stabi und Fußkraft (Fr abend, Stufen 1-3), Rad-Intervalle, Koppeltraining, Mittwochs-Intervalle Lauf.
- Wochenziele: TARGET-Einträge pro Sportart (Rad, Lauf, Schwimmen, Sonstiges) für jede Woche bis 06.09.2027. Übersicht Woche für Woche: Notiz 'Saisonübersicht: Woche für Woche'.
- Rennen: RACE-Einträge (DM Kurzdistanz 08.08.2027 mit Strecken, Zeitplan, Verpflegung und Supplements; Cottbus 12.06.2027; Hölle von Q 05.09.2027). Notizen DM-Strecke: Training abgleichen, DM Vortag, DM Renntag, Zeitfahrrad.
- Verpflegung: Notizen 'Verpflegung: Grundregeln', 'Darmtraining: Plan und Regeln' (plus Termine), 'Supplements: Plan und Regeln', 'Radrennen-Fenster 1-5'; jede Einheit mit Dauer ab 60 min hat unten einen Block 'Verpflegung'.
- Erholung: 'Sauna: Erholung und Hitzeanpassung' (05.07.), Sauna und Eis stehen im Wellness-Kommentar des Tages und als Notiz 'Sauna / Kälte'.
- Tests und Bricks: Retest-Notizen (23.01., 20.03., Zeitfahrtest 13.05., Generalprobe 10.07.), 'Koppel: Renn-Brick 1-4' und 'Koppel: Generalprobe DM'.
- Bibliothek (Workouts): 15 Ordner 01-07 Rad, 10-12 Lauf, 20 Koppel und Brick, 30 Schwimmen, 40 Kraft, 50 Rennen mit allen Einheiten des Plans.
- Hitzetraining: Notizen 'Hitzetraining Jahresplan', Phase 1-3, 'Mini-Block vor Cottbus', 'Plan für die DM' (05.-25.07.) und Wochen-Notizen; Heat-Ride auf der Rolle (Di), im Sommer Heat-Lauf. Abitur: Notizen 'Ferien und Abitur' und 'Abitur: geplante Plananpassung (noch nicht umgesetzt)'.
- Verfügbarkeit: Notiz 'Verfügbarkeit pro Wochentag (Schulzeit)' (Zeitfenster Mo-Do, Vereinstermine) und 'Ferien Brandenburg 2026/27' plus Ferien-Spannen im Kalender. Einheiten müssen in diese Fenster passen.
- Aktivitäten und Wellness (HRV, Ruhepuls, Schlaf) kommen automatisch von Garmin/Wahoo.

ZUSAMMENARBEIT UND WERKZEUGE
- Antworten und Plan auf Deutsch. Vor jedem Schreiben erst die Vorschau (ohne --apply) zeigen, dann eintragen.
- Werkzeug: Python-Paket im GitHub-Repository kai123444/abc, Branch claude/trainingsplan-interval-icu-j2qi2i. Aufruf: python -m trainingsplan <befehl>. Befehle: kontext (kompakter Einstieg, rund 9.000 Zeichen; kontext --profil N für ein Profil, kontext --alles für alles), analyse (Ampel aus HRV, Ruhepuls, Schlaf, Form, Last), anpassen, saison, woche, verpflegung, dm, bibliothek, stufentest, log.
- Zugang: Der intervals.icu-API-Key liegt als Network Secret (Basic Auth, Benutzer API_KEY) in der Cloud-Umgebung 'abc' mit erlaubtem Host intervals.icu; im Code INTERVALS_API_KEY=proxy-injected setzen. Der Key kommt nie in Chat oder Repository.
- Datenschutz: Das Profil steht nur in intervals.icu, nicht ins Repository (es wirkt öffentlich). Keine E-Mail-Adressen oder Gesundheitsdaten in Commits.

REGELN
- Eigene Einträge des Athleten (DM und Hölle von Q, Vereinstraining, Schultermine, Rennen, Aktivitäten) nicht löschen oder überschreiben; Löschen und Verschieben nur auf Wunsch.
- Aufbau nach Anpassungsfähigkeit: CTL-Anstieg höchstens ca. 4,5 pro Woche, Laufumfang höchstens +10 % pro Woche, alle 4 Wochen Erholungswoche. Ampel: Gelb bei HRV 7-Tage-Mittel unter ca. 78 oder Ruhepuls über ca. 51 (Umfang -15 %), Rot bei HRV unter ca. 68 oder Ruhepuls über ca. 54 (Intensität streichen). Sauna und Eisbad vorher eintragen, die Morgenwerte danach werden eingeordnet.
- Nach Tests Schwellen und Zonen aktualisieren, dann Paces und Prozente der Workouts prüfen.
- Neue Einheiten immer mit Verpflegungsblock, Intervalle nach Leistung (% FTP), 'm' = Minuten und 'mtr' = Meter in der Workout-Syntax von intervals.icu."""


def kontext_text(client, heute: date, alles: bool = False, profil: int | None = None) -> str:
    """Kompakter Einstieg (Standard): Einstiegsnotiz, Profil 6 (Verlauf), Phase, Woche, Rennen, Wellness.
    `profil=N` gibt nur Profil N aus, `alles=True` alle Profile und die Bibliothek."""
    noten = client.events(date(2026, 1, 1), date(2027, 12, 31), category="NOTE")
    profile = {int(n["external_id"].split("-")[1]): n for n in noten
               if (n.get("external_id") or "").startswith("profil-") and n["external_id"].split("-")[1].isdigit()}
    if profil is not None:
        n = profile.get(profil)
        return f"## {n['name']}\n{n.get('description') or ''}" if n else f"Profil {profil} nicht gefunden (vorhanden: {sorted(profile)})"
    a = client.athlete()
    z: list[str] = ["# Kontext aus intervals.icu", ""]
    z.append(f"Athlet: {a.get('name')}, {a.get('city')}, {a.get('icu_weight')} kg")
    for st in a.get("sportSettings", []):
        z.append(f"- {', '.join(st.get('types', [])[:1])}: FTP {st.get('ftp')}, LTHR {st.get('lthr')}, Max-HF {st.get('max_hr')}, "
                 f"Schwellen-Pace {st.get('threshold_pace')}")
    if 0 in profile:
        z += ["", "## " + profile[0]["name"], profile[0].get("description") or ""]
    for k in sorted(profile):
        if k == 0 or not (alles or k == 6):
            continue
        z += ["", "## " + profile[k]["name"], profile[k].get("description") or ""]
    if not alles:
        z += ["", "Weitere Details: python -m trainingsplan kontext --profil N (Profil 1 Kennwerte und Historie, 2 Verfügbarkeit, "
              "3 Ziele und Plan, 4 Ernährung und Supplements, 5 Offene Punkte) oder --alles."]
    phase = [n for n in noten if (n.get("name") or "").startswith(("Phase", "Taper", "Nach dem"))
             and n["start_date_local"][:10] <= heute.isoformat() < (n.get("end_date_local") or "9999")[:10]]
    z += ["", "## Aktuelle Phase", (phase[0]["name"] + ("\n" + (phase[0].get("description") or "") if alles else "")) if phase else "keine Phase im Kalender"]
    mo = heute - timedelta(days=heute.weekday())
    woche = client.events(mo, mo + timedelta(days=6), category="WORKOUT,TARGET")
    ziele = {e["type"]: e.get("load_target") for e in woche if e["category"] == "TARGET"}
    z += ["", f"## Woche ab {mo:%d.%m.}", f"Wochenziele (TSS): {ziele}"]
    for e in sorted((e for e in woche if e["category"] == "WORKOUT"), key=lambda e: e["start_date_local"]):
        z.append(f"- {e['start_date_local'][:10]} {e.get('type')}: {e['name']} ({round((e.get('moving_time') or 0) / 60)} min)")
    rennen = client.events(heute, heute + timedelta(days=400), category="RACE_A,RACE_B,RACE_C")
    z += ["", "## Kommende Rennen"]
    z += [f"- {r['start_date_local'][:10]} {r['category']}: {r['name']}" for r in sorted(rennen, key=lambda r: r["start_date_local"])]
    if alles:
        ordner = [f for f in client._request("GET", client._athlete("/folders")) if f["name"] != "Workouts"]
        w = client._request("GET", client._athlete("/workouts")) or []
        z += ["", f"## Bibliothek: {len(w)} Workouts in {len(ordner)} Ordnern"]
        z += [f"- {f['name']}" for f in sorted(ordner, key=lambda f: f["name"])]
    well = client.wellness(heute - timedelta(days=7), heute)
    z += ["", "## Wellness letzte 7 Tage"]
    for x in well:
        z.append(f"- {x['id']}: HRV {x.get('hrv')}, Ruhepuls {x.get('restingHR')}, Schlaf "
                 f"{round(x['sleepSecs'] / 3600, 1) if x.get('sleepSecs') else '-'} h"
                 + (f", Kommentar: {x['comments']}" if x.get("comments") else ""))
    return "\n".join(z)


def start_event() -> dict:
    return {"category": "NOTE", "name": "00 START HIER", "description": START_NOTIZ,
            "start_date_local": "2026-11-11T00:00:00", "end_date_local": "2026-11-12T00:00:00",
            "external_id": "profil-0"}


def wochen_event() -> dict:
    from . import saison
    text = saison.uebersicht_markdown()
    teil = text.split("## Woche für Woche", 1)[1].split("## Rennkalender", 1)[0].strip()
    return {"category": "NOTE", "name": "Saisonübersicht: Woche für Woche",
            "description": "Saisonübersicht bis zur DM (08.08.2027), Wochenziele in TSS und grobe Stunden, CTL/Form laut "
                           "Simulation:\n" + teil,
            "start_date_local": "2026-11-11T00:00:00", "end_date_local": "2026-11-12T00:00:00",
            "external_id": "saison-woche-fuer-woche"}
