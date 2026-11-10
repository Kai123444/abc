"""Konkrete Einheiten für die Testwochen 09.-22.11.2026 (Phase 0) als intervals.icu-Workouts.

Sonderfall dieser Woche: 24-Stunden-Schwimmen der Schule von Fr 13.11. bis Sa 14.11. (4 km locker).
Deshalb liegt der Rad-Stufentest am So 15.11. und der Lauf-Stufentest am Mi 18.11. (3 Tage Abstand).

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
    ("2026-11-19", "Lauf locker", "Do: nach dem Lauftest kein Lauf"),
]

# Verschieben/ändern: (altes Datum, Name, neues Datum, geänderte Felder)
VERSCHIEBEN = [
    ("2026-11-14", "Rad-Stufentest", "2026-11-15", {}),
    ("2026-11-15", "Ruhiger Dauerlauf (Run)", "2026-11-14",
     {"name": "Lauf locker (optional)", "moving_time": 1800,
      "description": "Nach dem Schlafen, nur wenn du dich frisch fühlst, sonst frei.\n- 30m 6:50/km Pace"}),
    ("2026-11-11", "Ride", "2026-11-11",
     {"moving_time": 2700, "description": "Grundlage, locker, Trittfrequenz 85-95\n- 45m 57%"}),
    ("2026-11-17", "Lauf-Stufentest", "2026-11-18", {}),
]

# Neue Einheiten und Hinweise dieser Woche
DIESE_WOCHE = [
    {"category": "NOTE", "name": "Fr bis Sa: 24-h-Schwimmen, So: Rad-Stufentest",
     "start_date_local": "2026-11-13T00:00:00",
     "description": "Der Rad-Stufentest liegt am Sonntag, damit du nach dem Event schlafen und dich erholen kannst. "
                    "Während der 24 h: locker schwimmen (nicht schneller als ca. 2:10/100 m), Schultern warm "
                    "halten, regelmäßig essen und trinken (Kohlenhydrate, Salz), zwischendurch schlafen, wenn möglich. "
                    "Sa: nach dem Event mindestens 8-9 h schlafen, abends kohlenhydratreich essen. Sportunterricht "
                    "am Fr ruhig laufen, kein Zeitlauf. So früh genug frühstücken (2-3 h vor dem Test). "
                    "Ausweichtermin Mo 16.11., falls dein Schlaf unter 7 h war oder HRV/Ruhepuls auffällig sind "
                    "(HRV unter ca. 78, Ruhepuls über ca. 51).",
     "external_id": "woche-2026-11-13-testhinweis"},
    {"category": "WORKOUT", "type": "Swim", "name": "24-Stunden-Schwimmen (Schule), 4 km",
     "start_date_local": "2026-11-13T00:00:00", "moving_time": 5400,
     "description": "4 km locker, verteilt über die 24 h. Technik sauber, kein Tempo, Schultern schonen.",
     "external_id": "woche-2026-11-13-24h"},
    {"category": "WORKOUT", "type": "Ride", "name": "Rad Grundlage (Freitag, Sondertraining)",
     "start_date_local": "2026-11-13T00:00:00", "moving_time": 3600,
     "description": "Möglichst am Vormittag, vor dem Event. Locker, damit der Sonntag frisch bleibt.\n"
                    "Warmup\n- 10m ramp 45-55%\n\nGrundlage, Trittfrequenz 85-95\n- 40m 58%\n\nCooldown\n- 10m 50%",
     "external_id": "woche-2026-11-13-radgrundlage"},
]

# Nächste Woche (16.-22.11.): Lauf-Stufentest am Mi (verschoben, Id 154094124)
# (Tag, Typ, Name, Beschreibung, Minuten)
NAECHSTE_WOCHE = [
    ("2026-11-16", "WeightTraining", "Kraft: Oberkörper und Core",
     "Beine schonen nach dem Rad-Stufentest. Klimmzüge/Rudern 3x8, Liegestütze 3x12, Schulterdrücken 3x10, "
     "Plank 3x45 s, Seitstütz 2x30 s je Seite, Rückenstrecker 2x12.", 40),
    ("2026-11-17", "Ride", "Rad locker",
     "Regeneration nach dem Test, Beine ausdrehen.\n- 10m ramp 45-52%\n- 30m 55%\n- 5m 50%", 45),
    ("2026-11-17", "Swim", "Vereinstraining",
     "Locker und mit Technikfokus. Morgen Lauf-Stufentest, deshalb keine Intensität.", 70),
    ("2026-11-19", "Swim", "Vereinstraining", "Wie geplant im Verein.", 70),
    ("2026-11-20", "NOTE", "Ruhetag",
     "Frei oder 20 min Mobilisation. Morgen lange Radeinheit, vorher gut essen und schlafen.", 0),
    ("2026-11-21", "Ride", "Rad Grundlage lang",
     "Warmup\n- 10m ramp 45-57%\n\nGrundlage, Trittfrequenz 85-95, essen und trinken (60 g Kohlenhydrate/h)\n"
     "- 100m 58%\n\nCooldown\n- 10m 50%", 120),
    ("2026-11-22", "Run", "Lauf locker lang",
     "Der längste Lauf der Woche, ruhig. Danach Dehnen/Mobilisation.\n- 45m 6:50/km Pace", 45),
]


def naechste_woche_events() -> list[dict]:
    out = []
    for tag, typ, name, text, minuten in NAECHSTE_WOCHE:
        ev = {"start_date_local": f"{tag}T00:00:00", "name": name, "description": text,
              "external_id": f"woche-{tag}-{name[:8].lower().replace(' ', '')}-{typ.lower()}"}
        if typ == "NOTE":
            ev["category"] = "NOTE"
        else:
            ev.update(category="WORKOUT", type=typ, moving_time=minuten * 60)
        out.append(ev)
    return out
