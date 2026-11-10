"""Saisonplanung 2026/27 bis zur DM Kurzdistanz (So 08.08.2027) für intervals.icu.

Schreibt Wochenziele (TARGET) pro Sportart und Notizen (NOTE) mit Phasen, Wochenstruktur,
Schlüsseleinheiten und Kontrollregeln in den Kalender.

Grundlagen (aus intervals.icu, Strava-Import ab 2020 und Angaben des Athleten):
* Mehrjährige Radsport-Basis auf hohem Niveau: 2020-2022 je 6-9 h/Woche im Schnitt, Spitzenwochen
  bis 22 h, CTL-Maximum 74 (Juli 2021). 2023-2025 fast Pause, 2026 Wiedereinstieg als Triathlet
  (CTL bis 40, jetzt ca. 26).
* Verfügbar: bis zu 20 h pro Woche. Das ist die Obergrenze für Spitzenblöcke, kein Ziel: geplant
  wird nach Anpassungsfähigkeit (CTL-Anstieg höchstens ~4 pro Woche), nicht nach freier Zeit.
* Engpässe: Laufen (bis 2026 kaum Läufe) und Schwimmen -> Lauf-Load steigt nur ~10 % pro Woche,
  Schwimmen ist durch das Vereinstraining (Di/Do je 70 min) fest vorgegeben und wächst in Stufen.
* Hauptwettkampf: DM Kurzdistanz, 08.08.2027 (1,5 km / 40 km / 10 km, geschätzt ca. 2:30 h, ca. 210 TSS).
  Zweiwöchiger Taper, Form am Renntag +15 bis +20 bei CTL ~84.
"""

from __future__ import annotations

from datetime import date, timedelta

# (Montag, TSS gesamt pro Woche, Erholungs-/Taperwoche?)  – 3 Belastungswochen : 1 Erholungswoche
WOCHEN: list[tuple[str, int, bool]] = [
    # Phase 0 Wiedereinstieg und Tests
    ("2026-11-16", 330, False), ("2026-11-23", 240, True),
    # Phase 1 Grundlage I
    ("2026-11-30", 380, False), ("2026-12-07", 405, False), ("2026-12-14", 430, False),
    ("2026-12-21", 300, True),
    ("2026-12-28", 445, False), ("2027-01-04", 475, False), ("2027-01-11", 505, False),
    ("2027-01-18", 340, True),
    # Phase 2 Grundlage II / Aufbau
    ("2027-01-25", 515, False), ("2027-02-01", 535, False), ("2027-02-08", 555, False),
    ("2027-02-15", 370, True),
    ("2027-02-22", 560, False), ("2027-03-01", 580, False), ("2027-03-08", 600, False),
    ("2027-03-15", 400, True),
    # Phase 3 Aufbau intensiv
    ("2027-03-22", 605, False), ("2027-03-29", 630, False), ("2027-04-05", 655, False),
    ("2027-04-12", 430, True),
    ("2027-04-19", 655, False), ("2027-04-26", 680, False), ("2027-05-03", 700, False),
    ("2027-05-10", 460, True),
    # Phase 4 Wettkampfvorbereitung (zwei Spitzenblöcke, 17-18 h)
    ("2027-05-17", 700, False), ("2027-05-24", 715, False), ("2027-05-31", 725, False),
    ("2027-06-07", 470, True),
    ("2027-06-14", 715, False), ("2027-06-21", 725, False), ("2027-06-28", 730, False),
    ("2027-07-05", 480, True),
    ("2027-07-12", 680, False), ("2027-07-19", 620, False),
    # Taper: Woche -2 ca. -20 %, Rennwoche 550 = ca. 340 Vorbereitung + ca. 210 Rennen, danach locker
    ("2027-07-26", 580, True), ("2027-08-02", 550, True), ("2027-08-09", 160, True),
]

RENNTAG = "2027-08-08"
TAPER_WOCHEN = {"2027-07-26", "2027-08-02", "2027-08-09"}  # keine "Erholungswoche"-Notiz

