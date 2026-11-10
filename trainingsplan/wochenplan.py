"""Konkrete Einheiten für die Testwochen 09.-22.11.2026 (Phase 0) als intervals.icu-Workouts.

Zonen sind noch die alten Einstellungen (FTP 280 W, Lauf-HF-Zonen veraltet). Deshalb Rad in Prozent
mit niedriger Z2 und Laufen nach Pace (deine lockeren Läufe liegen bei 6:30-7:00/km). Nach den
Stufentests FTP, Laufschwelle, LTHR und Zonen aktualisieren.
"""

from __future__ import annotations

# Diese Woche (09.-15.11.): Einheiten, die mit dem Rad-Stufentest am Sa kollidieren oder doppelt sind.
# (Datum, Name, Grund)
ENTFERNEN = [
    ("2026-11-12", "run", "Do: Lauf 30 min gestrichen (Sportunterricht 3000 m am Fr, Rad-Stufentest am Sa)"),
    ("2026-11-14", "Technik-Schwimmen (Swim)", "Sa: Schwimmen nach dem Stufentest gestrichen (Vereinstraining deckt es ab)"),
]

# Zusätzliche Hinweise in dieser Woche
HINWEISE = [
    {"category": "NOTE", "name": "Morgen: Rad-Stufentest", "start_date_local": "2026-11-13T00:00:00",
     "description": "Nach dem 3000-m-Lauf keine weitere Einheit. Heute Abend kohlenhydratreich essen, "
                    "morgen früh 2-3 h vor dem Test frühstücken, 8 h Schlaf. Test: 14 Stufen à 4 min "
                    "ab 140 W, bis zur Erschöpfung, dann LAP bis zum Ausfahren. Sekunden in der letzten "
                    "Stufe notieren.",
     "external_id": "woche-2026-11-13-testhinweis"},
]

# Nächste Woche (16.-22.11.): Lauf-Stufentest steht bereits am Di (Id 154094124)
# (Tag, Typ, Name, Beschreibung, Minuten)
NAECHSTE_WOCHE = [
    ("2026-11-16", "WeightTraining", "Kraft: Beine und Core",
     "Kniebeuge 3x8, Rumänisches Kreuzheben 3x8, Ausfallschritte 3x10 je Seite, Plank 3x45 s, "
     "Seitstütz 2x30 s je Seite. Mittlere Last (2 Wiederholungen in Reserve), Technik vor Gewicht, "
     "damit der Lauftest am Di nicht leidet.", 45),
    ("2026-11-17", "Swim", "Vereinstraining",
     "Nach dem Lauf-Stufentest: nur locker, Technik, keine Intervalle, Beine ausschütteln.", 70),
    ("2026-11-18", "Ride", "Rad Grundlage",
     "Warmup\n- 10m ramp 45-57%\n\nGrundlage, Trittfrequenz 85-95\n- 40m 57%\n\nCooldown\n- 10m 50%", 60),
    ("2026-11-19", "Swim", "Vereinstraining", "Wie geplant im Verein.", 70),
    ("2026-11-19", "Run", "Lauf locker",
     "Locker, nach dem Schwimmen oder davor, Puls niedrig halten.\n- 30m 6:50/km Pace", 30),
    ("2026-11-21", "Ride", "Rad Grundlage lang",
     "Warmup\n- 10m ramp 45-57%\n\nGrundlage, Trittfrequenz 85-95, essen und trinken (60 g Kohlenhydrate/h)\n"
     "- 70m 58%\n\nCooldown\n- 10m 50%", 90),
    ("2026-11-22", "Run", "Lauf locker lang",
     "Der längste Lauf der Woche, ruhig. Danach Dehnen/Mobilisation.\n- 45m 6:50/km Pace", 45),
    ("2026-11-20", "NOTE", "Ruhetag",
     "Frei oder 20 min Mobilisation. Morgen lange Radeinheit, vorher gut essen und schlafen.", 0),
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
