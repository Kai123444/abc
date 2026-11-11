"""Konkrete Einheiten für die Testwochen 09.-22.11.2026 (Phase 0) als intervals.icu-Workouts.

Sonderfall dieser Woche: Schulevent "24 Stunden Schwimmen" von Fr 13.11. bis Sa 14.11.; du schwimmst
dort nur 4 km locker. Am Fr kommen Sportunterricht und das Schwimmen zusammen (kein Radtraining). Der
Rad-Stufentest liegt deshalb am So 15.11. (ein freier Tag davor) und der Lauf-Stufentest am Mi 18.11.

Zonen sind noch die alten Einstellungen (FTP 280 W, Lauf-HF-Zonen veraltet). Deshalb Rad in Prozent
mit niedriger Z2 und Laufen nach Pace (deine lockeren Läufe liegen bei 6:30-7:00/km). Nach den
Stufentests FTP, Laufschwelle, LTHR und Zonen aktualisieren.
"""

from __future__ import annotations

# Einträge entfernen: (Datum, Name, Grund)
ENTFERNEN = [
    ("2026-11-12", "run", "Do: Lauf 30 min gestrichen (Sportunterricht 3000 m am Fr, davor Event)"),
    ("2026-11-14", "Technik-Schwimmen (Swim)", "Sa: nach dem 24-h-Schwimmen kein weiteres Schwimmen"),
    ("2026-11-15", "Ausrollen, optional (Ride)", "So: der Stufentest enthält das Ausfahren"),
    # frühere Fassung der nächsten Woche (Lauftest lag am Di, Kraft für Beine am Mo)
    ("2026-11-16", "Kraft: Beine und Core", "Mo: Kraft ohne Beine nach dem Rad-Stufentest"),
    ("2026-11-18", "Rad Grundlage", "Mi: Lauf-Stufentest, Rad am Di"),
    ("2026-11-23", "Rad locker (Montag)", "Mo: Beine nach dem Kraftraum frei, die Fahrt wandert auf den Sonntagnachmittag"),
    ("2026-11-29", "Rad locker (Sonntag Nachmittag)", "So: Rad und Lauf jetzt als Koppel am Vormittag"),
    ("2026-11-29", "Hügellauf locker", "So: Lauf jetzt als Koppel 2 nach dem Rad"),
    ("2026-11-19", "Kraft: Einstieg Beine (leicht)", "Do: Beine jetzt am Montag"),
    ("2026-11-23", "Kraft: Oberkörper und Core", "Mo: Ganzkörper mit Beinen"),
    ("2026-11-25", "Kraft: Beine Technik", "Mi: Beine jetzt am Montag"),
    ("2026-11-19", "Lauf locker", "Do: nach dem Lauftest kein Lauf"),
    ("2026-11-21", "Rad Grundlage lang", "Sa: jetzt als lange Fahrt mit Sweet-Spot-Block"),
    ("2026-11-13", "Rad Grundlage (Freitag, Sondertraining)",
     "Fr: gestrichen, Sportunterricht und Schulevent reichen vor dem Rad-Stufentest am So"),
]

