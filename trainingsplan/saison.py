"""Grobe Saisonplanung 2026/27: Wochenziele (TARGET) und Phasen-Notizen (NOTE) für intervals.icu.

Annahmen (aus deinen Daten ab August 2026):
* Normalwoche ~345 TSS, Spitzenwoche 443 TSS, CTL-Höchststand 37, aktuell ~26.
* CTL-Anstieg höchstens ~2-3 pro Woche, alle 4 Wochen eine Erholungswoche (-30 %).
* Hauptwettkampf Sonntag 08.08.2027: Aufbau bis Mitte Juli, 2 Wochen Taper, Form am Renntag +10 bis +20.
"""

from __future__ import annotations

from datetime import date, timedelta

# (Montag, TSS gesamt pro Woche, Erholungswoche?)
WOCHEN: list[tuple[str, int, bool]] = [
    ("2026-11-16", 330, False), ("2026-11-23", 240, True),
    ("2026-11-30", 340, False), ("2026-12-07", 365, False), ("2026-12-14", 385, False),
    ("2026-12-21", 265, True),
    ("2026-12-28", 375, False), ("2027-01-04", 395, False), ("2027-01-11", 410, False),
    ("2027-01-18", 285, True),
    ("2027-01-25", 410, False), ("2027-02-01", 425, False), ("2027-02-08", 440, False),
    ("2027-02-15", 300, True),
    ("2027-02-22", 435, False), ("2027-03-01", 450, False), ("2027-03-08", 460, False),
    ("2027-03-15", 315, True),
    ("2027-03-22", 460, False), ("2027-03-29", 470, False), ("2027-04-05", 480, False),
    ("2027-04-12", 325, True),
    ("2027-04-19", 475, False), ("2027-04-26", 485, False), ("2027-05-03", 495, False),
    ("2027-05-10", 335, True),
    # Vorbereitung auf den Hauptwettkampf am Sonntag 08.08.2027
    ("2027-05-17", 470, False), ("2027-05-24", 480, False), ("2027-05-31", 480, False),
    ("2027-06-07", 330, True),
    ("2027-06-14", 470, False), ("2027-06-21", 480, False), ("2027-06-28", 490, False),
    ("2027-07-05", 340, True),
    ("2027-07-12", 480, False), ("2027-07-19", 470, False),
    # Taper: -25 %, Rennwoche ~200 (ohne Rennen), Woche danach locker
    ("2027-07-26", 360, True), ("2027-08-02", 200, True), ("2027-08-09", 120, True),
]

RENNTAG = "2027-08-08"
TAPER_WOCHEN = {"2027-07-26", "2027-08-02", "2027-08-09"}  # keine "Erholungswoche"-Notiz

# Verteilung auf die Sportarten (wie im bisherigen Plan: Rad > Lauf > Schwimmen > Sonstiges)
SPLIT = {"Ride": 0.53, "Run": 0.21, "Swim": 0.16, "Other": 0.10}

ERHOLUNG_TEXT = ("Fokus auf leichtere Belastungen, reduziertes Volumen und Anpassung des Körpers an "
                 "Trainingsstress (Radfahren, Laufen, Schwimmen, Andere)")
# (Samstag, Beschreibung) – Retests ausgeruht in der Erholungswoche
RETESTS = [
    ("2027-01-23", "Rad-Stufentest und Lauf-Stufentest wiederholen (ausgeruht, in der Erholungswoche). "
                   "Danach FTP, Laufschwelle, LTHR und Zonen in intervals.icu aktualisieren."),
    ("2027-03-20", "Zweiter Retest: Rad-Stufentest und Lauf-Stufentest. Vergleich mit November und "
                   "Januar zeigt, ob Aufbau und Zonen passen."),
]