# Schwimmen und Kraft sind feste Größen (Vereinstraining, Krafttraining), der Rest geht an Rad/Lauf.
# Stufen: (gilt ab Datum, Belastungswoche); Erholungswochen = 70 % davon.
_SCHWIMMEN = [("2026-11-16", 110), ("2027-01-01", 130), ("2027-03-01", 150), ("2027-05-01", 170)]
_KRAFT = [("2026-11-16", 40), ("2027-04-01", 30)]
_TAPER_SCHWIMMEN = {"2027-07-26": 130, "2027-08-02": 70, "2027-08-09": 30}  # Rennwoche inkl. Renn-Schwimmen
_TAPER_KRAFT = {"2027-07-26": 20, "2027-08-02": 10, "2027-08-09": 0}
# Lauf-Anteil vom Rest (Rad + Lauf): Laufen ist der Engpass und wächst langsam
_LAUF_ANTEIL = [("2026-11-16", 0.33), ("2027-03-01", 0.35), ("2027-05-01", 0.36)]
# geschätzte TSS pro Stunde (konservativ) für die Stundenschätzung
TSS_PRO_STUNDE = {"Ride": 38, "Run": 52, "Swim": 48, "Other": 22}

ERHOLUNG_TEXT = ("Fokus auf leichtere Belastungen, reduziertes Volumen und Anpassung des Körpers an "
                 "Trainingsstress (Radfahren, Laufen, Schwimmen, Andere). Intensität behalten, "
                 "Umfang -35 %: je eine kurze Qualitätseinheit pro Sportart, kein langer Tag.")

WOCHENSTRUKTUR = (
    "Vorschlag für die Standardwoche (3 Schlüsseleinheiten, Rest locker; Schwimmen Di/Do = Vereinstraining):\n"
    "Mo: Rad locker 60-90 min (Z1-Z2), Kraft\n"
    "Di: Schwimmen (Verein) + SCHLÜSSEL Lauf (Tempo/Intervalle)\n"
    "Mi: SCHLÜSSEL Rad (Schwelle/VO2max) 90-120 min + Lauf locker 30-40 min abends\n"
    "Do: Schwimmen (Verein) + Rad Z2/Kadenz 60-90 min\n"
    "Fr: Sportunterricht/Lauf locker, Kraft (ab Mai nur noch 1x pro Woche)\n"
    "Sa: SCHLÜSSEL langes Rad 3-5 h (ab März mit Koppellauf 20-30 min)\n"
    "So: langer Lauf 75-100 min, optional Schwimmen frei 45 min\n"
    "Ein voller Ruhetag oder maximal locker pro Woche. Nie zwei harte Tage hintereinander in derselben "
    "Sportart, nach der Erholungswoche erst am 2. Tag wieder hart.")

KONTROLLE = (
    "Regeln, die der Plan überwacht:\n"
    "- CTL-Anstieg höchstens ca. 4 pro Woche, Belastungsverhältnis (7 Tage zu Normalwoche) zwischen 0,8 und 1,3.\n"
    "- Lauf-Load wächst höchstens ca. 10-12 % pro Woche; bei Schmerzen im Schienbein/Achilles/Knie "
    "sofort Lauf ersetzen (Rad/Aquajogging).\n"
    "- Ampel (HRV, Ruhepuls, Schlaf, Form): Gelb = Umfang -15 %, Rot = Intensität streichen. HRV 7-Tage-Mittel "
    "unter ca. 78 oder Ruhepuls über ca. 51 sind deine Gelb-Schwellen.\n"
    "- Schlaf mindestens 8 h in Belastungswochen, Verpflegung (60-90 g Kohlenhydrate/h "
    "bei Einheiten über 2 h) mit trainieren.\n"
    "- FTP, Laufschwelle, CSS (Schwimmen) nach jedem Test in intervals.icu aktualisieren, sonst stimmen "
    "TSS und Zonen nicht.")

# (Samstag, Name, Beschreibung) – Tests/Formchecks ausgeruht in der Erholungswoche
RETESTS = [
    ("2027-01-23", "Retest Stufentests",
     "Rad-Stufentest und Lauf-Stufentest wiederholen (ausgeruht, in der Erholungswoche). "
     "Dazu Schwimmtest CSS: 400 m und 200 m maximal, 10 min Pause dazwischen. Danach FTP, "
     "Laufschwelle, CSS, LTHR und Zonen in intervals.icu aktualisieren."),
    ("2027-03-20", "Retest Stufentests",
     "Zweiter Retest: Rad-Stufentest, Lauf-Stufentest, CSS-Test. Vergleich mit November und "
     "Januar zeigt, ob Aufbau und Zonen passen."),
    ("2027-05-22", "Standortbestimmung B-Rennen",
     "Empfehlung: ein Sprint- oder Kurzdistanz-Triathlon oder Duathlon in dieser Woche als "
     "Generalprobe für Wechsel, Pacing und Verpflegung. Danach Wochenload ca. -10 %. Termin bitte "
     "eintragen, dann plane ich ihn mit Mini-Taper ein."),
    ("2027-06-12", "Formcheck Renntempo",
     "In der Erholungswoche: 20-min-Radtest (FTP kontrollieren) und 5-km-Lauf auf Zeit. Daraus "
     "Renntempo ableiten: Rad ca. 85-90 % FTP über 40 km, Lauf etwa 10-km-Pace."),
    ("2027-07-10", "Generalprobe Kurzdistanz",
     "In der Erholungswoche: Koppel 30 km Rad im Renntempo + 5 km Lauf im Renntempo, "
     "Verpflegung und Wechsel üben, 1,5 km Freiwasser mit Neopren."),
]