# Verschieben/ändern: (altes Datum, Name, neues Datum, geänderte Felder)
VERSCHIEBEN = [
    ("2026-11-14", "Rad-Stufentest", "2026-11-15", {}),
    ("2026-11-15", "Ruhiger Dauerlauf (Run)", "2026-11-14",
     {"name": "Lauf locker (optional)", "moving_time": 1800,
      "description": "Nach dem Schlafen, nur wenn du dich frisch fühlst, sonst frei.\n- 30m 6:50/km Pace"}),
    # Mi 11.11.: Ruhepuls 52 (Basis 48) und HRV 79 nach langem Dienstag mit Sauna und Eisbad -> nur Beine ausdrehen
    ("2026-11-11", "Ride", "2026-11-11",
     {"name": "Rad locker (Erholung)", "moving_time": 2700,
      "description": "Nur Beine ausdrehen nach Dienstag (MTB 81 min, Schwimmen, Sauna, Eisbad). Puls unter ca. 130, "
                     "Trittfrequenz 85-95. Wenn du dich schwer fühlst: 30 min oder frei.\n- 45m 50%"}),
    ("2026-11-17", "Lauf-Stufentest", "2026-11-18", {}),
    # Heute (Di 10.11.): MTB statt Kadenz-Grundlage, gleiche Dauer
    ("2026-11-10", "Kadenz-Grundlage", "2026-11-10",
     {"type": "MountainBikeRide", "name": "MTB locker (statt Kadenz-Grundlage)", "moving_time": 4320,
      "description": "Gleiche Dauer wie geplant (72 min), aber locker und gleichmäßig: Puls unter ca. 150, "
                     "Anstiege im Sitzen und ruhig, keine Intervalle. Die Kadenz-Intervalle entfallen.\n"
                     "- 72m 55%"}),
]

# Neue Einheiten und Hinweise dieser Woche
DIESE_WOCHE = [
    {"category": "NOTE", "name": "Fr: Schulevent, So: Rad-Stufentest",
     "start_date_local": "2026-11-13T00:00:00",
     "description": "Beim Schulevent schwimmst du nur 4 km locker. Am Freitag kommen Sportunterricht und "
                    "das Schwimmen zusammen, ein Radtraining am Nachmittag entfällt. Der Rad-Stufentest liegt am "
                    "Sonntag mit einem freien Samstag davor. Sportunterricht am Fr ruhig laufen, kein "
                    "Zeitlauf. Sa locker, früh schlafen, abends kohlenhydratreich essen. So 2-3 h vor "
                    "dem Test frühstücken. Ausweichtermin Mo 16.11., falls der Schlaf unter 7 h war oder "
                    "HRV/Ruhepuls auffällig sind (HRV unter ca. 78, Ruhepuls über ca. 51). Bis zum Test: kein Eisbad mehr, "
                    "Sauna höchstens Do kurz (10 min), am Sa keine Sauna und kein Eisbad.",
     "external_id": "woche-2026-11-13-testhinweis"},
    {"category": "WORKOUT", "type": "Swim", "name": "Schulevent: 4 km locker schwimmen",
     "start_date_local": "2026-11-13T00:00:00", "moving_time": 5400,
     "description": "4 km locker, kein Tempo, mehr nicht. Technik sauber, Schultern schonen.",
     "external_id": "woche-2026-11-13-24h"},
]

