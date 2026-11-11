"""Vereinstermine als Kalendereinträge (Schwimmen Di/Do, Lauf Mi ab 09.12.2026).

Regeln (Stand 11.11.2026, Angaben von Kai): Vereinstraining Schwimmen Di 17:00 und Do 17:30 (je 70 min), Lauf Mi ab 17:00 mit
Einlaufen, Lauf-ABC und Intervallen auf der Bahn. Am 18.11. und 02.12. kein Vereinstraining (25.11. ebenfalls nicht angenommen,
bitte bestätigen); der Verein läuft ab 09.12.2026. In den Schulferien ist kein Vereinstraining.
"""

from __future__ import annotations

from datetime import date, timedelta

FERIEN = [("2026-12-23", "2027-01-02"), ("2027-02-01", "2027-02-06"), ("2027-03-22", "2027-04-03")]
SCHWIMMEN_VON, LAUF_VON, ENDE = date(2026, 12, 1), date(2026, 12, 9), date(2027, 6, 30)
KEIN_VEREIN = {"2026-11-18", "2026-11-25", "2026-12-02"}  # Mittwoch, Lauf

SCHWIMMEN = {1: ("17:00", "Vereinstraining Schwimmen (Di 17:00)"), 3: ("17:30", "Vereinstraining Schwimmen (Do 17:30)")}
LAUF_TEXT = ("Vereinstraining Lauf auf der Bahn in Cottbus, Treffen ca. 17:00: Einlaufen 2-3 km, Lauf-ABC, danach die Intervalle des Trainers "
             "(meist 400-1000 m), Auslaufen. Vorher Mi ab 13:30 nur Oberkörper-Kraft (35 min), keine schweren Beine. Pace nach dem "
             "Lauf-Stufentest 18.11. richten: Wiederholungen nicht schneller als die Zielpace. Nur eine harte Laufeinheit pro Woche.\n"
             "- 20m 6:50/km Pace\n- 5m 6:30/km Pace\n- 30m 4:15/km Pace\n- 10m 7:00/km Pace")


def _ferien(d: date) -> bool:
    return any(a <= d.isoformat() <= b for a, b in FERIEN)


def events() -> list[dict]:
    out = []
    d = SCHWIMMEN_VON
    while d <= ENDE:
        if not _ferien(d):
            if d.weekday() in SCHWIMMEN:
                zeit, name = SCHWIMMEN[d.weekday()]
                out.append({"category": "WORKOUT", "type": "Swim", "name": name, "moving_time": 70 * 60,
                            "start_date_local": f"{d.isoformat()}T00:00:00",
                            "description": f"Vereinstraining, Start {zeit}. Inhalt gibt der Trainer vor; Technik und Ausdauer.",
                            "external_id": f"verein-{d.isoformat()}-swim"})
            if d.weekday() == 2 and d >= LAUF_VON and d.isoformat() not in KEIN_VEREIN:
                out.append({"category": "WORKOUT", "type": "Run", "name": "Vereinstraining Lauf (Bahn Cottbus, Mi 17:00)",
                            "moving_time": 65 * 60, "start_date_local": f"{d.isoformat()}T00:00:00",
                            "description": LAUF_TEXT, "external_id": f"verein-{d.isoformat()}-lauf"})
        d += timedelta(days=1)
    return out


def notiz_events() -> list[dict]:
    text = ("Vereinstermine (Stand 11.11.2026):\n"
            "- Schwimmen: Di 17:00 und Do 17:30, je 70 min, in der Schulzeit bis Ende Juni 2027.\n"
            "- Lauf (Bahn Cottbus): Mi ab 17:00, Einlaufen, Lauf-ABC, Intervalle. Start ab Mi 09.12.2026. Am 18.11. und 02.12. kein "
            "Vereinstraining, 25.11. ebenfalls nicht angenommen (bestätigen). Bis dahin läufst du die Mittwochseinheit allein.\n"
            "- In den Schulferien ist kein Vereinstraining (Weihnachten 23.12.-02.01., Winter 01.-06.02., Ostern 22.03.-03.04.).\n"
            "- Im Kalender stehen die Einheiten als 'Vereinstraining ...' (Swim ab 01.12.2026, Lauf ab 09.12.2026). Die Zeit des Vereins "
            "zählt nicht in die nutzbare Zeit des Verfügbarkeits-Kalenders.\n"
            "- Offen: Sommer-Pause des Vereins und die Zeit nach dem Abitur bestätigen.")
    return [{"category": "NOTE", "name": "Vereinstermine: Schwimmen und Lauf", "description": text,
             "start_date_local": "2026-11-11T00:00:00", "end_date_local": "2026-11-12T00:00:00", "external_id": "vereinstermine"}]