# (Montag, Name, Beschreibung)
PHASEN: list[tuple[str, str, str]] = [
    ("2026-11-16", "Phase 0: Wiedereinstieg und Tests (bis 29.11.)",
     "Ziel: nach Krankheit/Off-Season wieder Normalbetrieb, Schwellenwerte ermitteln "
     "(Rad-Stufentest 14.11., Lauf-Stufentest 17.11.). Load 240-330 pro Woche.\n"
     "Erwartung: CTL 26 -> ca. 31, Form -7 bis -15. HRV (~90) und Ruhepuls (~47) bleiben auf "
     "deiner Basis, Schlaf ~8 h. Danach FTP, LTHR und Zonen aus den Tests übernehmen."),
    ("2026-11-30", "Phase 1: Grundlage I (30.11.-24.01.)",
     "Intensitätsverteilung ca. 85 % Z1-Z2, 15 % darüber. Rad: lange Z2-Fahrt (Sa 3-4 h), eine "
     "Sweet-Spot-Einheit 2x20 min bei 88-93 % FTP, Kraftausdauer 4x8 min bei 50-60 U/min. "
     "Lauf: 4 Läufe, ein langer Lauf 60-75 min, Steigerungsläufe 6x20 s, Lauf-ABC. Schwimmen: "
     "Vereinstraining plus Technik. Kraft 2x pro Woche (Beine/Core, schwer: Kniebeuge, "
     "Kreuzheben, einbeinig). Load 380 -> 505, ca. 9 -> 13 h.\n"
     "Deine Radbasis aus 2020-2022 kommt schnell zurück, Engpässe sind Laufen und Schwimmen.\n"
     "Erwartung: CTL 31 -> ca. 52 (+3 pro Woche), Form -13 bis -18 in Belastungswochen, "
     "-4 bis 0 in Erholungswochen. In der 3. Belastungswoche sind HRV 5-10 % unter Basis und "
     "Ruhepuls +1-3 bpm normal."),
    ("2026-11-30", "Wochenstruktur und Kontrolle", WOCHENSTRUKTUR + "\n\n" + KONTROLLE),
    ("2027-01-25", "Phase 2: Grundlage II / Aufbau (25.01.-21.03.)",
     "Intensität steigt (pyramidal ca. 80/15/5). Rad: Schwelle 3x15 oder 2x20 min bei 95-100 % "
     "FTP, Over-Unders 3x(2x6 min bei 95/105 %), Z2 lang. Lauf: Tempoläufe 2x15-20 min an der "
     "Schwellenpace, Bergläufe 8x60 s. Schwimmen: CSS-Sätze 10x100 m. Kraft 2x, später "
     "Erhalt. Load 515 -> 600, ca. 13 -> 15 h.\n"
     "Erwartung: CTL 52 -> ca. 69, Form -14 bis -17. Ruhepuls im Wochenmittel +1-2 bpm in "
     "Belastungswochen."),
    ("2027-03-22", "Phase 3: Aufbau intensiv (22.03.-09.05.)",
     "VO2max: Rad 5x4-5 min bei 110-120 % FTP (Pause gleich lang) oder 30/30; Lauf 6x1 km bei "
     "3-5-km-Tempo; Schwimmen 8x200 m bei CSS. Einmal pro Woche Koppeltraining (60-90 min Rad "
     "Sweet Spot + 15-20 min Lauf im Renntempo), Samstag 4-5 h Z2 mit 2x30 min Tempo. "
     "Load 605 -> 700, ca. 15 -> 17 h.\n"
     "Erwartung: CTL 69 -> ca. 83, Form -10 bis -14. Mehr Intensität heißt stärkere Reaktion: "
     "nach harten Tagen HRV 10-15 % niedriger ist normal und sollte nach 48 h zurück sein. "
     "Ab hier die Ampel (Gelb/Rot) strikt befolgen."),
    ("2027-05-17", "Phase 4: Wettkampfvorbereitung (17.05.-25.07.)",
     "Kurzdistanz-spezifisch (1,5 km / 40 km / 10 km, ca. 2:30 h): Renntempo-Blöcke Rad 3x12 min "
     "bei 100-105 % FTP, Brick Rad 40 min bei 85-90 % FTP + Lauf 10 km im Renntempo (alle 2 Wochen), "
     "Freiwasser mit Neopren ab Mai, 1,5 km am Stück, lange Radfahrt bis 4 h, langer Lauf bis 100 min. "
     "Zwei Spitzenblöcke zu 3 Wochen (700-730 TSS, ca. 17-18 h; bei grüner Ampel einzelne Wochen bis 20 h), "
     "Erholungswochen am 07.06. und 05.07.; Wochen 12. und 19.07. leicht abfallend.\n"
     "Erwartung: CTL 83 -> ca. 93 Ende Juni (dein bisheriges Maximum war 74 im Jahr 2021), Form -10 bis "
     "-14 in Blöcken. Die Zahlen hängen an einer korrekten FTP-Einstellung."),
    ("2027-07-26", "Taper und Höchstform (26.07.-08.08.)",
     "Woche -2 (26.07.): Volumen ca. -20 % (580), Intensität unverändert. Rennwoche: ca. 340 TSS "
     "Vorbereitung plus Rennen (ca. 200-220 TSS), Wochenziel 550 enthält das Rennen. Mo/Di "
     "je 1 Qualitätsreiz (3-5 Reize à 3-5 min im Renntempo), Mi/Do locker mit 3x30 s Öffnern, Fr "
     "frei, Sa 20 min Öffnungsrunde. Letzte schwere Kraft 14 Tage vorher, nichts Neues "
     "ausprobieren, Schlaf 8-9 h, Kohlenhydrate ab 2 Tage vorher erhöhen.\n"
     "Erwartung: CTL sinkt von ca. 93 auf ca. 84, ATL fällt auf ca. 66, Form am Renntag ca. +19 "
     "(Ziel +15 bis +20), HRV über Basis (90 oder mehr), Ruhepuls an oder unter Basis (46-47). "
     "Liegt in der Rennwoche die HRV unter ca. 78 oder der Ruhepuls über ca. 51: Intensität weglassen, "
     "nur locker aktivieren."),
    ("2027-08-09", "Nach dem Wettkampf (ab 09.08.)",
     "Eine Woche locker (Load ca. 160), danach entscheiden: Spätsaison mit kurzem Aufbau oder "
     "direkt Off-Season (2-4 Wochen aktive Pause, Load unter 150).\n"
     "Erwartung: Form bleibt erst hoch (+15 bis +25), CTL fällt in der Pause auf ca. 40-50. "
     "Beim Wiedereinstieg die Wochenload über 3-4 Wochen auf die Normalwoche anheben."),
]