# Nächste Woche (16.-22.11.): Lauf-Stufentest am Mi (verschoben, Id 154094124)
# (Tag, Typ, Name, Beschreibung, Minuten)
NAECHSTE_WOCHE = [
    ("2026-11-16", "WeightTraining", "Kraft: Oberkörper und Beine (Einstieg)",
     "Wie gewohnt montags, jetzt mit Beinen. Gewichte finden, 3-4 Wiederholungen in Reserve: Goblet-Kniebeuge 2x8, "
     "Rumänisches Kreuzheben 2x8, Split Squat 2x6 je Seite, Wadenheben 2x12, dann Klimmzüge oder Latzug 3x8, "
     "Rudern 3x10, Liegestütze 3x12, Plank 3x45 s. Nach dem Rad-Stufentest vom Sonntag nicht bis zur Erschöpfung; "
     "Lauf-Stufentest ist am Mittwoch, deshalb bleiben die Beine leicht.", 50),
    ("2026-11-17", "Ride", "Rad locker",
     "Regeneration nach dem Test, Beine ausdrehen.\n- 10m ramp 45-52%\n- 30m 55%\n- 5m 50%", 45),
    ("2026-11-17", "Swim", "Vereinstraining",
     "Locker und mit Technikfokus. Morgen Lauf-Stufentest, deshalb keine Intensität.", 70),
    ("2026-11-19", "Swim", "Vereinstraining", "Wie geplant im Verein.", 70),
    ("2026-11-19", "Ride", "Rad Schlüssel: Sweet Spot (nach dem Test)",
     "Nach den Stufentests wieder Intensität. Prozente beziehen sich auf die neue FTP aus dem Rad-Stufentest vom 15.11.; "
     "Fenster Do 14:00-16:30, danach Schwimmen im Verein (17:30). Wenn die FTP noch nicht gesetzt ist, vorläufig 280 W.\n"
     "Warmup\n- 15m ramp 50-75%\n\nSweet Spot 3x\n- 12m 90%\n- 4m 55%\n\nCooldown\n- 10m 50%", 73),
    ("2026-11-19", "WeightTraining", "Kraft: Beine (nach dem Rad)",
     "Nach dem Lauf-Stufentest und dem Sweet Spot. Die Montagseinheit hatte leichte Beine, deshalb heute der Beinteil, "
     "40 min im Kraftraum nach dem Rad, RIR 3: Goblet-Kniebeuge 3x8, Rumänisches Kreuzheben 3x8, Split Squat 3x6 je Seite, "
     "Hip Thrust 3x10, Wadenheben 3x12, Plank 3x45 s. Nicht bis zum Versagen, damit die Beine am Samstag frisch sind. "
     "Danach Schwimmen im Verein (17:30).", 40),
    ("2026-11-20", "NOTE", "Ruhetag",
     "Freitag ist trainingsfrei. Morgen lange Radeinheit mit Sweet-Spot-Block, vorher gut essen und schlafen.", 0),
    ("2026-11-21", "Ride", "Rad lang mit Sweet-Spot-Block",
     "Im Gelände wie du es hast (Harz oder flach), gleiche Zonen wie im Flachen: nach Leistung fahren. Der Block ist die zweite "
     "Intensität der Woche. Essen und trinken (60 g Kohlenhydrate/h).\n"
     "Warmup\n- 10m ramp 45-57%\n\nGrundlage\n- 40m 58%\n\nSweet Spot 2x\n- 15m 90%\n- 5m 55%\n\nGrundlage\n- 35m 58%\n\nCooldown\n- 10m 50%", 135),
    ("2026-11-23", "WeightTraining", "Kraft: Beine und Oberkörper (Technik)",
     "Erste Aufbauwoche, Technik und Gewichte finden (RIR 3): Front- oder Goblet-Kniebeuge 3x8, Rumänisches "
     "Kreuzheben 3x8, Bulgarian Split Squat 3x6 je Seite, Hip Thrust 3x10, Wadenheben 3x12, danach Klimmzüge "
     "3x8, Rudern 3x10, Bankdrücken 3x8, Plank 3x45 s. Danach +2,5 kg pro Fortschritt.", 55),
    ("2026-11-25", "WeightTraining", "Kraft: Oberkörper und Core (vor dem Lauf)",
     "35 min vor den Bahnintervallen, RIR 3: Bankdrücken 3x8, Klimmzüge oder Latzug 3x8, Face Pulls "
     "2x15, Plank 3x45 s, Pallof Press 2x10 je Seite. Aktivierung: Glute Bridge 2x10, Wadenheben 2x12, 2x5 leichte "
     "Hocksprünge. Keine schweren Beine vor dem Laufen.", 35),
    ("2026-11-25", "Run", "Bahn: Einstieg 5x400 m",
     "Erste Bahneinheit nach dem Lauf-Stufentest. Paces nach dem Test anpassen, vorläufig "
     "4:15/km. Qualität vor Menge, die 5. Runde so schnell wie die erste.\n"
     "Warmup\n- 15m 6:50/km Pace\n\nIntervalle 5x\n- 400mtr 4:15/km Pace\n- 200mtr 7:15/km Pace\n\nCooldown\n- 8m 7:00/km Pace", 50),
    ("2026-11-29", "Ride", "Koppel 1: Rad locker 60 min",
     "Sonntags-Koppel Teil 1: nur Beine ausdrehen, Z1-Z2, Trittfrequenz 85-95. Danach direkt der Hügellauf (Koppel 2), "
     "Laufschuhe bereitlegen, Wechsel unter 3 min.\n- 10m ramp 45-55%\n- 40m 55%\n- 10m 50%", 60),
    ("2026-11-24", "Ride", "Rad locker",
     "Beine ausdrehen nach dem Montag, Trittfrequenz 85-95.\n- 10m ramp 45-55%\n- 70m 57%\n- 10m 50%", 90),
    ("2026-11-24", "Swim", "Vereinstraining", "Wie geplant im Verein.", 70),
    ("2026-11-26", "Ride", "Rad Schlüssel: Sweet Spot",
     "Erste Intensität nach den Tests, Prozente beziehen sich auf die neue FTP.\nWarmup\n- 15m ramp 50-75%\n\n"
     "Sweet Spot 2x\n- 15m 88%\n- 5m 55%\n\nCooldown\n- 10m 50%", 65),
    ("2026-11-26", "Swim", "Vereinstraining", "Wie geplant im Verein.", 70),
    ("2026-11-26", "WeightTraining", "Kraft: Ergänzung Beine nach dem Rad",
     "Nach dem Sweet Spot, 30-35 min, RIR 3: Single-Leg RDL 3x8 je Seite, Step-ups 3x8 je Seite, Hip Thrust 3x10, "
     "Nordic Hamstring 2x5, Wadenheben 3x12, Dead Bug 3x10, Seitstütz 2x30 s. Kein Muskelkater für den Samstag.", 35),
    ("2026-11-28", "Swim", "Schwimmen frei (Samstag)",
     "Zusätzliche freie Einheit am Samstagnachmittag, 45 min, weil Schwimmen ein Engpass ist und im Verein nur 2x70 min "
     "stehen. Technik und lockere Ausdauer: 10 min einschwimmen, 6x(50 m Technik + 50 m locker), 400 m durchgehend ruhig, "
     "4x100 m locker mit 20 s Pause, 5 min ausschwimmen. Wasserlage und Atmung vor Tempo.", 45),
    ("2026-11-28", "Ride", "Rad in den Bergen",
     "Im Harz oder flach, nach Leistung (Z2, nicht über 75 % FTP), Essen und Trinken üben.\nWarmup\n- 15m ramp 45-57%\n\nGrundlage\n- 200m 58%\n\nCooldown\n- 10m 50%", 225),
    ("2026-11-29", "Run", "Koppel 2: Hügellauf locker",
     "Sonntags-Koppel Teil 2, direkt nach dem Rad (60 min locker): die ersten 5 min bewusst ruhig, Beine finden. Hügelgelände, "
     "bergauf kräftig, bergab traben oder gehen, Puls niedrig halten.\n- 55m 6:50/km Pace", 55),
    ("2026-11-22", "Run", "Lauf locker lang",
     "Locker, 35 min: nach Lauf-Stufentest und Rad-Block bleibt der Laufumfang bei höchstens +10 % gegenüber den Läufen "
     "der Vorwochen (ohne den Test). Gern im Hügelgelände (bergauf locker, bergab traben oder gehen). "
     "Danach Dehnen/Mobilisation.\n- 35m 6:50/km Pace", 35),
]


def naechste_woche_events() -> list[dict]:
    from . import verpflegung
    out = []
    for tag, typ, name, text, minuten in NAECHSTE_WOCHE:
        ev = {"start_date_local": f"{tag}T00:00:00", "name": name, "description": text,
              "external_id": f"woche-{tag}-{name[:8].lower().replace(' ', '')}-{typ.lower()}"}
        if typ == "NOTE":
            ev["category"] = "NOTE"
        else:
            ev.update(category="WORKOUT", type=typ, moving_time=minuten * 60)
            block = verpflegung.block_fuer_event(ev)
            if block:
                ev["description"] = verpflegung.mit_block(ev["description"], block)
        out.append(ev)
    return out
