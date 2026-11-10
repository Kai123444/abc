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
* Hauptwettkampf: DM Kurzdistanz, 08.08.2027 (1,5 km / 40 km / 10 km; eine Kurzdistanz im Juni 2026 dauerte 2:19 h bei ca. 145 TSS, für die DM
  rechne ich mit ca. 170 TSS).
  Zweiwöchiger Taper, Form am Renntag +15 bis +20 bei CTL ~86.
"""

from __future__ import annotations

from datetime import date, timedelta

# (Montag, TSS gesamt pro Woche, Erholungs-/Taperwoche?)  – 3 Belastungswochen : 1 Erholungswoche
WOCHEN: list[tuple[str, int, bool]] = [
    # Phase 0 Wiedereinstieg und Tests (Woche 09.11. mit Rad-Stufentest, Woche 16.11. mit Lauf-Stufentest)
    ("2026-11-09", 411, False), ("2026-11-16", 304, False), ("2026-11-23", 240, True),
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
    # Phase 4 Wettkampfvorbereitung (zwei Spitzenblöcke, 18-19 h, Spitzenwochen bis ~21 h möglich)
    ("2027-05-17", 710, False), ("2027-05-24", 730, False), ("2027-05-31", 745, False),
    ("2027-06-07", 480, True),
    ("2027-06-14", 735, False), ("2027-06-21", 750, False), ("2027-06-28", 760, False),
    ("2027-07-05", 490, True),
    ("2027-07-12", 695, False), ("2027-07-19", 635, False),
    # Taper: Woche -2 ca. -20 %, Rennwoche 520 = ca. 345 Vorbereitung + ca. 170 Rennen, danach locker
    ("2027-07-26", 600, True), ("2027-08-02", 520, True), ("2027-08-09", 160, True),
    # Spätsaison: Mitteldistanz-Schlüsselwoche, Hölle von Q (Mitteldistanz, B-Rennen, So 05.09.)
    ("2027-08-16", 400, True), ("2027-08-23", 560, True), ("2027-08-30", 540, True),
]

RENNTAG = "2027-08-08"
TAPER_WOCHEN = {"2027-07-26", "2027-08-02", "2027-08-09", "2027-08-16", "2027-08-23", "2027-08-30"}  # Sonderwochen

# Schwimmen und Kraft sind feste Größen (Vereinstraining, Krafttraining), der Rest geht an Rad/Lauf.
# Stufen: (gilt ab Datum, Belastungswoche); Erholungswochen = 70 % davon.
_SCHWIMMEN = [("2026-11-16", 110), ("2027-01-01", 130), ("2027-03-01", 150), ("2027-05-01", 170)]
_KRAFT = [("2026-11-16", 40), ("2027-04-01", 30)]
_TAPER_SCHWIMMEN = {"2027-07-26": 130, "2027-08-02": 70, "2027-08-09": 30,  # Rennwoche inkl. Renn-Schwimmen
                    "2027-08-16": 100, "2027-08-23": 120, "2027-08-30": 90}
_TAPER_KRAFT = {"2027-07-26": 20, "2027-08-02": 10, "2027-08-09": 0, "2027-08-16": 20, "2027-08-23": 30, "2027-08-30": 10}
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
     "Freiwasser mit Neopren ab Mai, 1,5 km am Stück, lange Radfahrt bis 4-5 h, langer Lauf bis 100 min. "
     "Sa 12.06. Cottbus (Olympische Distanz = B-Rennen und Generalprobe für die DM, Mini-Taper Mi-Fr, "
     "ersetzt den Formcheck). Weitere Rennen vor der DM nach Termin: Supersprint/Sprint ersetzt die "
     "Samstags-Brick-Einheit. "
     "Zwei Spitzenblöcke zu 3 Wochen (710-760 TSS, ca. 18-19 h). Spitzenwochen dürfen 20-21 h "
     "erreichen, wenn der Mehrumfang locker ist (Z1-Z2, zusätzliches Rad/Schwimmen) und die Ampel grün "
     "bleibt. Erholungswochen am 07.06. und 05.07.; die Wochen 12. und 19.07. fallen leicht ab.\n"
     "Erwartung: CTL 83 -> ca. 95 Ende Juni (dein bisheriges Maximum war 74 im Jahr 2021), Form -10 bis "
     "-14 in Blöcken. Die Zahlen hängen an einer korrekten FTP-Einstellung."),
    ("2027-07-26", "Taper und Höchstform (26.07.-08.08.)",
     "Woche -2 (26.07.): Volumen ca. -20 % (600), Intensität unverändert. Rennwoche: ca. 345 TSS "
     "Vorbereitung plus Rennen (ca. 150-180 TSS), Wochenziel 520 enthält das Rennen. Mo/Di "
     "je 1 Qualitätsreiz (3-5 Reize à 3-5 min im Renntempo), Mi/Do locker mit 3x30 s Öffnern, Fr "
     "frei, Sa 20 min Öffnungsrunde. Letzte schwere Kraft 14 Tage vorher, nichts Neues "
     "ausprobieren, Schlaf 8-9 h, Kohlenhydrate ab 2 Tage vorher erhöhen.\n"
     "Erwartung: CTL sinkt von ca. 95 auf ca. 86, ATL fällt auf ca. 67, Form am Renntag ca. +20 "
     "(Ziel +15 bis +20), HRV über Basis (90 oder mehr), Ruhepuls an oder unter Basis (46-47). "
     "Liegt in der Rennwoche die HRV unter ca. 78 oder der Ruhepuls über ca. 51: Intensität weglassen, "
     "nur locker aktivieren."),
    ("2027-08-09", "Nach dem Wettkampf und Spätsaison (ab 09.08.)",
     "Woche 09.08. locker (Load ca. 160). Danach kurze Spätsaison mit einem Ziel: Hölle von Q, "
     "Mitteldistanz im Harz, B-Rennen am So 05.09. Weitere Rennen in dieser Zeit nur nach Absprache, "
     "ein Sprint zwei Wochen vor der Hölle von Q geht als Trainingsrennen ohne Taper. Danach Off-Season (2-4 Wochen aktive Pause, Load unter 150).\n"
     "Erwartung: Form bleibt nach der DM hoch (+10 bis +20), CTL fällt in der Spätsaison von ca. 86 "
     "auf ca. 78 und bleibt dort. Beim Wiedereinstieg im Herbst die Wochenload über 3-4 Wochen auf "
     "die Normalwoche anheben."),
    ("2027-08-23", "Hölle von Q: Mitteldistanz (B-Rennen, 05.09.)",
     "Mitteldistanz im Harz (laut deinem Kalender 2 km Schwimmen / 90 km Rad / 10 km Lauf, Rennzeit "
     "geschätzt 4:15-5:15 h, Rennlast ca. 300-350 TSS; bei Halbmarathon-Lauf ca. +60). Anders als die "
     "Kurzdistanz: Pacing und Verpflegung entscheiden.\n"
     "Schlüsselwoche 23.08. (560): Sa Brick 100 km Rad bei 70-78 % FTP + 10-14 km Lauf, Neopren-"
     "Schwimmen 2 km am Stück, langer Lauf 16-18 km, Verpflegung 80-90 g Kohlenhydrate pro Stunde "
     "üben. Rennwoche 30.08. (540 mit Rennen): Mo 60-70 min mit 3x10 min Renntempo, Di Schwimmen "
     "1.500 m, Mi locker, Do 20 min mit Öffnern, Fr frei, Sa 30 min Öffnerrunde und Material.\n"
     "Rennplan: Rad nicht über 75 % FTP (IF höchstens 0,75), Laufen die ersten 5 km bewusst zurückhaltend, "
     "bei Hitze Natrium dazu. Erwartung: Form am Renntag ca. +3 bis +8 (kurzer Taper, B-Rennen), das "
     "reicht für ein starkes Rennen."),
]


# Testwochen: Verteilung nach den tatsächlich geplanten Einheiten (Stufentests, Vereinstraining, Sportunterricht)
_SPORT_FEST = {
    "2026-11-09": {"Ride": 167, "Run": 55, "Swim": 157, "Other": 32},  # 24-h-Schwimmen Fr/Sa, Rad-Test So
    "2026-11-16": {"Ride": 87, "Run": 100, "Swim": 102, "Other": 15},  # Lauf-Stufentest Mi
}


def _stufe(stufen: list, tag: str):
    wert = stufen[0][1]
    for ab, w in stufen:
        if tag >= ab:
            wert = w
    return wert


def verteilung(gesamt: int, tag: str = "2026-11-16", erholung: bool = False) -> dict[str, int]:
    """Wochenload auf Sportarten verteilen: Schwimmen und Kraft fest, Rest an Rad und Lauf."""
    if tag in _SPORT_FEST:
        return dict(_SPORT_FEST[tag])
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


# ---------------------------------------------------------------------------------------------
# Übersicht: welche Belastungsart wann
# ---------------------------------------------------------------------------------------------
RENNWOCHE_VORBEREITUNG = [80, 100, 50, 70, 0, 40]  # Mo-Sa vor dem Rennen (ohne Rennen)
RENNTAG_TSS = 170

# (von, bis, Phase, Belastungsart, Intensitätsverteilung, Rad, Lauf, Schwimmen/Kraft)
PHASEN_UEBERSICHT = [
    ("2026-11-09", "2026-11-29", "0 Wiedereinstieg und Tests", "Reaktivierung, Leistungsdiagnostik",
     "locker, Tests Sa 14.11./Di 17.11.", "Stufentest, Z2", "Stufentest, locker", "Verein, Kraft-Technik"),
    ("2026-11-30", "2027-01-24", "1 Grundlage I", "Aerobes Volumen, Kraftausdauer, Technik",
     "ca. 85 % Z1-Z2 / 15 % darüber", "Z2 lang (Sa 3-4 h), Sweet Spot 2x20, Kraftausdauer 4x8 min",
     "4 Läufe, langer Lauf 60-75 min, Steigerungen, Lauf-ABC", "Verein + Technik; Kraft 2x schwer"),
    ("2027-01-25", "2027-03-21", "2 Grundlage II / Aufbau", "Schwelle, Tempo, aerobe Leistung",
     "ca. 80 / 15 / 5 (pyramidal)", "Schwelle 3x15 / 2x20, Over-Unders, Z2 lang",
     "Tempoläufe 2x15-20 min, Berge 8x60 s", "CSS-Sätze 10x100; Kraft 2x, später Erhalt"),
    ("2027-03-22", "2027-05-16", "3 Aufbau intensiv", "VO2max, Koppeltraining, lange Ausdauer",
     "ca. 75 / 15 / 10", "VO2max 5x4-5 min, 30/30, Sa 4-5 h mit 2x30 Tempo, Koppel 1x/Woche",
     "6x1 km (3-5-km-Tempo), Koppellauf 15-20 min", "8x200 bei CSS; Kraft 1x Erhalt"),
    ("2027-05-17", "2027-07-25", "4 Wettkampfvorbereitung", "Renntempo, Spezifik, Spitzenvolumen",
     "ca. 75 / 15 / 10 mit Renntempo", "3x12 min bei 100-105 % FTP, Brick 40 min bei 85-90 % FTP + 10-km-Lauf",
     "Langer Lauf bis 100 min, Brick-Lauf 10 km Renntempo", "Freiwasser mit Neopren, 1,5 km am Stück; Kraft 1x"),
    ("2027-07-26", "2027-08-08", "Taper und Rennen", "Frische, Schärfe, Renntempo-Öffner",
     "locker + wenige scharfe Reize", "3-5 Reize à 3-5 min im Renntempo, Öffner", "kurze Tempoläufe, Öffner",
     "locker, Technik; letzte schwere Kraft 14 Tage vorher"),
    ("2027-08-09", "2027-09-05", "Spätsaison", "Regeneration, dann Hölle von Q",
     "locker, wenige scharfe Reize", "locker, 1-2 Renntempo-Blöcke", "locker, Brick vor Hölle von Q", "locker, Technik"),
]

_TESTWOCHEN = {"2027-01-18": "Retest Sa 23.01.", "2027-03-15": "Retest Sa 20.03.",
               "2027-06-07": "Cottbus Olympische Distanz Sa 12.06.", "2027-07-05": "Generalprobe Sa 10.07.",
               "2027-08-23": "Mitteldistanz-Schlüsselwoche (Brick 100 km + 10-14 km)",
               "2027-08-30": "Hölle von Q (Mitteldistanz, B) So 05.09."}


def phase_fuer(tag: str) -> tuple:
    for ph in PHASEN_UEBERSICHT:
        if ph[0] <= tag <= ph[1]:
            return ph
    return PHASEN_UEBERSICHT[-1]


def simulation() -> dict[str, tuple[float, float]]:
    """CTL/ATL am Ende jeder Woche (Startwerte 16.11.: CTL 28, ATL 43; Last gleichmäßig verteilt)."""
    from math import exp
    kc, ka = 1 - exp(-1 / 42), 1 - exp(-1 / 7)
    ctl, atl = 28.0, 43.0
    out = {}
    for tag, tss, _ in WOCHEN:
        if tag < "2026-11-16":  # Startwerte gelten für den 16.11.
            continue
        if tag == "2027-08-02":
            for d in RENNWOCHE_VORBEREITUNG:
                ctl += (d - ctl) * kc
                atl += (d - atl) * ka
            out["renntag"] = (ctl, atl)
            ctl += (RENNTAG_TSS - ctl) * kc  # Rennen am Sonntag
            atl += (RENNTAG_TSS - atl) * ka
            out[tag] = (ctl, atl)
            continue
        for _ in range(7):
            ctl += (tss / 7 - ctl) * kc
            atl += (tss / 7 - atl) * ka
        out[tag] = (ctl, atl)
    return out


def uebersicht_markdown() -> str:
    sim = simulation()
    z = ["# Saisonübersicht bis zur DM Kurzdistanz (08.08.2027)", "",
         "Wochenziele in TSS, Stunden grob geschätzt (Rad 38, Lauf 52, Schwimmen 48, Kraft 22 TSS/h). "
         "CTL/Form am Wochenende laut Simulation; sie stimmen nur bei korrekter FTP-Einstellung.", "",
         "## Phasen im Überblick", "",
         "| Phase | Zeitraum | Belastungsart | Intensitätsverteilung | Load/Woche (ohne Erholung) | Stunden | CTL am Ende |",
         "|---|---|---|---|---|---|---|"]
    for von, bis, name, art, vert, *_ in PHASEN_UEBERSICHT:
        wk = [(t, l, r) for t, l, r in WOCHEN if von <= t <= bis]
        if not wk:
            continue
        mit_sim = [t for t, _, _ in wk if t in sim]
        ctl_ende = f"{sim[mit_sim[-1]][0]:.0f}" if mit_sim else "-"
        voll = [(t, l, r) for t, l, r in wk if not r] or wk  # Belastungswochen, sonst alle
        lo, hi = min(l for _, l, _ in voll), max(l for _, l, _ in voll)
        load = f"{lo}-{hi}" if lo != hi else f"{lo}"
        std = [stunden(l, t, r) for t, l, r in voll]
        z.append(f"| {name} | {date.fromisoformat(von):%d.%m.}-{date.fromisoformat(bis):%d.%m.%Y} | {art} | {vert} | "
                 f"{load} | {min(std):.0f}-{max(std):.0f} | {ctl_ende} |")
    z += ["", "## Schlüsseleinheiten pro Phase", "",
          "| Phase | Rad | Lauf | Schwimmen / Kraft |", "|---|---|---|---|"]
    for _, _, name, _, _, rad, lauf, swim in PHASEN_UEBERSICHT:
        z.append(f"| {name} | {rad} | {lauf} | {swim} |")
    z += ["", "## Woche für Woche", "",
          "| Woche ab | Phase | Art | TSS | Std. | Rad | Lauf | Schw. | Kraft | CTL | Form |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for tag, tss, rec in WOCHEN:
        ph = phase_fuer(tag)
        v = verteilung(tss, tag, rec)
        art = "Erholung" if rec and tag not in TAPER_WOCHEN else ph[3].split(",")[0]
        if tag == "2027-07-26":
            art = "Taper (-20 %)"
        elif tag == "2027-08-02":
            art = "Rennwoche DM (Rennen So 08.08., Werte nach dem Rennen)"
        elif tag == "2027-08-09":
            art = "Regeneration"
        elif tag in ("2027-08-16", "2027-08-23", "2027-08-30"):
            art = "Spätsaison"
        if tag in _TESTWOCHEN:
            art += f" + {_TESTWOCHEN[tag]}"
        if tag in sim:
            c, a = sim[tag]
            cf = f"{c:.0f} | {c - a:+.0f}"
        else:
            cf = "- | -"
        z.append(f"| {date.fromisoformat(tag):%d.%m.} | {ph[2].split(' ', 1)[0]} | {art} | {tss} | "
                 f"{stunden(tss, tag, rec):.0f} | {v['Ride']} | {v['Run']} | {v['Swim']} | {v['Other']} | {cf} |")
    z += ["", "## Rennkalender 2027", "", "| Datum | Rennen | Distanz | Rolle | Rennlast | Vorbereitung |",
          "|---|---|---|---|---|---|",
          "| **08.08.** | **DM Kurzdistanz** | Kurzdistanz | **A** | ~170 TSS | Taper 2 Wochen, siehe Notiz |",
          "| **05.09.** | **Hölle von Q (Harz)** | Mitteldistanz: 2 km / 90 km / 10 km laut Eintrag | **B** | "
          "~300-350 TSS | Schlüsselwoche 23.08., Rennwoche 30.08. mit kurzem Taper, Rad nicht über 75 % FTP |"]
    for tag, name, klasse, kat, dist, tss, hinweis in RENNEN:
        z.append(f"| {date.fromisoformat(tag):%d.%m.} | {name} | {klasse} ({dist}) | {kat[-1]} | ~{tss} TSS | {hinweis} |")
    c, a = sim["renntag"]
    z += ["", f"Renntag 08.08.2027 (Prognose am Morgen): CTL {c:.0f}, ATL {a:.0f}, Form {c - a:+.0f}.", ""]
    return "\n".join(z)


# ---------------------------------------------------------------------------------------------
# Rennkalender 2027: zusätzliche Rennen (nur eintragen, wenn der Termin feststeht).
# (Datum, Name, Klasse, Kategorie, Distanzen, geschätzte TSS, Vorbereitung/Hinweis)
# Messwerte der Vorjahresrennen (Regionalliga-Termine 2026, intervals.icu) als Orientierung für die Rennlast:
#   Supersprint ca. 40 TSS, Sprint ca. 80-90 TSS, Kurzdistanz (1,4 km / 42 km / 10 km) ca. 145 TSS in 2:19 h.
RENNEN: list[tuple[str, str, str, str, str, int, str]] = [
    ("2027-06-12", "Cottbus", "Olympische Distanz", "RACE_B",
     "Schwimmen 1,5 km / Rad 40 km / Lauf 10 km (Vergleich: Kurzdistanz im Juni 2026 in 2:19 h)", 150,
     "B-Rennen und Generalprobe für die DM, 8 Wochen vorher. Mini-Taper Mi-Fr (-40 %): Mo 60 min locker, "
     "Di Schwimmen (Verein) + 5x1 min Renntempo Lauf, Mi 45 min Rad mit 3x5 min Renntempo, Do Schwimmen "
     "Technik, Fr 30 min locker mit 3x30 s Öffnern. Pacing, Wechsel und Verpflegung wie bei der DM üben. "
     "So locker 60 min oder frei, Mo locker, ab Di wieder Belastung. Ersetzt den Formcheck."),
]


def rennen_events() -> list[dict]:
    """Rennen des Vorjahres als Platzhalter-Termine (RACE_B/RACE_C) im Kalender."""
    out = []
    for tag, name, klasse, kat, dist, tss, hinweis in RENNEN:
        d = date.fromisoformat(tag)
        out.append({"category": kat, "type": "Other", "name": f"{name} ({klasse})",
                    "start_date_local": f"{tag}T00:00:00",
                    "description": (f"{klasse}: {dist}. Geschätzte Rennlast ca. {tss} TSS.\n{hinweis}\n"
                                    "Termin und Distanz laut Athlet."),
                    "external_id": f"saison-rennen-{tag}-{name[:5].lower().strip()}"})
    return out