def _stufe(stufen: list, tag: str):
    wert = stufen[0][1]
    for ab, w in stufen:
        if tag >= ab:
            wert = w
    return wert


def verteilung(gesamt: int, tag: str = "2026-11-16", erholung: bool = False) -> dict[str, int]:
    """Wochenload auf Sportarten verteilen: Schwimmen und Kraft fest, Rest an Rad und Lauf."""
    if tag in _TAPER_SCHWIMMEN:
        swim, kraft, anteil = _TAPER_SCHWIMMEN[tag], _TAPER_KRAFT[tag], 0.33
    else:
        faktor = 0.7 if erholung else 1.0
        swim = round(_stufe(_SCHWIMMEN, tag) * faktor)
        kraft = round(_stufe(_KRAFT, tag) * (0.5 if erholung else 1.0))
        anteil = _stufe(_LAUF_ANTEIL, tag)
    rest = max(gesamt - swim - kraft, 0)
    lauf = round(rest * anteil)
    return {"Ride": rest - lauf, "Run": lauf, "Swim": swim, "Other": kraft}


def stunden(gesamt: int, tag: str, erholung: bool = False) -> float:
    """Grobe Stundenschätzung der Woche aus den Sportart-Zielen."""
    return sum(load / TSS_PRO_STUNDE[sport] for sport, load in verteilung(gesamt, tag, erholung).items())


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
    """Phasen-, Erholungswochen- und Test-Notizen; Erholungswochen an Tagen mit Notiz entfallen."""
    out = []
    for tag, name, text in PHASEN:
        out.append((montag(tag), name, text))
    for tag, _, erholung in WOCHEN:
        if erholung and tag not in TAPER_WOCHEN:
            out.append((montag(tag), "Erholungswoche", ERHOLUNG_TEXT))
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
