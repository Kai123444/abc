"""Saisonplanung 2026/27 bis zur DM Kurzdistanz (So 08.08.2027) für intervals.icu.

Schreibt Wochenziele (TARGET) pro Sportart und Notizen (NOTE) mit Phasen, Wochenstruktur,
Schlüsseleinheiten und Kontrollregeln in den Kalender.

Grundlagen (aus intervals.icu, Strava-Import ab 2020 und Angaben des Athleten):
* Mehrjährige Radsport-Basis auf hohem Niveau: 2020-2022 je 6-9 h/Woche im Schnitt, Spitzenwochen
  bis 22 h, CTL-Maximum 74 (Juli 2021). 2023-2025 fast Pause, 2026 Wiedereinstieg als Triathlet
  (CTL bis 40, jetzt ca. 26).
* Verfügbar: bis zu 20 h pro Woche. Das ist die Obergrenze für Spitzenblöcke, kein Ziel: geplant
  wird nach Anpassungsfähigkeit (CTL-Anstieg höchstens ~4,5 pro Woche), nicht nach freier Zeit.
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
    # Phase 0 Tests (Woche 09.11. mit Rad-Stufentest, Woche 16.11. mit Lauf-Stufentest); kein Deload danach,
    # der Wiedereinstieg ist kurz: Belastung steigt ab 23.11. (erster Block 4 Wochen, dann Erholungswoche 21.12.)
    ("2026-11-09", 411, False), ("2026-11-16", 311, False),
    # Phase 1 Grundlage I
    ("2026-11-23", 440, False), ("2026-11-30", 460, False), ("2026-12-07", 480, False), ("2026-12-14", 500, False),
    ("2026-12-21", 330, True),
    ("2026-12-28", 515, False), ("2027-01-04", 535, False), ("2027-01-11", 550, False),
    ("2027-01-18", 370, True),
    # Phase 2 Grundlage II / Aufbau
    ("2027-01-25", 560, False), ("2027-02-01", 580, False), ("2027-02-08", 600, False),
    ("2027-02-15", 400, True),
    ("2027-02-22", 610, False), ("2027-03-01", 625, False), ("2027-03-08", 640, False),
    ("2027-03-15", 430, True),
    # Phase 3 Aufbau intensiv
    ("2027-03-22", 640, False), ("2027-03-29", 660, False), ("2027-04-05", 680, False),
    ("2027-04-12", 450, True),
    ("2027-04-19", 680, False), ("2027-04-26", 700, False), ("2027-05-03", 715, False),
    ("2027-05-10", 470, True),
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

# Schwimmen und Kraft sind feste Größen (Vereinstraining, Kraftraum Mo-Do), der Rest geht an Rad/Lauf.
# Stufen: (gilt ab Datum, Belastungswoche); Erholungswochen = 70 % davon.
_SCHWIMMEN = [("2026-11-16", 85), ("2027-01-01", 100), ("2027-03-01", 115), ("2027-05-01", 125)]  # 2 x Verein = ca. 2,3 h; später dritte Einheit
_KRAFT = [("2026-11-16", 28), ("2027-03-22", 22), ("2027-05-17", 18)]  # Kraftraum: 2x, ab Frühjahr Erhalt
_TAPER_SCHWIMMEN = {"2027-07-26": 130, "2027-08-02": 70, "2027-08-09": 30,  # Rennwoche inkl. Renn-Schwimmen
                    "2027-08-16": 100, "2027-08-23": 120, "2027-08-30": 90}
_TAPER_KRAFT = {"2027-07-26": 20, "2027-08-02": 10, "2027-08-09": 0, "2027-08-16": 20, "2027-08-23": 30, "2027-08-30": 10}
# Lauf-Anteil vom Rest (Rad + Lauf): Laufen ist der Engpass und wächst langsam
_LAUF_ANTEIL = [("2026-11-16", 0.26), ("2027-02-01", 0.27), ("2027-03-01", 0.29), ("2027-04-01", 0.31),
                ("2027-05-01", 0.33), ("2027-05-17", 0.35)]
# geschätzte TSS pro Stunde (konservativ) für die Stundenschätzung
TSS_PRO_STUNDE = {"Ride": 34, "Run": 48, "Swim": 35, "Other": 14}  # aus deinen Aktivitäten seit August gemessen
# Rad: TSS pro Stunde steigt mit dem Intensitätsanteil (Grundlage Z2 ca. 32, später Schwelle/VO2max/Renntempo)
_RAD_TSS_H = [("2026-11-16", 32), ("2027-01-25", 35), ("2027-03-22", 38), ("2027-05-17", 40)]

ERHOLUNG_TEXT = ("Fokus auf leichtere Belastungen, reduziertes Volumen und Anpassung des Körpers an "
                 "Trainingsstress (Radfahren, Laufen, Schwimmen, Andere). Intensität behalten, "
                 "Umfang -35 %: je eine kurze Qualitätseinheit pro Sportart, kein langer Tag.")

WOCHENSTRUKTUR = (
    "Vorschlag für die Standardwoche (Schwimmen Di/Do = Vereinstraining; Kraftraum Mo, Mi und Do; am Wochenende kannst du "
    "vormittags und nachmittags trainieren; Intervalle legst du dorthin, wo sie am besten passen):\n"
    "Mo: KRAFT Beine schwer + Oberkörper (55-60 min), Rad nur locker nach Lust\n"
    "Di: Rad locker/Kadenz 60-90 min (Beine ausdrehen nach Montag), ab Phase 3 alle 2 Wochen Intervalle statt locker, "
    "Schwimmen (Verein)\n"
    "Mi: KRAFT Oberkörper, Core und kurze Beinaktivierung (35-40 min), danach SCHLÜSSEL Lauf = Bahnintervalle "
    "(Einlaufen 3-4 km, 400-1000 m Wiederholungen, Auslaufen; eigene Einheit, bis das Vereinstraining startet)\n"
    "Do: SCHLÜSSEL Rad-Intervalle (Sweet Spot/Schwelle/VO2max/Renntempo) 75-105 min, ab Phase 3 mit Koppellauf 10-15 min (Phase 4: 15-20 min), Schwimmen (Verein), Sauna\n"
    "Do danach: KRAFT Ergänzung Beine/Hüfte/Rumpf 30-35 min nach dem Rad (Phase 1-2; Phase 3 20 min, Phase 4 entfällt), moderat, RIR 3\n"
    "Fr: trainingsfrei (Schule, Sportunterricht zählt nicht als Einheit)\n"
    "Sa vormittags: SCHLÜSSEL langes Rad 3-5 h in Z2 mit einem Intervallblock in der Mitte (siehe Rad-Intervalle), in den "
    "Bergen oder flach, danach kein Lauf (der Sonntag ist der Lauftag)\n"
    "Sa nachmittags: locker, Schwimmen frei 45 min (ab Mai Freiwasser; nicht Sa 21.11.) oder Core 20 min; in Phase 1-2 optional Lauf 30-45 min\n"
    "So vormittags: KOPPEL: erst 60 min Rad locker (Z1-Z2), direkt danach der lange Lauf 60-100 min im Hügelgelände (bergauf "
    "kräftig, bergab kontrolliert). In Phase 3-4 alle 2 Wochen Renn-Brick statt des lockeren Koppels (siehe Notiz Koppeltraining)\n"
    "So nachmittags: frei oder Schwimmen frei 45 min\n"
    "Ein voller Ruhetag oder maximal locker pro Woche (meist Fr). Schwere Beine nur Mo (48 h vor den Mittwochs-Intervallen, "
    "Radsport-Erfahrung trägt das nach dem Wochenende); Mi vor dem Laufen keine schweren Beine. Keine Rad-Intervalle an "
    "zwei Tagen hintereinander (Do und Sa haben den Freitag dazwischen).")

KRAFTPLAN = (
    "Kraftraum Mo, Mi und Do, orientiert an deinen letzten Einheiten (meist montags, 45-60 min). Mo = Ganzkörper mit "
    "schweren Beinen (dein gewohnter Tag). Mi = vor dem Lauftraining nur Oberkörper, Core und eine kurze, nicht "
    "ermüdende Beinaktivierung (35-40 min): so leidet die Qualität der Intervalle nicht. Do = Ergänzung nach dem Rad-Schlüssel (30-35 min, moderat), damit auch bei leichtem oder ausgefallenem Montag genug Krafteinheiten bleiben. Last nach "
    "Wiederholungen in Reserve (RIR) steuern, nicht nach Gewicht: in den ersten 2 Wochen Gewichte finden "
    "(RIR 3-4), danach +2,5 kg, wenn alle Sätze sauber sind.\n"
    "Phase 1 (23.11.-24.01.) Aufbau, 3x8-10, RIR 2-3:\n"
    "- Mo Beine: Kniebeuge (Front oder Goblet) 3x8, Rumänisches Kreuzheben 3x8, Bulgarian Split Squat 3x8 je Seite, "
    "Hip Thrust 3x10, Wadenheben stehend 3x12-15, Tibialis-Raises 2x15. Waden und Hüfte sind die Laufvorsorge. "
    "Danach Oberkörper: Klimmzüge oder Latzug 3x8, Rudern 3x10, Plank 3x45 s.\n"
    "- Mi vor dem Lauf: Bankdrücken oder Kurzhantel 3x8, Schulterdrücken 3x10, Face Pulls 2x15, Pallof Press "
    "2x10 je Seite, Seitstütz 2x30 s, Aktivierung: Glute Bridge 2x10, Wadenheben 2x12, 2x5 leichte Hocksprünge.\n"
    "- Do Ergänzung nach dem Rad (30-35 min, RIR 3): Einbeinige Übungen und Rückseite: Single-Leg RDL 3x8 je Seite, Step-ups 3x8 je Seite, Hip Thrust 3x10, Nordic Hamstring 2x5, Wadenheben 3x12, Core: Dead Bug 3x10, Seitstütz 2x30 s. Nicht bis zum Versagen, kein Muskelkater für den Samstag.\n"
    "Phase 2 (25.01.-21.03.) Maximalkraft, 3-4x4-6 bei 80-87 % 1RM, RIR 1-2:\n"
    "- Mo Beine: Kniebeuge, Trap-Bar- oder Kreuzheben (nie bis zum Versagen), Step-ups schwer 3x6 je Seite, "
    "Nordic Hamstring 2x5, Wadenheben schwer 4x8. Oberkörper kurz (Klimmzüge/Rudern 3x5).\n"
    "- Mi vor dem Lauf: Bankdrücken/Schulterdrücken 3x5, Core, Aktivierung mit Hocksprüngen oder Boxjumps 3x4 "
    "(kurz, volle Pausen, ermüdet nicht und bereitet die Intervalle vor).\n"
    "Phase 3 (22.03.-16.05.) Erhalt und Explosivkraft: Do 20 min Hamstring, Waden und Core nach dem Rad; Mo 35-40 min (Beine 2-3x3-5 bei 85 %, Sprünge 3x5, "
    "Oberkörper kurz), Mi nur 20 min Core und Aktivierung. Die lange Ausfahrt am Samstag läuft in deinen gewohnten Zonen.\n"
    "Phase 4 (17.05.-25.07.): Do entfällt; Mo 35 min (Beine 2x4 bei 85 %, Zug/Rumpf), Mi entfällt oder 15 min Core. In "
    "Erholungswochen aussetzen oder ganz leicht. Letzte Beineinheit 14 Tage vor der DM (25.07.), letzte "
    "Oberkörper/Core-Einheit 7 Tage vorher (01.08.). In der Woche von Cottbus (12.06.) keine schweren Beine.\n"
    "Wichtig: Schwere Beine nur Mo, am Do nur moderate Ergänzung. Beinkraft nie am Dienstag (Tag vor den Intervallen), nie am Tag vor einem Test oder Rennen und nie "
    "mit Muskelkater über 48 h. HRV/Ruhepuls auffällig: Einheit leichter machen, nicht ausfallen lassen.")

LAUFINTERVALLE = (
    "Auswertung deiner Mittwochsläufe in Cottbus (22 Läufe, Juni bis September 2026): Ablauf immer gleich. Gegen "
    "17:00 Einlaufen 3,5-4,9 km locker (6:15-6:50/km, Puls 136-152), ab ca. 17:50 Intervalle auf der Bahn.\n"
    "- 400-m-Wiederholungen bei 3:50-4:05/km (1:32-1:38 pro Runde), die schnellste bei 3:29. 800 m bei 3:54-4:04/km.\n"
    "- Pausen: 200 m Trab (7:00-7:20/km) oder 400 m Trab (5:30-6:30/km).\n"
    "- Umfang: 4 bis 16 Wiederholungen (16x400 am 03.06., 13 am 26.08., 12 am 16.09.), Intensitätsanteil 4-6 km.\n"
    "- Puls: im Schnitt 166-176, zum Ende der Serie 183-194 (Maximum 198). Das ist VO2max-Training an der Grenze, "
    "nicht Schwelle.\n"
    "- Einordnung: 400er bei 3:50/km passen zu deiner 5-km-Rennpace (4:03/km in Erfurt nach dem Rad) und zur "
    "10-km-Pace (4:21/km in Teichland).\n"
    "Vorgehen jetzt: Wiedereinstieg bei 70 % Volumen. Dezember 6-8x400 m bei 4:05-4:15/km, Pause 200 m; Januar "
    "10x400 oder 5x600; Februar 12x400 bei 3:55-4:05 oder 3x800; März/April 4-5x1000 m an der Schwellenpace "
    "(ca. 4:10-4:15/km) oder 6x1 km bei 3-5-km-Tempo. Nicht schneller als die Zielpace in den ersten Wiederholungen: "
    "bei der Hälfte der Serien sinkt die Qualität (z. B. 26.08. von 3:43 auf 5:35). Paces nach dem Lauf-Stufentest "
    "am 18.11. anpassen. Pro Woche nur eine harte Laufeinheit, dazu der lange Lauf am Sonntag. Solange das Vereinstraining "
    "noch nicht startet (Termin offen), läufst du dieselbe Einheit allein auf der Bahn am Mittwoch, nach dem Kraftraum.")

RAD_INTERVALLE = (
    "Rad-Intervalle: Du fährst sie dort, wo sie am besten in die Woche passen, unter der Woche und am Wochenende, Berge oder "
    "flach, immer nach Leistung (% FTP). Plan: Schlüssel 1 = Do, Schlüssel 2 = Sa vormittags als Block in der langen Fahrt, "
    "Schlüssel 3 = Di alle 2 Wochen ab Phase 3. Die DM-spezifischen Renntempo-Blöcke ab Mai fährst du bevorzugt flach, weil "
    "Cottbus und die DM flach und windschattenfrei sind; das geht Do oder Sa auf flacher Strecke. Am Wochenende hast du "
    "zwei Einheiten pro Tag: Intervall oder lange Fahrt morgens, nachmittags nur locker (Lauf, Schwimmen, Core).\n"
    "Phase 1 (23.11.-24.01.): Do Sweet Spot 2x20 min bei 88-93 % FTP (Pause 5 min), im Verlauf 2x25, 3x15, 3x20 min. "
    "Sa ab Januar im Mittelteil der Ausfahrt 1x30 min Sweet Spot, sonst Z2. Sobald das Zeitfahrrad da ist, mindestens "
    "20 min im Do-Block in Aeroposition.\n"
    "Phase 2 (25.01.-21.03.): Do Schwelle 2x20 min bei 95-100 % FTP, im Verlauf 3x15, 2x25, 4x12 min. Sa in der 3-4 h Fahrt "
    "ein Block 2x20 min Sweet Spot oder 3x15 min Schwelle. Di alle 2 Wochen (ab Februar) Over-Unders 3x(2x6 min bei 95/105 %).\n"
    "Phase 3 (22.03.-16.05.): Do VO2max 5x4, 5x5, 6x4 min bei 110-120 % FTP (Pause gleich lang) plus Koppellauf 10-15 min. "
    "Sa in 4-5 h Fahrt ein Block 2x30 min bei 88-93 % oder 3x15 min bei 95-100 % im Wechsel. Di alle 2 Wochen Sweet Spot/Tempo "
    "2x25-30 min. Erholungswoche 10.05.: Zeitfahrtest 40 km am Do 13.05.\n"
    "Phase 4 (17.05.-25.07.): Do Renntempo-Block 2x20 oder 3x15 min bei 95-100 % FTP, später 40 km bei 88-92 % FTP (Wert aus dem "
    "Zeitfahrtest) plus Koppellauf 15-20 min. Sa Renntempo-Block flach in der 3-4 h Fahrt (40 km bei 88-92 %) im Wechsel mit "
    "Schwelle 3x12 min. Di alle 2 Wochen Schwelle 3x12 min bei 100 % oder VO2max 4x4 min zur Frische. So alle 2 Wochen Brick (40 "
    "min Rad bei 85-90 % FTP, dann 10 km Lauf im Renntempo) statt des langen Laufs. In den Radrennen-Fenstern ersetzt das "
    "Rennen den Samstagsblock.\n"
    "Rennwoche DM (02.08.): nur kurze Öffner, keine Intervalle über 5 min. Spätsaison: Hölle von Q liegt im Harz, deshalb fährst "
    "du den Brick am Sa 28.08. auf hügeligem Harz-Profil und die Renntempo-Blöcke davor am Anstieg, sobald das Streckenprofil "
    "feststeht.\n"
    "Regeln: Intervalle immer nach Leistung, nicht nach Gefühl; Wind ist Teil des Trainings; Wenden (U-Turns) in jeder "
    "Renntempo-Einheit 6-8 mal; bei Gelb Umfang um ein Intervall kürzen, bei Rot streichen; nie Rad-Intervalle an zwei Tagen "
    "hintereinander.")

KOPPEL = (
    "Koppeltraining (Rad -> Lauf) für T2 und die Laufbeine nach dem Rad. Drei Arten:\n"
    "A) Sonntags-Koppel, jede Woche: erst 60 min Rad locker (Z1-Z2, 50-60 % FTP, Trittfrequenz 85-95), direkt danach der lange "
    "Lauf der Woche (60-100 min, locker bis steady). Wechsel zügig unter 3 min, Laufschuhe bereitgelegt. Das ist ab sofort "
    "sinnvoll: der Rad-Teil ist leicht (ca. 28 TSS), der Lauf bleibt locker, du übst den Übergang früh und sparst Zeit. In "
    "Erholungswochen 45 min Rad plus 40 min Lauf.\n"
    "B) Kurz-Koppel nach dem Do-Rad-Schlüssel, ab Phase 3: Lauf 10-15 min (Phase 4: 15-20 min) direkt nach den Intervallen. Die "
    "ersten 5 min kontrolliert (Beine finden), danach Renn-Gefühl.\n"
    "C) Renn-Brick, alle 2 Wochen in Phase 3-4 statt A: 40 min Rad bei 85-90 % FTP in Rennposition (flach) plus 10 km Lauf im "
    "Renntempo (erste 2 km kontrolliert), Verpflegung exakt nach Renn-Plan (siehe Darmtraining). Termine: 09.05., 06.06., 20.06., "
    "04.07., Generalprobe 18.07. (Start 11:30). Hölle von Q: Sa 28.08. Brick 100 km Rad bei 70-78 % FTP plus 10-14 km Lauf.\n"
    "Pflicht nach Phase: Phase 1-2 nur A; ab 22.03. (Phase 3) mindestens 2 Koppelläufe pro Woche (So und Do); ab 17.05. "
    "zusätzlich alle 2 Wochen ein Renn-Brick; die letzte Koppel vor der DM ist der Renn-Brick am 18.07., danach nur kurze "
    "Koppel im Taper. Nicht koppeln: nach der langen Samstagsfahrt, in Erholungswochen kein Renn-Brick, in der Rennwoche gar "
    "nicht.\n"
    "Steuerung: Der Koppel-Lauf zählt voll zum Laufumfang (höchstens +10 % pro Woche). Bei Gelb den Rad-Teil auf 45 min kürzen "
    "und den Lauf locker halten, bei Rot streichen.")

KOPPEL_BRICKS = [
    ("2027-05-09", "Koppel: Renn-Brick 1", "Erster Renn-Brick am Ende von Phase 3. 40 min Rad bei 85-90 % FTP flach in Rennposition, direkt 10 km Lauf im Renntempo (erste 2 km kontrolliert). Wechsel stoppen, Ziel unter 1:00. Verpflegung wie im Renn-Plan."),
    ("2027-06-06", "Koppel: Renn-Brick 2", "Eine Woche vor Cottbus. 40 min Rad bei 85-90 % FTP flach, 10 km Lauf im Renntempo, Brick-Lauf mit 85 g/h (Darmtraining). Danach Mini-Taper für Cottbus."),
    ("2027-06-20", "Koppel: Renn-Brick 3", "Nach Cottbus Plan überprüfen. 40 min Rad bei 85-90 % FTP flach, 10 km Lauf im Renntempo mit 90 g/h."),
    ("2027-07-04", "Koppel: Renn-Brick 4", "40 min Rad bei 85-90 % FTP flach in Rennposition, 10 km Lauf im Renntempo mit 95 g/h, Hitzeprotokoll (Sauna-Block läuft). Letzte Bestätigung vor der Generalprobe."),
    ("2027-07-18", "Koppel: Generalprobe DM", "Exakt der Renn-Plan, Start um 11:30: 40 min Rad im Renntempo flach in Rennposition mit 130 g/h, 10 km Lauf im Renntempo mit 100 g/h, Koffein und Natrium wie geplant. Wechsel stoppen."),
]

SAUNA = (
    "Sauna steht dir zur Verfügung. Zwei Nutzungen:\n"
    "1) Erholung (ganzjährig, 1-2x pro Woche, z. B. Do nach Schwimmen und Fr abends): 10-15 min bei 80-90 Grad, "
    "dann abkühlen, Wasser trinken. Nicht direkt vor Schlüsseleinheiten oder Tests, nicht bei Krankheit.\n"
    "2) Hitzeanpassung für die DM (August): 3 Wochen vom 05.07. bis 25.07., 3-4x pro Woche je 20-30 min direkt "
    "nach einer lockeren Einheit (Rad oder Lauf), nicht nach harten Tagen. Ziel: mehr Plasmavolumen, niedrigerer "
    "Puls bei Hitze. Pro Woche 1-2 Saunagänge mehr als bisher steigern. In der Rennwoche nur noch 1-2 kurze Gänge "
    "bis 3 Tage vor dem Rennen, am Renntag davor und danach nicht.\n"
    "Viel trinken (500 ml pro Gang plus Salz), Gewicht vor und nach wiegen (Verlust höchstens 1 %). HRV am Morgen "
    "nach der Sauna kann niedriger sein, das ist normal und kein Gelb-Signal, solange es nach 48 h zurück ist.\n"
    "Eisbad/Kaltwasser (1-3 min): gut nach Schwimmen, Wettkämpfen und in Erholungswochen, höchstens 1-2x pro Woche. "
    "Nicht direkt nach Krafttraining (Mo, Mi) und nicht nach den Schlüsseleinheiten im Aufbau, weil Kälte die Anpassung "
    "dämpfen kann. Nicht in den 3 Tagen vor einem Test oder Rennen.\n"
    "Eintragen: python -m trainingsplan log --tag JJJJ-MM-TT --text 'Sauna 2x15 min bei 90 Grad, Eistonne 1 min' --apply. "
    "Die Auswertung erkennt Sauna und Eisbad im Kommentar, lässt die Morgenwerte des Folgetags aus HRV- und Ruhepuls-Mittel "
    "heraus und schreibt dazu eine Einordnung (Beispiel 11.11.: Ruhepuls 52 statt 48, HRV 79 statt 93).")

HITZE = (
    "Sportspezifisches Hitzetraining für die DM So 08.08.2027 (Start 11:30, Nordsee, Mittagshitze möglich): Die "
    "Anpassung findet in den Sportarten statt, in denen du im Rennen arbeitest, also auf dem Rad (Rolle im warmen Raum, im "
    "Sommer auch draußen) und im Sommer beim Laufen. Sauna oder heißes Bad sind nur Ergänzung. Block 05.07. bis 25.07. "
    "(3 Wochen, endet 14 Tage vor dem Rennen; die Anpassung hält 2-3 Wochen), danach Auffrischung. Ab 01.07. sind Schule und "
    "Ferien vorbei, die Wochentage sind frei. Im Juli und August ist Sommerhitze draußen zusätzlicher Reiz.\n"
    "PRINZIP\n"
    "- Hitze nur auf lockeren bis mittleren Einheiten (Z1-Z2, bei Brick/Generalprobe Renntempo in natürlicher Hitze). Keine Intervalle "
    "künstlich in Hitze: die Qualität leidet. Die Heat-Einheiten ersetzen lockere Einheiten, sie sind kein Zusatzumfang.\n"
    "- Reiz ist die Körperkerntemperatur ab 38,5 Grad für 45-60 min: Puls 10-15 Schläge über normal, Schweiß fließt, Leistung/Pace nicht erhöhen.\n"
    "BAUSTEINE\n"
    "1) Heat-Ride Rolle (Di, Sa nachmittags, 45 -> 60 min): geschlossener warmer Raum (28-32 Grad), ohne Ventilator oder mit "
    "langer Kleidung (Trikot, Windweste/Jacke), 55-60 % FTP. Workout 'Rad Hitze-Anpassung 60 min'. Im Sommer: lockere "
    "Fahrt mittags bei Wärme, zusätzlich Weste.\n"
    "2) Heat-Lauf (Fr, 30 -> 45 min, ab Woche 2 plus ein zweiter): lockerer Lauf mittags bei Sommerwärme, bei Kühle mit langer "
    "Hose/Shirt und Mütze. Pace 6:50-7:10/km, Puls steigt, Tempo nicht erhöhen. Workout 'Lauf Hitze-Anpassung 40 min'. "
    "Nie bei Gewitter oder Hitzewarnung über 32 Grad im Freien ohne Trinkpausen.\n"
    "3) Heat-Koppel (So): 60 min lockeres Rad auf der Rolle im warmen Raum oder draußen mittags, dann der Lauf in Mittagshitze "
    "(wie am Renntag 11:30). Hier übst du Trinken, Gels und Kühlen wie im Rennen.\n"
    "4) Optional passiv nach lockeren Einheiten: 1-2 x pro Woche Sauna oder 40-Grad-Bad 20-30 min, nicht nach Intervallen oder "
    "dem langen Samstag.\n"
    "DOSIS\n"
    "- Woche 05.07.: 2 Heat-Rides (Di 45 min, Sa 45 min), 1 Heat-Lauf (Fr 30 min), Koppel So normal\n"
    "- Woche 12.07.: 2 Heat-Rides 60 min, 2 Heat-Läufe (Fr 40 min, Mo 30 min), Heat-Koppel So 11.07.; Generalprobe So 18.07. nicht "
    "künstlich überhitzen\n"
    "- Woche 19.07.: 3 Heat-Rides 60 min, 2 Heat-Läufe 40 min, Heat-Koppel So 25.07.; Sauna optional\n"
    "- Taper 26.07.-03.08.: 1 Heat-Ride 45 min (Di) und 1 Heat-Lauf 25 min (Fr 30.07.), danach nichts Künstliches mehr; "
    "natürliche Hitze und Sauna 15-20 min nur wie gewohnt, ab 04.08. nichts Neues.\n"
    "TRINKEN UND KONTROLLE\n"
    "- Gewicht vor und nach wiegen: Verlust höchstens 2 % (bei 67 kg ca. 1,3 kg); pro 1 kg Verlust 1,2-1,5 l ersetzen, dazu "
    "500-1000 mg Natrium pro Stunde. Die Schweißrate der ersten Einheit ist dein Natrium- und Trinkwert für die DM.\n"
    "- Morgenwerte: HRV 5-10 % niedriger und Ruhepuls +2-4 nach Hitze sind normal, wenn nach 48 h zurück. Länger: Ampel Gelb, "
    "Hitze streichen, Umfang -15 %. Nicht bei Krankheit, Schwindel, Kopfschmerz oder Herzrasen.\n"
    "- Test: Puls bei gleicher Leistung/Pace (erste vs letzte Hitzeeinheit), Schweißrate, Gefühl bei Mittagshitze. Neopren und "
    "Salzwasser: 1-2 Freiwassereinheiten bei Wärme üben.\n"
    "- Ausrüstung: Rad: Ventilator weg, Rolle im kleinen Raum, Heizlüfter nur mit Abstand und Sicherheit; Lauf: Mütze, Trinkflasche, "
    "Schatten, Wasser über den Kopf.")

KONTROLLE = (
    "Regeln, die der Plan überwacht:\n"
    "- CTL-Anstieg höchstens ca. 4,5 pro Woche, Belastungsverhältnis (7 Tage zu Normalwoche) zwischen 0,8 und 1,3.\n"
    "- Lauf-Load wächst höchstens ca. 10-12 % pro Woche; bei Schmerzen im Schienbein/Achilles/Knie "
    "sofort Lauf ersetzen (Rad/Aquajogging). Beinkraft ersetzt keine Laufprogression: den Laufumfang trotzdem bei "
    "höchstens +10 % pro Woche halten und nie zwei lange Läufe in einer Woche. Bergab laufen ist hohe "
    "Bremsbelastung: in den ersten 8 Wochen bergab traben oder gehen, Höhenmeter pro Woche um höchstens "
    "20-25 % steigern. Radberge sind dagegen gelenkschonend.\n"
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
    ("2027-05-13", "Zeitfahrtest 40 km",
     "Do 13.05. in der Erholungswoche (unter der Woche, flache Strecke bei dir): 40 km solo in Rennposition, so schnell wie möglich und gleichmäßig "
     "(Windschatten verboten wie bei der DM). Daraus Renn-Leistung und Aero-Position bewerten: bei der DM ca. 88-92 % deiner "
     "40-km-Leistung, weil danach noch 10 km laufen. Dabei Verpflegung mit 130 g/h testen."),
    ("2027-07-10", "Generalprobe Kurzdistanz",
     "In der Erholungswoche: Koppel 30 km Rad im Renntempo (flach, Rennposition) + 5 km Lauf im Renntempo, "
     "Verpflegung und Wechsel üben, 1,5 km Freiwasser mit Neopren."),
]

# (Montag, Name, Beschreibung)
def _hitze_tage(von: str, bis: str, wochentag: int = 1) -> list[str]:
    """Hitzetage (Standard Dienstag) von Montag `von` bis `bis`; Erholungs- und Testwochen entfallen."""
    skip = {t for t, _, r in WOCHEN if r}
    for d, _, _ in RETESTS:
        dd = date.fromisoformat(d)
        skip.add((dd - timedelta(days=dd.weekday())).isoformat())
    tage, m = [], date.fromisoformat(von)
    while m <= date.fromisoformat(bis):
        if m.isoformat() not in skip:
            tage.append(f"{m + timedelta(days=wochentag):%d.%m.}")
        m += timedelta(days=7)
    return tage


PHASEN: list[tuple[str, str, str]] = [
    ("2026-11-16", "Phase 0: Tests (bis 22.11.)",
     "Ziel: nach Krankheit/Off-Season wieder Normalbetrieb, Schwellenwerte ermitteln "
     "(Rad-Stufentest 14.11., Lauf-Stufentest 17.11.). Load 310-410 pro Woche inkl. beider Tests. Der Wiedereinstieg ist kurz: du bist\n"
     "seit Wochen wieder bei Normalwochen, HRV und Ruhepuls sind auf Basis, deshalb kein Deload danach.\n"
     "Erwartung: CTL 26 -> ca. 31, Form -7 bis -15. HRV (~90) und Ruhepuls (~47) bleiben auf "
     "deiner Basis, Schlaf ~8 h. Danach FTP, LTHR und Zonen aus den Tests übernehmen."),
    ("2026-11-23", "Phase 1: Grundlage I (23.11.-24.01.)",
     "Intensitätsverteilung ca. 85 % Z1-Z2, 15 % darüber. Beinkraft kommt aus dem Kraftraum. "
     "Rad: Sa 3-4 h in deinen gewohnten Zonen (Z2), am Wochenende in den Bergen, wenn du kannst, sonst flach; das Training ist "
     "dasselbe wie im Flachen, nach Leistung gefahren. Dazu eine Sweet-Spot-Einheit am Do "
     "2x20 min bei 88-93 % FTP. Der Do-Schlüssel liegt unter der Woche und damit flach; die DM-Radstrecke ist flach und windschattenfrei (Notiz DM-Strecke). Bis das Zeitfahrrad da ist, fährst du ihn in tiefer Position am Unterlenker, danach mindestens 20 min davon in Aeroposition. Lauf: 4 Läufe, So nach 60 min lockerem Rad (Koppel) 60-75 min im Hügelgelände (bergauf kräftig, bergab "
     "traben oder gehen), Steigerungsläufe 6x20 s, Lauf-ABC, Mi Intervalle auf der Bahn (6-10x400 m, Verein). Schwimmen: Vereinstraining plus Technik. "
     "Kraftraum: Mo Beine schwer + Oberkörper, Mi Oberkörper/Core vor dem Lauf (siehe Notiz Krafttraining). "
     "Load 440 -> 550, ca. 13 -> 17 h (KW 48 bereits ca. 13 h), davon Rad 7 -> 10 h (dein Radumfang aus 2021/22 und deine Spitzenwoche vom "
     "07.09. mit 10,5 h Rad). Erster Block 4 Wochen bis 14.12., danach Erholungswoche.\n"
     "Deine Radbasis aus 2020-2022 kommt schnell zurück, Engpässe sind Laufen und Schwimmen.\n"
     "Erwartung: CTL 31 -> ca. 59 (erste Aufbauwoche einmalig +5, danach +3,5 bis 4,5 pro Woche), Form -17 bis -21 in Belastungswochen, "
     "-4 bis 0 in Erholungswochen. In der 3. Belastungswoche sind HRV 5-10 % unter Basis und "
     "Ruhepuls +1-3 bpm normal."),
    ("2026-11-23", "Wochenstruktur und Kontrolle", WOCHENSTRUKTUR + "\n\n" + KONTROLLE),
    ("2026-11-23", "Krafttraining Kraftraum", KRAFTPLAN),
    ("2026-11-23", "Rad-Intervalle: Plan nach Möglichkeiten und Zielen", RAD_INTERVALLE),
    ("2026-11-23", "Koppeltraining: Plan", KOPPEL),
    ("2026-11-23", "Mittwochs-Intervalle Lauf", LAUFINTERVALLE),
    ("2027-07-05", "Sauna: Erholung und Hitzeanpassung", SAUNA),
    ("2027-06-28", "Hitzetraining: Plan für die DM", HITZE),
    ("2026-11-23", "Hitzetraining Jahresplan: wöchentlicher Heat-Ride (Rolle)",
     "Hitzetraining läuft das ganze Jahr, sportspezifisch auf der Rolle (Rolle ist verfügbar) und im Sommer beim Laufen. "
     "Idee: Grundstock von 1 Heat-Ride pro Woche ab Dezember (hält die Anpassung), Mini-Block vor Cottbus (24.05.-06.06.), "
     "Haupt-Block vor der DM (05.-25.07., siehe Notiz Hitzetraining: Plan für die DM), im Spätsommer 1 Heat-Ride pro Woche. "
     "Erholungs- und Testwochen entfallen, Heat-Ride ersetzt immer eine lockere Rad-Einheit (kein Zusatzumfang). "
     "Winter: Raum so warm wie möglich (24-30 Grad), lange Kleidung, kein Ventilator, 55-60 % FTP, Puls 10-15 über normal. "
     "Abbruch bei Schwindel, Kopfschmerz, Krankheit. Ampel Gelb (HRV unter ca. 78 oder Ruhepuls über ca. 51): kein Heat-Ride. "
     "Nicht in den 3 Tagen vor Tests, Cottbus und DM künstlich überhitzen. Gewicht vor/nach wiegen, höchstens 2 % Verlust, 500-1000 mg Natrium pro Stunde. "
     "Workout in der Bibliothek: 'Rad Hitze-Anpassung 60 min' (45 min: Dauer verkürzen)."),
    ("2026-11-30", "Hitzetraining Phase 1: 1x pro Woche Heat-Ride (Di)",
     "Grundlage I, 1 Heat-Ride pro Woche, Di, erste Woche 45 min, danach 60 min. Termine: " + ", ".join(_hitze_tage("2026-11-30", "2027-01-24")) +
     ". Erholungswochen (21.12.) entfallen. Raum warm, lange Kleidung, 55-60 % FTP; Ziel ist die Gewöhnung, kein Leistungsdruck."),
    ("2027-01-25", "Hitzetraining Phase 2: 1x pro Woche Heat-Ride (Di)",
     "Grundlage II: 1 Heat-Ride pro Woche, Di, 60 min. Termine: " + ", ".join(_hitze_tage("2027-01-25", "2027-03-21")) +
     ". Erholungs- und Retest-Wochen (15.03.) entfallen. Bei Schlüsseleinheit am Do darauf achten, dass der Di-Heat-Ride nicht die Ermüdung erhöht (Ampel prüfen)."),
    ("2027-03-22", "Hitzetraining Phase 3: 1x pro Woche Heat-Ride (Di)",
     "Aufbau intensiv und Abitur-Phase: 1 Heat-Ride pro Woche, Di, 45-60 min. Termine: " + ", ".join(_hitze_tage("2027-03-22", "2027-05-16")) +
     ". In Prüfungswochen (siehe Abitur-Notizen) streichen, wenn der Schlaf leidet; Erholungswoche 12.04. und 10.05. entfallen."),
    ("2027-05-24", "Hitzetraining Mini-Block vor Cottbus (24.05.-06.06.)",
     "2 Wochen: 3 Heat-Rides pro Woche (Di 60 min, Sa nachmittags 60 min, So Heat-Koppel: 60 min Rad warm + Lauf mittags) und 1 Heat-Lauf Mo 30 min (Sommerwärme, wenn vorhanden). "
     "Termine: Mo 24.05. (Lauf), Di 25.05., Sa 29.05., So 30.05., Mo 31.05. (Lauf), Di 01.06., Sa 05.06., So 06.06. Cottbus Sa 12.06. liegt 6 Tage nach dem Block. Reiz ersetzt lockere Einheiten; "
     "Brick am 06.06. (Renn-Brick 2) bleibt wie geplant, aber in warmer Umgebung. Fr bleibt frei."),
    ("2027-06-14", "Hitzetraining Erhalt bis zum Hauptblock",
     "1 Heat-Ride pro Woche (Di 45-60 min): " + ", ".join(_hitze_tage("2027-06-14", "2027-06-28")) +
     ". Dazu natürliche Sommerhitze nutzen. Danach beginnt der Haupt-Block 05.07.-25.07. (Notiz Hitzetraining: Plan für die DM)."),
    ("2027-08-16", "Hitzetraining Spätsaison (Hölle von Q)",
     "Optional für das B-Rennen Hölle von Q (So 05.09., Harz, 90 km Rad): 1 Heat-Ride pro Woche Di 45-60 min am 17.08. und 24.08. "
     "(Schlüsselwoche 23.08.: nur wenn die Ampel grün ist), Rennwoche 30.08. nichts Künstliches. Jahres-Ende: Heat-Ride im Herbst bei Bedarf fortsetzen."),
    ("2027-07-05", "Hitzetraining Woche 1: 2 Heat-Rides, 1 Heat-Lauf", "Di Heat-Ride 45 min (Rolle warm, 55-60 % FTP), Fr Heat-Lauf 30 min (mittags im Sommer, 6:50-7:10/km), Sa nachmittags Heat-Ride 45 min. Gewicht vor/nach wiegen, Schweißrate notieren, HRV und Ruhepuls beobachten. Siehe Notiz Hitzetraining: Plan für die DM."),
    ("2027-07-12", "Hitzetraining Woche 2: 2 Heat-Rides, 2 Heat-Läufe, Heat-Koppel", "Mo Heat-Lauf 30 min, Di Heat-Ride 60 min, Fr Heat-Lauf 40 min, Sa Heat-Ride 60 min nachmittags, So 11.07. Heat-Koppel (60 min Rad warm + Lauf mittags). Generalprobe So 18.07.: vorher nichts künstlich Heißes am Sa."),
    ("2027-07-19", "Hitzetraining Woche 3: 3 Heat-Rides, 2 Heat-Läufe, Heat-Koppel", "Di, Do (locker, kein Schlüssel) und Sa Heat-Ride 60 min, Mo und Fr Heat-Lauf 40 min, So 25.07. Heat-Koppel. Letzte Hitzewoche, Sauna optional 20-30 min nach lockeren Tagen."),
    ("2027-07-26", "Hitzetraining: Auffrischung im Taper", "Di 27.07. Heat-Ride 45 min, Fr 30.07. Heat-Lauf 25 min, danach nur noch natürliche Hitze. Rennwoche: nichts Neues, Trinken und Natrium wie getestet."),
    ("2027-01-25", "Phase 2: Grundlage II / Aufbau (25.01.-21.03.)",
     "Intensität steigt (pyramidal ca. 80/15/5). Rad-Intervalle, wo sie am besten passen: Do Schwelle "
     "2x20 min bei 95-100 % FTP (später 3x15, 2x25), Sa in der langen Fahrt ein Block (2x20 min Sweet Spot oder 3x15 min "
     "Schwelle), Di alle 2 Wochen Over-Unders; Berge oder flach, gleiche Zonen. "
     "Lauf: Mi Bahnintervalle (10-12x400 m, 3x800 m, 4-5x1000 m an der Schwellenpace), So Bergläufe 8x60 s bergauf. Schwimmen: CSS-Sätze 10x100 m. Kraftraum Mo Maximalkraft, Mi Oberkörper vor dem Lauf, ab März "
     "Erhalt. Load 560 -> 640, ca. 16 -> 18 h (Rad 9-10 h).\n"
     "Erwartung: CTL 58 -> ca. 75, Form -14 bis -17. Ruhepuls im Wochenmittel +1-2 bpm in "
     "Belastungswochen."),
    ("2027-03-22", "Phase 3: Aufbau intensiv (22.03.-16.05.)",
     "VO2max: Rad 5x4-5 min bei 110-120 % FTP (Pause gleich lang) oder 30/30; Lauf 6x1 km bei "
     "3-5-km-Tempo; Schwimmen 8x200 m bei CSS. Koppeltraining: jeden Sonntag 60 min Rad locker plus Lauf, Do nach den Intervallen "
     "Koppellauf 10-15 min, alle 2 Wochen Renn-Brick (siehe Notiz Koppeltraining), Rad-Intervalle: Do VO2max "
     "5x4-5 min bei 110-120 % FTP plus Koppellauf 10-15 min, Sa in 4-5 h Fahrt ein Block 2x30 min bei 88-93 % oder 3x15 min "
     "bei 95-100 % FTP (Berge oder flach), Di alle 2 Wochen Sweet Spot/Tempo 2x25-30 min. "
     "Load 640 -> 715, ca. 17 -> 19 h (Rad 9-10 h).\n"
     "Erwartung: CTL 75 -> ca. 87, Form -10 bis -14. Mehr Intensität heißt stärkere Reaktion: "
     "nach harten Tagen HRV 10-15 % niedriger ist normal und sollte nach 48 h zurück sein. "
     "Ab hier die Ampel (Gelb/Rot) strikt befolgen."),
    ("2027-05-17", "Phase 4: Wettkampfvorbereitung (17.05.-25.07.)",
     "Kurzdistanz-spezifisch (1,5 km / 40 km / 10 km, ca. 2:30 h): Renntempo-Blöcke Rad 3x12 min "
     "bei 100-105 % FTP, Brick Rad 40 min bei 85-90 % FTP + Lauf 10 km im Renntempo (alle 2 Wochen), "
     "Freiwasser mit Neopren ab Mai, 1,5 km am Stück, lange Radfahrt bis 4-5 h, langer Lauf bis 100 min. "
     "Die DM-Strecke ist flach und windschattenfrei (siehe Notiz DM-Strecke). Die Renntempo-Blöcke fährst du bevorzugt flach "
     "(Do, Sa auf flacher Strecke): 3x12 oder 2x20 min bei 95-100 % FTP und 40-km-Blöcke in Rennposition (Aeroposition, sobald "
     "das Zeitfahrrad da ist), Wenden üben, bei Wind fahren. Sa lange Fahrt mit Renntempo-Block, am Wochenende vormittags "
     "Intervall, nachmittags locker. Läufe ab "
     "Mai flach im Renntempo; in der Rennwoche keine Intervalle am Samstag. Zeitfahrtest 40 km solo am Do 13.05. "
     "Sa 12.06. Cottbus (Olympische Distanz = B-Rennen und Generalprobe für die DM, Mini-Taper Mi-Fr, "
     "ersetzt den Formcheck). Weitere Rennen vor der DM nach Termin: Supersprint/Sprint ersetzt die "
     "Samstags-Brick-Einheit. "
     "Zwei Spitzenblöcke zu 3 Wochen (710-760 TSS, ca. 18-19 h). Spitzenwochen dürfen 20-21 h "
     "erreichen, wenn der Mehrumfang locker ist (Z1-Z2, zusätzliches Rad/Schwimmen) und die Ampel grün "
     "bleibt. Erholungswochen am 07.06. und 05.07.; die Wochen 12. und 19.07. fallen leicht ab.\n"
     "Erwartung: CTL 87 -> ca. 96 Ende Juni (dein bisheriges Maximum war 74 im Jahr 2021), Form -10 bis "
     "-14 in Blöcken. Die Zahlen hängen an einer korrekten FTP-Einstellung."),
    ("2027-07-26", "Taper und Höchstform (26.07.-08.08.)",
     "Woche -2 (26.07.): Volumen ca. -20 % (600), Intensität unverändert. Rennwoche: ca. 345 TSS "
     "Vorbereitung plus Rennen (ca. 150-180 TSS), Wochenziel 520 enthält das Rennen. Mo/Di "
     "je 1 Qualitätsreiz (3-5 Reize à 3-5 min im Renntempo), Mi/Do locker mit 3x30 s Öffnern, Fr "
     "frei, Sa 20 min Öffnungsrunde. Letzte Beinkraft 14 Tage, Oberkörper/Core 7 Tage vorher, nichts Neues "
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
    "2026-11-16": {"Ride": 87, "Run": 100, "Swim": 102, "Other": 22},  # Lauf-Stufentest Mi
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
    rate = dict(TSS_PRO_STUNDE, Ride=_stufe(_RAD_TSS_H, tag))
    return sum(load / rate[sport] for sport, load in verteilung(gesamt, tag, erholung).items())


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


# Phasen-Notizen als Zeitspanne (letzter Tag der Phase), damit sie im Kalender als Balken über die Phase stehen
PHASEN_ENDE = {"Phase 0": "2026-11-22", "Phase 1": "2027-01-24", "Phase 2": "2027-03-21", "Phase 3": "2027-05-16",
               "Phase 4": "2027-07-25", "Taper und Höchstform": "2027-08-08", "Nach dem Wettkampf": "2027-09-05"}


def _phasen_ende(name: str) -> date | None:
    for k, v in PHASEN_ENDE.items():
        if name.startswith(k):
            return date.fromisoformat(v)
    return None


def notiz_events(vorhandene_notizen: set[str]) -> list[dict]:
    """Phasen- (als Zeitspanne), Erholungswochen-, Test- und Koppel-Notizen; Erholungswochen an Tagen mit Notiz entfallen."""
    out = []
    for tag, name, text in PHASEN:
        out.append((montag(tag), name, text, _phasen_ende(name)))
    for tag, _, erholung in WOCHEN:
        if erholung and tag not in TAPER_WOCHEN:
            out.append((montag(tag), "Erholungswoche", ERHOLUNG_TEXT, None))
    for tag, name, text in RETESTS:
        out.append((date.fromisoformat(tag), name, text, None))
    for tag, name, text in KOPPEL_BRICKS:
        out.append((date.fromisoformat(tag), name, text, None))
    events = []
    for d, name, text, ende in out:
        if name == "Erholungswoche" and d.isoformat() in vorhandene_notizen:
            continue
        letzter = ende or d
        events.append({"category": "NOTE", "name": name, "description": text,
                       "start_date_local": f"{d.isoformat()}T00:00:00",
                       "end_date_local": f"{(letzter + timedelta(days=1)).isoformat()}T00:00:00",
                       "external_id": f"saison-note-{d.isoformat()}-{name[:7].lower().strip(':')}"})
    return events


# ---------------------------------------------------------------------------------------------
# Übersicht: welche Belastungsart wann
# ---------------------------------------------------------------------------------------------
RENNWOCHE_VORBEREITUNG = [80, 100, 50, 70, 0, 40]  # Mo-Sa vor dem Rennen (ohne Rennen)
RENNTAG_TSS = 170

# (von, bis, Phase, Belastungsart, Intensitätsverteilung, Rad, Lauf, Schwimmen/Kraft)
PHASEN_UEBERSICHT = [
    ("2026-11-09", "2026-11-22", "0 Tests", "Reaktivierung, Leistungsdiagnostik",
     "locker, Tests Sa 14.11./Di 17.11.", "Stufentest, Z2", "Stufentest, locker", "Verein, Kraft Mo Oberkörper + Beine leicht (ab 16.11.), Mi vor dem Lauf"),
    ("2026-11-23", "2027-01-24", "1 Grundlage I", "Aerobes Volumen, Technik, Maximalkraft im Kraftraum",
     "ca. 85 % Z1-Z2 / 15 % darüber", "Do Sweet Spot 2x20-3x20, Sa 3-4 h Z2 (ab Jan. 1x30 min Sweet Spot im Block), So PM Rad locker",
     "Mi Bahn 6-10x400, So Koppel: 60 min Rad locker + Hügellauf 60-75 min, Steigerungen", "Verein + Technik; Kraftraum Mo Beine + Oberkörper, Mi Oberkörper/Core, RIR 2-3"),
    ("2027-01-25", "2027-03-21", "2 Grundlage II / Aufbau", "Schwelle, Tempo, aerobe Leistung",
     "ca. 80 / 15 / 5 (pyramidal)", "Do Schwelle 2x20 / 3x15 bei 95-100 %, Sa Block 2x20 Sweet Spot / 3x15 Schwelle in 3-4 h, Di (alle 2 Wo.) Over-Unders",
     "Mi Bahn 10-12x400 / 3x800 / 4-5x1000, So Koppel 60 min Rad + Lauf mit Bergläufen 8x60 s", "CSS-Sätze 10x100; Kraftraum Mo Maximalkraft (4-6 Wdh.), Mi Oberkörper + Sprünge"),
    ("2027-03-22", "2027-05-16", "3 Aufbau intensiv", "VO2max, Koppeltraining, lange Ausdauer",
     "ca. 75 / 15 / 10", "Do VO2max 5x4-5 min + Koppellauf, Sa Block 2x30 Tempo / 3x15 Schwelle in 4-5 h, Di (alle 2 Wo.) Sweet Spot 2x25-30",
     "Mi Bahn 6x1 km (3-5-km-Tempo), So Koppel (60 min Rad + Lauf), Do Koppellauf 10-15 min, alle 2 Wo. Renn-Brick", "8x200 bei CSS; Kraftraum Mo 35-40 min Erhalt, Mi 20 min Core"),
    ("2027-05-17", "2027-07-25", "4 Wettkampfvorbereitung", "Renntempo, Spezifik, Spitzenvolumen",
     "ca. 75 / 15 / 10 mit Renntempo", "Do Renntempo-Block 2x20 / 3x15 / 40 km flach (Aero sobald Zeitfahrrad da) + Koppellauf, Sa Renntempo-Block in 3-4 h, Di alle 2 Wo. Schwelle, So alle 2 Wo. Brick 40 min + 10-km-Lauf",
     "So Koppel (60 min Rad + Lauf bis 100 min) im Wechsel mit Renn-Brick (40 min Rad + 10 km Renntempo flach), Do Koppellauf 15-20 min", "Freiwasser mit und ohne Neopren, Wellen, Bojenwenden, Pulk; 1,5 km am Stück; Kraftraum Mo 35 min Erhalt bis 14 Tage vor DM; Sauna-Block 05.-25.07."),
    ("2027-07-26", "2027-08-08", "Taper und Rennen", "Frische, Schärfe, Renntempo-Öffner",
     "locker + wenige scharfe Reize", "3-5 Reize à 3-5 min im Renntempo, Öffner", "kurze Tempoläufe, Öffner",
     "locker, Technik; letzte Beinkraft 14 Tage, Oberkörper 7 Tage vorher"),
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
         "Wochenziele in TSS, Stunden grob geschätzt (Rad 34, Lauf 48, Schwimmen 35, Kraft 14 TSS/h, aus deinen Daten). "
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
     "Technik, Fr frei (kein Training möglich), Sa Rennen. Pacing, Wechsel und Verpflegung wie bei der DM üben. "
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