# (Montag, Name, Beschreibung)
PHASEN: list[tuple[str, str, str]] = [
    ("2026-11-16", "Phase 0: Wiedereinstieg und Tests (bis 29.11.)",
     "Ziel: nach Krankheit/Off-Season wieder Normalbetrieb, Schwellenwerte ermitteln "
     "(Rad-Stufentest 14.11., Lauf-Stufentest 17.11.). Load 240-330 pro Woche.\n"
     "Erwartung: CTL 26 -> ca. 32, Form -7 bis -14. HRV (~90) und Ruhepuls (~47) bleiben auf "
     "deiner Basis, Schlaf ~8 h. Danach FTP, LTHR und Zonen aus den Tests übernehmen."),
    ("2026-11-30", "Phase 1: Grundlage I (30.11.-24.01.)",
     "Aerobes Volumen (Z2), Schwimmtechnik, Kraft 1-2x pro Woche, höchstens eine "
     "Intensitätseinheit pro Woche (Sweet Spot bis 2x15 min). Load 340 -> 410, alle 4 Wochen "
     "Erholungswoche.\n"
     "Erwartung: CTL 32 -> ca. 46 (+2,5 pro Woche), Form -10 bis -13 in Belastungswochen, "
     "0 bis -4 in Erholungswochen. In der 3. Belastungswoche sind HRV 5-10 % unter Basis und "
     "Ruhepuls +1-3 bpm normal, in der Erholungswoche kommt beides zurück."),
    ("2027-01-25", "Phase 2: Grundlage II / Aufbau (25.01.-21.03.)",
     "Sweet Spot und Schwelle (2x pro Woche), Tempodauerläufe nahe Schwellenpace, "
     "Schwimmen mit Schwellenblöcken, Kraft weiter. Load 410 -> 460.\n"
     "Erwartung: CTL 46 -> ca. 57, Form -6 bis -11. Ruhepuls im Wochenmittel +1-2 bpm in "
     "Belastungswochen. Handlungsbedarf erst bei HRV 7-Tage-Mittel unter ca. 78 oder Ruhepuls "
     "über ca. 51 (dann schlägt die Ampel in Gelb um)."),
    ("2027-03-22", "Phase 3: Spezifisch (22.03.-09.05.)",
     "VO2max-Intervalle 1x pro Woche, Wettkampftempo-Blöcke, Koppeltraining Rad -> Lauf, "
     "lange Z2-Einheiten. Load 460 -> 495.\n"
     "Erwartung: CTL 57 -> ca. 62 (flacherer Anstieg), Form -4 bis -9. Mehr Intensität heißt "
     "stärkere Reaktion: nach harten Tagen HRV 10-15 % niedriger ist normal und sollte nach "
     "48 h zurück sein. Ab hier die Ampel (Gelb/Rot) ernst nehmen."),
    ("2027-05-17", "Phase 4: Wettkampfvorbereitung (17.05.-25.07.)",
     "Wettkampfspezifisch: Koppeltraining Rad -> Lauf, Wettkampftempo-Blöcke, lange Z2-Einheiten, "
     "eine Intensitätseinheit pro Sportart. Load 470-490, Erholungswochen am 07.06. und 05.07. "
     "(2 Blöcke zu 3 Wochen, danach letzter Block 12.-25.07.).\n"
     "Erwartung: CTL 62 -> ca. 65 Mitte Juli (Höhepunkt der Fitness), Form -3 bis -9. Die Ampel "
     "ernst nehmen: bei Gelb Umfang kürzen, aber die Schlüsseleinheiten behalten."),
    ("2027-07-26", "Taper und Höchstform (26.07.-08.08.)",
     "Volumen -25 % (Woche 360), Rennwoche ca. 200 TSS plus Rennen, Intensität bleibt kurz und "
     "scharf (2-3 Reize à 3-5 min im Renntempo), nichts Neues ausprobieren, Schlaf 8-9 h, "
     "ausreichend Kohlenhydrate.\n"
     "Erwartung: CTL sinkt nur leicht (ca. 65 -> 58), ATL fällt von ca. 66 auf ca. 40, "
     "Form am Renntag ca. +16 (Ziel +10 bis +20), HRV über Basis (90 oder mehr), Ruhepuls an oder "
     "unter Basis (46-47). Liegt in der Rennwoche die HRV unter ca. 78 oder der Ruhepuls über "
     "ca. 51: Intensität weglassen, nur locker aktivieren."),
    ("2027-08-09", "Nach dem Wettkampf (ab 09.08.)",
     "Eine Woche locker (Load ca. 120), danach entscheiden: Spätsaison mit kurzem Aufbau oder "
     "direkt Off-Season (2-4 Wochen aktive Pause, Load unter 150).\n"
     "Erwartung: Form bleibt erst hoch (+15 bis +25), CTL fällt in der Pause auf ca. 30-35. "
     "Beim Wiedereinstieg die Wochenload über 3-4 Wochen auf die Normalwoche anheben."),
]


def verteilung(gesamt: int) -> dict[str, int]:
    teile = {sport: round(gesamt * anteil) for sport, anteil in SPLIT.items()}
    teile["Ride"] += gesamt - sum(teile.values())  # Rundung ausgleichen
    return teile


def montag(datum: str) -> date:
    d = date.fromisoformat(datum)
    assert d.weekday() == 0, f"{datum} ist kein Montag"
    return d


def ziel_events() -> list[dict]:
    """Alle Wochenziele als TARGET-Events (external_id = saison-<Montag>-<Sport>)."""
    out = []
    for tag, tss, _ in WOCHEN:
        d = montag(tag)
        for sport, load in verteilung(tss).items():
            out.append({"category": "TARGET", "type": sport, "name": "Weekly",
                        "start_date_local": f"{d.isoformat()}T00:00:00",
                        "end_date_local": f"{(d + timedelta(days=1)).isoformat()}T00:00:00",
                        "load_target": load, "training_availability": "NORMAL",
                        "external_id": f"saison-{d.isoformat()}-{sport}"})
    return out


def notiz_events(vorhandene_notizen: set[str]) -> list[dict]:
    """Phasen- und Erholungswochen-Notizen; schon vorhandene Tage werden ausgelassen."""
    out = []
    for tag, name, text in PHASEN:
        d = montag(tag)
        out.append((d, name, text))
    for tag, _, erholung in WOCHEN:
        if erholung and tag not in TAPER_WOCHEN:
            d = montag(tag)
            out.append((d, "Erholungswoche", ERHOLUNG_TEXT))
    for tag, text in RETESTS:
        out.append((date.fromisoformat(tag), "Retest Stufentests", text))
    events = []
    for d, name, text in out:
        if name == "Erholungswoche" and d.isoformat() in vorhandene_notizen:
            continue
        events.append({"category": "NOTE", "name": name, "description": text,
                       "start_date_local": f"{d.isoformat()}T00:00:00",
                       "end_date_local": f"{(d + timedelta(days=1)).isoformat()}T00:00:00",
                       "external_id": f"saison-note-{d.isoformat()}-{name[:7].lower().strip(':')}"})
    return events
