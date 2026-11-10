"""Grobe Saisonplanung 2026/27: Wochenziele (TARGET) und Phasen-Notizen (NOTE) für intervals.icu.

Grundlagen (aus intervals.icu, Strava-Import ab 2020):
* Rad-Basis: 2020-2022 je 6-9 h/Woche (12-16k TSS/Jahr), CTL-Maximum 74 (Juli 2021), 29 % der
  aktiven Wochen über 400 TSS. 2023-2025 fast Pause, 2026 Wiedereinstieg als Triathlet (CTL bis 40).
* Limitierend sind Laufen (bis 2026 kaum Läufe) und Schwimmen -> Lauf-Load steigt nur etwa 10 % pro
  Woche, Schwimmen ist durch das Vereinstraining (2 x 70 min, ca. 105 TSS) fest vorgegeben.
* Hauptwettkampf: DM Kurzdistanz am Sonntag 08.08.2027 (1,5 km / 40 km / 10 km, geschätzt ca. 2:30 h,
  ca. 200-220 TSS). Aufbau bis Mitte Juli, 2 Wochen Taper, Form am Renntag +10 bis +20.
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
    ("2027-05-17", 490, False), ("2027-05-24", 500, False), ("2027-05-31", 510, False),
    ("2027-06-07", 340, True),
    ("2027-06-14", 500, False), ("2027-06-21", 510, False), ("2027-06-28", 520, False),
    ("2027-07-05", 350, True),
    ("2027-07-12", 510, False), ("2027-07-19", 490, False),
    # Taper: -25 %, Rennwoche 400 = ca. 190 Vorbereitung + ca. 210 Rennen, Woche danach locker
    ("2027-07-26", 370, True), ("2027-08-02", 400, True), ("2027-08-09", 120, True),
]

RENNTAG = "2027-08-08"
TAPER_WOCHEN = {"2027-07-26", "2027-08-02", "2027-08-09"}  # keine "Erholungswoche"-Notiz

# Schwimmen und Kraft sind feste Größen (Vereinstraining, Krafttraining), der Rest geht an Rad/Lauf.
SCHWIMMEN = {"normal": 105, "erholung": 75, "2027-07-26": 80, "2027-08-02": 60, "2027-08-09": 30}
KRAFT = {"normal": 30, "erholung": 20, "2027-07-26": 20, "2027-08-02": 10, "2027-08-09": 0}

ERHOLUNG_TEXT = ("Fokus auf leichtere Belastungen, reduziertes Volumen und Anpassung des Körpers an "
                 "Trainingsstress (Radfahren, Laufen, Schwimmen, Andere)")
# (Samstag, Name, Beschreibung) – Retests/Formchecks ausgeruht in der Erholungswoche
RETESTS = [
    ("2027-01-23", "Retest Stufentests",
     "Rad-Stufentest und Lauf-Stufentest wiederholen (ausgeruht, in der Erholungswoche). "
     "Danach FTP, Laufschwelle, LTHR und Zonen in intervals.icu aktualisieren."),
    ("2027-03-20", "Retest Stufentests",
     "Zweiter Retest: Rad-Stufentest und Lauf-Stufentest. Vergleich mit November und "
     "Januar zeigt, ob Aufbau und Zonen passen."),
    ("2027-06-12", "Formcheck Renntempo",
     "In der Erholungswoche: 20-min-Radtest (FTP kontrollieren) und 5-km-Lauf auf Zeit. Daraus "
     "Renntempo ableiten: Rad ca. 85-90 % FTP über 40 km, Lauf etwa 10-km-Pace."),
    ("2027-07-10", "Generalprobe Kurzdistanz",
     "In der Erholungswoche: Koppel 30 km Rad im Renntempo + 5 km Lauf im Renntempo, "
     "Verpflegung und Wechsel üben. Optional ein Sprint-Triathlon als Formtest."),
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
     "Erholungswoche. Deine Radbasis aus 2020-2022 (6-9 h/Woche, CTL bis 74) ist da und kommt "
     "schnell zurück. Engpässe sind Laufen und Schwimmen: 3 Läufe pro Woche mit einem langen "
     "Lauf, Lauf-Load nur etwa +10 % pro Woche, Schwimmen = Vereinstraining plus Technik.\n"
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
     "Kurzdistanz (1,5 km / 40 km / 10 km, geschätzt ca. 2:30 h): Koppeltraining Rad -> Lauf, "
     "Renntempo-Blöcke (Rad 3x15 min im Renntempo, Lauf 3x2 km), lange Radfahrt bis 3 h, langer Lauf "
     "bis 90 min, Freiwasserschwimmen ab Mai, 1,5 km am Stück. Load 490-520, Erholungswochen am "
     "07.06. und 05.07., letzter Block 12.-25.07.\n"
     "Erwartung: CTL 62 -> ca. 66 Mitte Juli (dein Maximum war 74 im Jahr 2021), Form -3 bis -9. "
     "Die Ampel ernst nehmen: bei Gelb Umfang kürzen, aber die Schlüsseleinheiten behalten."),
    ("2027-07-26", "Taper und Höchstform (26.07.-08.08.)",
     "Volumen -25 % (Woche 370), Rennwoche ca. 190 TSS Vorbereitung plus Rennen (ca. 200-220 TSS, "
     "Wochenziel 400 enthält das Rennen). Intensität bleibt kurz und scharf (2-3 Reize à 3-5 min im "
     "Renntempo), nichts Neues ausprobieren, Schlaf 8-9 h, ausreichend Kohlenhydrate.\n"
     "Erwartung: CTL sinkt nur leicht (ca. 66 -> 60), ATL fällt von ca. 69 auf ca. 42, Form am "
     "Renntag ca. +18 (Ziel +10 bis +20), HRV über Basis (90 oder mehr), Ruhepuls an oder unter "
     "Basis (46-47). Liegt in der Rennwoche die HRV unter ca. 78 oder der Ruhepuls über ca. 51: "
     "Intensität weglassen, nur locker aktivieren."),
    ("2027-08-09", "Nach dem Wettkampf (ab 09.08.)",
     "Eine Woche locker (Load ca. 120), danach entscheiden: Spätsaison mit kurzem Aufbau oder "
     "direkt Off-Season (2-4 Wochen aktive Pause, Load unter 150).\n"
     "Erwartung: Form bleibt erst hoch (+15 bis +25), CTL fällt in der Pause auf ca. 30-35. "
     "Beim Wiedereinstieg die Wochenload über 3-4 Wochen auf die Normalwoche anheben."),
]


def verteilung(gesamt: int, tag: str = "2026-11-16", erholung: bool = False) -> dict[str, int]:
    """Wochenload auf Sportarten verteilen. Lauf bekommt vom Rest 36 % (ab März 38 %), weil Laufen
    der Engpass für die 10 km nach dem Rad ist und langsam wachsen soll."""
    art = tag if tag in SCHWIMMEN else ("erholung" if erholung else "normal")
    swim, kraft = SCHWIMMEN[art], KRAFT[art]
    rest = max(gesamt - swim - kraft, 0)
    anteil = 0.35 if tag in TAPER_WOCHEN else (0.38 if tag >= "2027-03-01" else 0.36)
    lauf = round(rest * anteil)
    return {"Ride": rest - lauf, "Run": lauf, "Swim": swim, "Other": kraft}


def montag(datum: str) -> date:
    d = date.fromisoformat(datum)
    assert d.weekday() == 0, f"{datum} ist kein Montag"
    return d


def ziel_events() -> list[dict]:
    """Alle Wochenziele als TARGET-Events (external_id = saison-<Montag>-<Sport>)."""
    out = []
    for tag, tss, erholung in WOCHEN:
        d = montag(tag)
        for sport, load in verteilung(tss, tag, erholung).items():
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
    for tag, name, text in RETESTS:
        out.append((date.fromisoformat(tag), name, text))
    events = []
    for d, name, text in out:
        if name == "Erholungswoche" and d.isoformat() in vorhandene_notizen:
            continue
        events.append({"category": "NOTE", "name": name, "description": text,
                       "start_date_local": f"{d.isoformat()}T00:00:00",
                       "end_date_local": f"{(d + timedelta(days=1)).isoformat()}T00:00:00",
                       "external_id": f"saison-note-{d.isoformat()}-{name[:7].lower().strip(':')}"})
    return events
