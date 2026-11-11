"""Workout-Bibliothek für intervals.icu: alle Einheiten des Plans, sinnvoll in Ordnern sortiert.

Ordner sind nummeriert, weil intervals.icu keine verschachtelten Ordner kennt: 0x Rad, 1x Lauf, 20 Koppel,
30 Schwimmen, 40 Kraft, 50 Rennen. Alle Einheiten stehen in der Syntax von intervals.icu ("m" = Minuten,
"mtr" = Meter, Rad in % FTP, Lauf nach Pace) und tragen Tags (Phase, Gelände, Art). Zonen und Paces gelten bis
zu den Stufentests (Rad 15.11., Lauf 18.11.) vorläufig und werden danach angepasst.
"""

from __future__ import annotations

from . import verpflegung as vp
from .stufentest import lauf_stufentest, rad_stufentest
from datetime import date

ORDNER = [
    "01 Rad - Grundlage Z2",
    "02 Rad - Lange Ausfahrt mit Block",
    "03 Rad - Sweet Spot",
    "04 Rad - Schwelle und Over-Unders",
    "05 Rad - VO2max",
    "06 Rad - Renntempo und Zeitfahren",
    "07 Rad - Tests",
    "10 Lauf - Bahnintervalle",
    "11 Lauf - Dauerlauf, Huegel, lang",
    "12 Lauf - Tests",
    "20 Koppel und Brick",
    "30 Schwimmen",
    "40 Kraft",
    "50 Rennen und Generalproben",
    "90 Weitere (aus dem Kalender)",
]


def _z2(minuten: int, wu: int = 15, cd: int = 10, pct: int = 58) -> str:
    return f"Warmup\n- {wu}m ramp 45-57%\n\nZ2, Trittfrequenz 85-95\n- {minuten - wu - cd}m {pct}%\n\nCooldown\n- {cd}m 50%"


def _block(titel: str, reps: int, arbeit: int, pct: str, pause: int, pause_pct: int = 55) -> str:
    if reps == 1:
        return f"{titel}\n- {arbeit}m {pct}%"
    return f"{titel} {reps}x\n- {arbeit}m {pct}%\n- {pause}m {pause_pct}%"


def _rad_intervall(wu: int, bloecke: list[str], cd: int = 10) -> str:
    return f"Warmup\n- {wu}m ramp 50-75%\n\n" + "\n\n".join(bloecke) + f"\n\nCooldown\n- {cd}m 50%"


def _lang_mit_block(minuten: int, block: str, vor: int, wu: int = 15, cd: int = 10) -> str:
    nach = minuten - wu - cd - vor - _dauer(block)
    return (f"Warmup\n- {wu}m ramp 45-57%\n\nZ2\n- {vor}m 58%\n\n{block}\n\nZ2\n- {nach}m 58%\n\n"
            f"Cooldown\n- {cd}m 50%")


def _dauer(block: str) -> int:
    """Gesamtdauer eines Blocks aus '- Xm ...'-Zeilen (nur für die Zeitplanung der langen Fahrten)."""
    import re
    summe = 0
    reps = 1
    kopf = block.splitlines()[0]
    m = re.search(r"(\d+)x$", kopf)
    if m:
        reps = int(m.group(1))
    zeilen = [int(x) for x in re.findall(r"^- (\d+)m", block, re.M)]
    return reps * sum(zeilen) if m else sum(zeilen)


def _bahn(reps: int, meter: int, pace: str, pause_m: int, pause_pace: str, name: str, wu: int = 15, cd: int = 8) -> str:
    return (f"Warmup\n- {wu}m 6:50/km Pace\n\nIntervalle {reps}x\n- {meter}mtr {pace}/km Pace\n- {pause_m}mtr {pause_pace}/km Pace\n\n"
            f"Cooldown\n- {cd}m 7:00/km Pace")


# (Ordner, Name, Typ, Beschreibung, Tags, erwartete Minuten)
def _liste() -> list[tuple[str, str, str, str, list[str], int]]:
    w: list[tuple[str, str, str, str, list[str], int]] = []
    add = lambda o, n, t, d, tags, m: w.append((ORDNER[o], n, t, d, tags, m))

    # ---------------- 01 Rad Grundlage ----------------
    add(0, "Erholung 45 min", "Ride", "Nur Beine ausdrehen, Puls unter 130.\n" + _z2(45, 10, 5, 50), ["Rad", "Z2", "Erholung"], 45)
    add(0, "Rad Hitze-Anpassung 60 min", "Ride", "Hitzetraining für die DM: Rolle im warmen Raum (28-32 Grad), ohne Ventilator oder mit langer Kleidung. Gewicht vor und nach wiegen, Verlust höchstens 2 %, Wasser mit 500-1000 mg Natrium pro Stunde. Puls steigt, Leistung nicht erhöhen.\n" + _z2(60, 10, 10, 57), ["Rad", "Z2", "Hitze"], 60)
    add(0, "Z2 60 min", "Ride", _z2(60, 10, 10, 57), ["Rad", "Z2", "Gelände egal"], 60)
    add(0, "Z2 90 min", "Ride", _z2(90, 10, 10, 57), ["Rad", "Z2", "Gelände egal"], 90)
    add(0, "Z2 120 min", "Ride", _z2(120, 15, 10, 58), ["Rad", "Z2", "Gelände egal"], 120)
    add(0, "Z2 180 min", "Ride", _z2(180, 15, 10, 58), ["Rad", "Z2", "Gelände egal", "Darmtraining"], 180)
    add(0, "Z2 225 min (Berge)", "Ride", _z2(225, 15, 10, 58), ["Rad", "Z2", "Berge", "Darmtraining"], 225)
    add(0, "Z2 240 min", "Ride", _z2(240, 15, 10, 58), ["Rad", "Z2", "Gelände egal", "Darmtraining"], 240)
    add(0, "Kadenz-Grundlage 72 min", "Ride",
        "Warmup\n- 15m ramp 50-65%\n\nKadenz 6x\n- 1m 68% 105rpm\n- 6m 65%\n\nCooldown\n- 15m 55%", ["Rad", "Kadenz", "Z2"], 72)
    add(0, "MTB locker 72 min", "MountainBikeRide", "Locker und gleichmäßig, Puls unter 150, keine Intervalle.\n- 72m 55%",
        ["Rad", "MTB", "Z2"], 72)

    # ---------------- 02 Lange Ausfahrt mit Block ----------------
    add(1, "Lang 180 min + Sweet Spot 1x30 (Phase 1)", "Ride", _lang_mit_block(180, "Sweet Spot\n- 30m 90%", 60),
        ["Rad", "Phase 1", "Sa", "Gelände egal"], 180)
    add(1, "Lang 210 min + Sweet Spot 2x20 (Phase 2)", "Ride", _lang_mit_block(210, _block("Sweet Spot", 2, 20, "90", 5), 70),
        ["Rad", "Phase 2", "Sa", "Gelände egal"], 210)
    add(1, "Lang 210 min + Schwelle 3x15 (Phase 2)", "Ride", _lang_mit_block(210, _block("Schwelle", 3, 15, "97", 5), 70),
        ["Rad", "Phase 2", "Sa", "Gelände egal"], 210)
    add(1, "Lang 240 min + Tempo 2x30 (Phase 3)", "Ride", _lang_mit_block(240, _block("Tempo", 2, 30, "90", 8), 80),
        ["Rad", "Phase 3", "Sa", "Gelände egal"], 240)
    add(1, "Lang 240 min + Schwelle 3x15 (Phase 3)", "Ride", _lang_mit_block(240, _block("Schwelle", 3, 15, "97", 5), 80),
        ["Rad", "Phase 3", "Sa", "Gelände egal"], 240)
    add(1, "Lang 210 min + Renntempo 40 km flach (Phase 4)", "Ride", _lang_mit_block(210, "Renntempo flach, Rennposition\n- 62m 90%", 60),
        ["Rad", "Phase 4", "Sa", "flach", "Renntempo"], 210)

    # ---------------- 03 Sweet Spot ----------------
    for reps, arbeit, pause, tag in ((2, 20, 5, "Phase 1"), (2, 25, 5, "Phase 1"), (3, 15, 5, "Phase 1"), (3, 20, 5, "Phase 1")):
        gesamt = 15 + reps * arbeit + (reps - 1) * pause + 10
        add(2, f"Sweet Spot {reps}x{arbeit}", "Ride", _rad_intervall(15, [_block("Sweet Spot", reps, arbeit, "88-93", pause)]),
            ["Rad", "Intervall", "Sweet Spot", tag, "Do", "flach"], gesamt)
    add(2, "Sweet Spot 60 min am Stück", "Ride", _rad_intervall(15, ["Sweet Spot\n- 60m 90%"]), ["Rad", "Intervall", "Sweet Spot", "Phase 2", "flach"], 85)
    add(2, "Sweet Spot / Tempo 2x25-30 (Phase 3)", "Ride", _rad_intervall(15, [_block("Tempo", 2, 28, "88-93", 6)]),
        ["Rad", "Intervall", "Sweet Spot", "Phase 3", "Di", "flach"], 15 + 2 * 28 + 6 + 10)

    # ---------------- 04 Schwelle und Over-Unders ----------------
    for reps, arbeit, pause in ((2, 20, 5), (3, 15, 5), (2, 25, 6), (4, 12, 4)):
        gesamt = 15 + reps * arbeit + (reps - 1) * pause + 10
        add(3, f"Schwelle {reps}x{arbeit}", "Ride", _rad_intervall(15, [_block("Schwelle", reps, arbeit, "95-100", pause)]),
            ["Rad", "Intervall", "Schwelle", "Phase 2", "Do", "flach"], gesamt)
    add(3, "Schwelle 3x12 bei 100 % (Phase 4)", "Ride", _rad_intervall(15, [_block("Schwelle", 3, 12, "100", 5)]),
        ["Rad", "Intervall", "Schwelle", "Phase 4", "Di", "flach"], 15 + 3 * 12 + 2 * 5 + 10)
    add(3, "Over-Unders 3x(6+6)", "Ride",
        _rad_intervall(15, ["Over-Unders 3x\n- 6m 95%\n- 6m 105%\n- 5m 55%"]),
        ["Rad", "Intervall", "Over-Unders", "Phase 2", "Di", "flach"], 15 + 3 * 17 + 10)

    # ---------------- 05 VO2max ----------------
    for reps, arbeit, pause in ((5, 4, 4), (5, 5, 5), (6, 4, 4)):
        gesamt = 20 + reps * arbeit + (reps - 1) * pause + 10
        add(4, f"VO2max {reps}x{arbeit}", "Ride", _rad_intervall(20, [_block("VO2max", reps, arbeit, "110-120", pause, 50)]),
            ["Rad", "Intervall", "VO2max", "Phase 3", "Do", "flach"], gesamt)
    add(4, "VO2max 4x4 zur Frische (Phase 4)", "Ride", _rad_intervall(20, [_block("VO2max", 4, 4, "112-118", 4, 50)]),
        ["Rad", "Intervall", "VO2max", "Phase 4", "Di", "flach"], 20 + 4 * 4 + 3 * 4 + 10)
    add(4, "30/30 3x8", "Ride", _rad_intervall(20, ["Serie 3x\n- 30s 120%\n- 30s 50%\n- 30s 120%\n- 30s 50%\n- 30s 120%\n- 30s 50%\n- 30s 120%\n- 30s 50%\n- 5m 55%"]),
        ["Rad", "Intervall", "VO2max", "30/30", "Phase 3", "flach"], 20 + 3 * 9 + 10)

    # ---------------- 06 Renntempo und Zeitfahren ----------------
    add(5, "Renntempo 2x20 (Phase 4)", "Ride", _rad_intervall(20, [_block("Renntempo flach, Rennposition", 2, 20, "95-100", 5)]),
        ["Rad", "Renntempo", "Phase 4", "Do", "flach"], 20 + 45 + 10)
    add(5, "Renntempo 3x15 (Phase 4)", "Ride", _rad_intervall(20, [_block("Renntempo flach, Rennposition", 3, 15, "95-100", 5)]),
        ["Rad", "Renntempo", "Phase 4", "Do", "flach"], 20 + 55 + 10)
    add(5, "Renntempo 40 km (Phase 4)", "Ride", _rad_intervall(20, ["Renntempo 40 km, Rennposition, 6-8 Wenden\n- 62m 90%"]),
        ["Rad", "Renntempo", "Phase 4", "Do", "flach", "Zeitfahren"], 20 + 62 + 10)
    add(5, "Aero-Gewöhnung 20/40/60 min", "Ride", _rad_intervall(15, ["Aeroposition 20 min, später 40 und 60 min am Stück\n- 20m 80%"]),
        ["Rad", "Aero", "Zeitfahrrad", "flach"], 15 + 20 + 10)

    # ---------------- 07 Rad Tests ----------------
    rt = rad_stufentest(date(2026, 11, 15))
    add(6, "Rad-Stufentest 14 Stufen à 4 min", "Ride", rt.beschreibung, ["Rad", "Test", "FTP", "Stufentest"], rt.dauer_min)
    rr = rad_stufentest(date(2026, 11, 15), modus="rampe")
    add(6, "Rad-Rampentest (Lap beendet)", "Ride", rr.beschreibung, ["Rad", "Test", "Rampe"], rr.dauer_min)
    add(6, "Zeitfahrtest 40 km", "Ride",
        "Do 13.05. in der Erholungswoche, flach, solo, Rennposition, gleichmäßig so schnell wie möglich.\nWarmup\n- 20m ramp 50-80%\n\n"
        "Test\n- 62m 100%\n\nCooldown\n- 10m 50%", ["Rad", "Test", "Zeitfahren", "flach"], 92)
    add(6, "FTP-Test 20 min", "Ride", "Warmup\n- 20m ramp 50-80%\n\nAnlauf\n- 5m 100%\n- 5m 55%\n\nTest\n- 20m 100%\n\nCooldown\n- 10m 50%",
        ["Rad", "Test", "FTP"], 60)

    # ---------------- 10 Lauf Bahnintervalle ----------------
    for reps, pace, name, tag in ((5, "4:15", "Einstieg", "Phase 1"), (6, "4:10", "Aufbau", "Phase 1"), (8, "4:10", "Aufbau", "Phase 1"),
                                  (10, "4:05", "Aufbau", "Phase 1"), (12, "4:00", "Phase 2", "Phase 2")):
        add(7, f"Bahn {reps}x400 ({name})" if name != "Phase 2" else f"Bahn {reps}x400",
            "Run", _bahn(reps, 400, pace, 200, "7:15", f"{reps}x400 m"), ["Lauf", "Bahn", "Intervall", tag, "Mi"],
            15 + int(reps * (400 * (int(pace[0]) * 60 + int(pace[2:])) / 1000 + 90) / 60) + 8)
    add(7, "Bahn 5x600", "Run", _bahn(5, 600, "4:05", 200, "7:15", "5x600 m"), ["Lauf", "Bahn", "Intervall", "Phase 1", "Mi"], 45)
    add(7, "Bahn 3x800", "Run", _bahn(3, 800, "4:00", 400, "6:00", "3x800 m"), ["Lauf", "Bahn", "Intervall", "Phase 2", "Mi"], 45)
    add(7, "Bahn 4x1000 (Schwellenpace)", "Run", _bahn(4, 1000, "4:12", 400, "6:00", "4x1000 m"), ["Lauf", "Bahn", "Schwelle", "Phase 2", "Mi"], 50)
    add(7, "Bahn 6x1 km (3-5-km-Tempo)", "Run", _bahn(6, 1000, "4:00", 400, "6:00", "6x1 km"), ["Lauf", "Bahn", "Intervall", "Phase 3", "Mi"], 60)

    # ---------------- 11 Lauf locker, Hügel, lang ----------------
    for m_, n_ in ((30, "Lauf locker 30 min"), (45, "Lauf locker 45 min"), (60, "Lauf locker 60 min")):
        add(8, n_, "Run", f"Locker, Puls niedrig.\n- {m_}m 6:50/km Pace", ["Lauf", "locker"], m_)
    add(8, "Lauf Hitze-Anpassung 40 min", "Run", "Hitzetraining für die DM: lockerer Lauf mittags bei Sommerwärme oder mit langer Kleidung und Mütze. Tempo nicht erhöhen, Puls steigt. Gewicht vor/nach wiegen, Trinkflasche mitnehmen, Verlust höchstens 2 %.\n- 40m 6:55/km Pace", ["Lauf", "locker", "Hitze"], 40)
    add(8, "Hügellauf locker 55 min", "Run", "Hügelgelände, bergauf kräftig, bergab traben oder gehen.\n- 55m 6:50/km Pace",
        ["Lauf", "Hügel", "Sonntag"], 55)
    for m_ in (75, 90, 100):
        add(8, f"Langer Lauf {m_} min", "Run", f"Hügelgelände, bergab kontrolliert.\n- {m_}m 6:45/km Pace", ["Lauf", "lang", "Sonntag"], m_)
    add(8, "Steigerungsläufe 6x20 s", "Run", "Warmup\n- 15m 6:50/km Pace\n\nSteigerungen 6x\n- 20s 3:50/km Pace\n- 60s 8:00/km Pace\n\nCooldown\n- 10m 7:00/km Pace",
        ["Lauf", "Technik", "Phase 1"], 30)
    add(8, "Bergläufe 8x60 s", "Run", "Warmup\n- 15m 6:50/km Pace\n\nBerg 8x\n- 60s 4:00/km Pace\n- 90s 8:00/km Pace\n\nCooldown\n- 10m 7:00/km Pace",
        ["Lauf", "Berg", "Phase 2", "Sonntag"], 40)

    # ---------------- 12 Lauf Tests ----------------
    lt = lauf_stufentest(date(2026, 11, 18))
    add(9, "Lauf-Stufentest 11 Stufen à 4 min", "Run", lt.beschreibung, ["Lauf", "Test", "LTHR", "Stufentest"], lt.dauer_min)

    # ---------------- 20 Koppel und Brick ----------------
    add(10, "Koppel A1: Rad locker 60 min (Sonntag)", "Ride", "Teil 1 des Sonntags-Koppels, direkt danach der Lauf.\n" + _z2(60, 10, 10, 55),
        ["Koppel", "Rad", "Sonntag", "Z2"], 60)
    add(10, "Koppel A2: Lauf locker 60 min (Sonntag)", "Run", "Teil 2 direkt nach dem Rad, die ersten 5 min bewusst ruhig.\n- 60m 6:50/km Pace",
        ["Koppel", "Lauf", "Sonntag"], 60)
    add(10, "Koppel A2: Lauf 75 min Hügel (Sonntag)", "Run", "Teil 2 direkt nach dem Rad, Hügelgelände.\n- 75m 6:45/km Pace", ["Koppel", "Lauf", "Sonntag", "Hügel"], 75)
    add(10, "Koppel B: Kurzer Lauf 10-15 min (nach Do-Rad)", "Run", "Direkt nach den Intervallen, erste 5 min kontrolliert, dann Renn-Gefühl.\n- 12m 4:30/km Pace",
        ["Koppel", "Lauf", "Do", "Phase 3"], 12)
    add(10, "Koppel B: Kurzer Lauf 15-20 min (nach Do-Rad)", "Run", "Direkt nach den Intervallen, erste 5 min kontrolliert, dann Renntempo.\n- 18m 4:25/km Pace",
        ["Koppel", "Lauf", "Do", "Phase 4"], 18)
    add(10, "Renn-Brick Rad: 40 min bei 85-90 %", "Ride", _rad_intervall(15, ["Renn-Brick Rad, flach, Rennposition\n- 40m 88%"], 5),
        ["Koppel", "Brick", "Rad", "Phase 4", "flach"], 60)
    add(10, "Renn-Brick Lauf: 10 km im Renntempo", "Run", "Direkt nach dem Rad, erste 2 km kontrolliert, Wechsel stoppen (Ziel unter 1:00).\n- 2000mtr 4:30/km Pace\n- 8000mtr 4:20/km Pace",
        ["Koppel", "Brick", "Lauf", "Phase 4", "Renntempo"], 44)
    add(10, "Mitteldistanz-Brick Rad: 100 km (Harz)", "Ride", _z2(190, 15, 10, 74).replace("Z2, Trittfrequenz 85-95", "Mitteldistanz-Tempo, 70-78 % FTP"),
        ["Koppel", "Brick", "Hölle von Q", "Harz", "Rad"], 190)
    add(10, "Mitteldistanz-Brick Lauf: 10-14 km", "Run", "Direkt nach dem Rad, kontrolliert, Verpflegung wie im Rennplan.\n- 70m 5:00/km Pace",
        ["Koppel", "Brick", "Hölle von Q", "Lauf"], 70)

    # ---------------- 30 Schwimmen ----------------
    add(11, "Vereinstraining 70 min", "Swim", "Wie geplant im Verein.", ["Schwimmen", "Verein", "Di", "Do"], 70)
    add(11, "Schwimmen Technik 45 min", "Swim",
        "Einschwimmen\n- 300mtr Z1 Pace\n\nTechnik 6x\n- 50mtr Z1 Pace\n- 20s Pause\n\nLage 4x\n- 100mtr Z2 Pace\n- 20s Pause\n\nAusschwimmen\n- 200mtr Z1 Pace",
        ["Schwimmen", "Technik"], 36)
    add(11, "CSS-Sätze 10x100", "Swim", "Einschwimmen\n- 400mtr Z1 Pace\n\nCSS 10x\n- 100mtr 100% Pace\n- 15s Pause\n\nAusschwimmen\n- 200mtr Z1 Pace",
        ["Schwimmen", "CSS", "Phase 2"], 40)
    add(11, "CSS-Sätze 8x200 (Phase 3)", "Swim", "Einschwimmen\n- 400mtr Z1 Pace\n\nCSS 8x\n- 200mtr 100% Pace\n- 20s Pause\n\nAusschwimmen\n- 200mtr Z1 Pace",
        ["Schwimmen", "CSS", "Phase 3"], 60)
    add(11, "CSS-Test 400 m und 200 m", "Swim", "Einschwimmen\n- 400mtr Z1 Pace\n\nTest 400\n- 400mtr Z4 Pace\n- 10m Pause\n\nTest 200\n- 200mtr Z5 Pace\n\nAusschwimmen\n- 200mtr Z1 Pace",
        ["Schwimmen", "Test", "CSS"], 45)
    add(11, "Freiwasser 1,5 km am Stück", "OpenWaterSwim", "Mit und ohne Neopren, Bojenwenden, Pulk, bei Wind/Wellen.\n- 1500mtr Z2 Pace",
        ["Schwimmen", "Freiwasser", "Phase 4", "DM"], 35)
    add(11, "Schulevent: 4 km locker", "Swim", "4 km locker, kein Tempo, mehr nicht.\n- 4000mtr Z1 Pace", ["Schwimmen", "locker"], 115)

    # ---------------- 40 Kraft ----------------
    add(12, "Kraft Mo Phase 1: Beine + Oberkörper", "WeightTraining",
        "Beine: Kniebeuge (Front/Goblet) 3x8, Rumänisches Kreuzheben 3x8, Bulgarian Split Squat 3x8 je Seite, Hip Thrust 3x10, "
        "Wadenheben 3x12-15, Tibialis-Raises 2x15. RIR 2-3.\nOberkörper: Klimmzüge oder Latzug 3x8, Rudern 3x10, Plank 3x45 s.",
        ["Kraft", "Mo", "Phase 1", "Beine"], 60)
    add(12, "Kraft Mo Phase 2: Maximalkraft Beine", "WeightTraining",
        "Kniebeuge 3-4x4-6 bei 80-87 % 1RM, Trap-Bar-/Kreuzheben (nie bis zum Versagen), Step-ups 3x6 je Seite, Nordic Hamstring 2x5, "
        "Wadenheben 4x8. Oberkörper kurz: Klimmzüge/Rudern 3x5. RIR 1-2.", ["Kraft", "Mo", "Phase 2", "Beine"], 60)
    add(12, "Kraft Mo Phase 3-4: Erhalt", "WeightTraining",
        "Beine 2-3x3-5 bei 85 %, Sprünge 3x5, Oberkörper kurz. 35-40 min.", ["Kraft", "Mo", "Phase 3", "Phase 4"], 40)
    add(12, "Kraft Mi: Oberkörper, Core, Aktivierung (vor dem Lauf)", "WeightTraining",
        "Bankdrücken 3x8, Klimmzüge oder Latzug 3x8, Schulterdrücken 3x10, Face Pulls 2x15, Pallof Press 2x10, Seitstütz 2x30 s. "
        "Aktivierung: Glute Bridge 2x10, Wadenheben 2x12, 2x5 leichte Hocksprünge. Keine schweren Beine.", ["Kraft", "Mi", "Phase 1"], 38)
    add(12, "Stabi und Fußkraft Stufe 1 (30 min)", "WeightTraining",
        "Freitagabend, RIR 2-3. Fuß: Wadenheben einbeinig auf der Stufe 3x12 (3 s ab, Knie gestreckt) und 3x12 mit gebeugtem Knie, "
        "Tibialis-Raises 3x15, Short Foot 2x10 (8 s halten). Hüfte: Single-Leg Glute Bridge 3x10, Lateral Band Walk 3x12 je Seite, "
        "Copenhagen Plank kurz 3x20 s, Seitstütz mit Abduktion 3x10. Core: Dead Bug mit Band 3x8, Pallof Press 3x10, Hollow Hold 3x20 s, "
        "Einbeinstand auf instabiler Unterlage 3x30 s.", ["Kraft", "Stabi", "Fuß", "Phase 1"], 30)
    add(12, "Stabi und Fußkraft Stufe 2 (35 min)", "WeightTraining",
        "Wadenheben einbeinig mit 15-20 kg 3x10 (3 s ab, 1 s oben), Single-Leg RDL mit Kurzhantel 3x8, seitliche Step-downs 3x8, "
        "Copenhagen Plank voll 3x20 s, Reverse Nordic 2x8, Pogo-Sprünge 3x20 (aufwärmen), Pallof Press mit Rotation 3x10, "
        "Hollow Rock 3x12, Bird Dog mit Gewicht 3x8.", ["Kraft", "Stabi", "Fuß", "Phase 2"], 35)
    add(12, "Stabi und Fußkraft Stufe 3 (Erhalt, 20 min)", "WeightTraining",
        "Pogo-Sprünge 3x15, Einbeinsprünge 3x6, Wadenheben einbeinig 3x8 schwer, Copenhagen 2x20 s, Anti-Rotation Core 2x10, "
        "Lauf-ABC Skippings 3x20 m. Nicht in den 7 Tagen vor Rennen.", ["Kraft", "Stabi", "Fuß", "Phase 3", "Phase 4"], 20)
    add(12, "Mobilisation und Stabi leicht (25 min)", "WeightTraining",
        "Für Ruhe- und Erholungstage: Hüftbeuger-Dehnung 2x45 s je Seite, Waden 2x45 s, Gesäß/Piriformis 2x45 s, BWS-Rotation 2x8, "
        "Brust offen 2x45 s. Dann Core leicht: Dead Bug 2x8, Seitstütz 2x25 s, Glute Bridge 2x12. Fuß: Short Foot 2x10.",
        ["Kraft", "Mobilisation", "Erholung"], 25)
    add(12, "Core 20 min", "WeightTraining", "Plank 3x45 s, Seitstütz 2x30 s je Seite, Pallof Press 2x10 je Seite, Rückenstrecker 2x12.", ["Kraft", "Core"], 20)

    # ---------------- 50 Rennen und Generalproben ----------------
    add(13, "DM Kurzdistanz - Renntag (NordseeMan Wilhelmshaven)", "Other",
        "08.08.2027, Start 11:30. 1,5 km Hafenbecken, 40 km flach windschattenfrei, 10 km Wendepunktstrecke.\nSiehe Kalender: Strecken, Zeitplan, Verpflegung 130 g/h Rad und 100 g/h Lauf.",
        ["Rennen", "A", "DM"], 140)
    add(13, "Cottbus Olympische Distanz - Generalprobe", "Other", "12.06.2027, B-Rennen. Rad 130 g/h, Lauf 95 g/h, Mini-Taper Mi-Fr.", ["Rennen", "B", "Cottbus"], 140)
    add(13, "Hölle von Q - Mitteldistanz", "Other", "05.09.2027, B-Rennen im Harz. Rad 115 g/h, Lauf 80 g/h.", ["Rennen", "B", "Hölle von Q"], 300)
    return w


def workouts() -> list[dict]:
    """Bibliothekseinträge mit Verpflegungsblock (nur bei Rad/Lauf ab 60 min, Kraft/Schwimmen/Rennen ebenfalls)."""
    out = []
    for ordner, name, typ, text, tags, minuten in _liste():
        ev = {"category": "WORKOUT", "type": typ, "name": name, "moving_time": minuten * 60, "description": text}
        block = vp.block_fuer_event(ev) if not ordner.startswith("50") else None
        beschr = vp.mit_block(text, block) if block else text
        out.append({"ordner": ordner, "name": name, "type": typ, "description": beschr, "tags": tags, "minuten": minuten})
    return out


def _ordner_fuer_event(ev: dict) -> str:
    n = (ev.get("name") or "").lower()
    t = ev.get("type") or ""
    if t in ("Ride", "VirtualRide", "MountainBikeRide", "GravelRide"):
        if "test" in n:
            return ORDNER[6]
        if "sweet" in n:
            return ORDNER[2]
        if "schwelle" in n or "over" in n:
            return ORDNER[3]
        if "vo2" in n:
            return ORDNER[4]
        if "renntempo" in n or "zeitfahr" in n:
            return ORDNER[5]
        if "koppel" in n or "brick" in n:
            return ORDNER[10]
        if "block" in n:
            return ORDNER[1]
        return ORDNER[0]
    if t == "Run":
        if "stufentest" in n:
            return ORDNER[9]
        if "bahn" in n or "intervall" in n:
            return ORDNER[7]
        if "koppel" in n or "brick" in n:
            return ORDNER[10]
        return ORDNER[8]
    if t in ("Swim", "OpenWaterSwim"):
        return ORDNER[11]
    if t == "WeightTraining":
        return ORDNER[12]
    return ORDNER[14]


def anwenden(client, apply: bool, kalender: list[dict]) -> dict:
    """Ordner und Workouts in die Bibliothek schreiben. Bestehende Einträge (gleicher Ordner und Name) werden aktualisiert.
    kalender: WORKOUT-Events aus dem Kalender, die zusätzlich einsortiert werden (nur wenn der Name noch fehlt)."""
    items = workouts()
    namen = {w["name"].lower() for w in items}
    # schon durch Vorlagen abgedeckt (gleiche Einheit unter anderem Namen) oder einmalige Einstiegsvarianten
    abgedeckt = ("koppel", "vereinstraining", "rad-stufentest", "lauf-stufentest", "bahn:", "rad schlüssel", "mtb locker",
                 "rad locker", "rad grundlage", "rad in den bergen", "lauf locker", "kraft", "run", "90 g", "schulevent")
    for ev in kalender:
        n = (ev.get("name") or "").strip()
        if not n or n.lower() in namen or ev.get("category") != "WORKOUT" or n.lower().startswith(abgedeckt):
            continue
        namen.add(n.lower())
        block = vp.block_fuer_event(ev)
        beschr = vp.mit_block(ev.get("description"), block) if block else (ev.get("description") or "")
        items.append({"ordner": _ordner_fuer_event(ev), "name": n, "type": ev.get("type") or "Other", "description": beschr,
                      "tags": ["aus Kalender"], "minuten": round((ev.get("moving_time") or 0) / 60)})
    stat = {"ordner_neu": 0, "neu": 0, "aktualisiert": 0, "warnungen": []}
    vorhandene = client._request("GET", client._athlete("/folders")) or []
    ordner_id = {f["name"]: f["id"] for f in vorhandene}
    vorh_w = {(w.get("folder_id"), (w.get("name") or "").lower()): w["id"]
              for w in (client._request("GET", client._athlete("/workouts")) or [])}
    for ordner in ORDNER:
        if ordner not in ordner_id:
            stat["ordner_neu"] += 1
            if apply:
                f = client._request("POST", client._athlete("/folders"), body={"name": ordner, "type": "FOLDER"})
                ordner_id[ordner] = f["id"]
    for w in items:
        fid = ordner_id.get(w["ordner"])
        body = {"folder_id": fid, "name": w["name"], "type": w["type"], "description": w["description"], "tags": w["tags"]}
        if w["type"] in ("WeightTraining", "Other") or not any(l.startswith("-") for l in w["description"].splitlines()):
            body["moving_time"] = w["minuten"] * 60
        vorhanden = vorh_w.get((fid, w["name"].lower()))
        stat["aktualisiert" if vorhanden else "neu"] += 1
        if not apply:
            continue
        if vorhanden:
            r = client._request("PUT", client._athlete(f"/workouts/{vorhanden}"), body=body)
        else:
            r = client._request("POST", client._athlete("/workouts"), body=body)
        mt = (r.get("moving_time") or 0) / 60
        if w["minuten"] and mt and abs(mt - w["minuten"]) > max(8, 0.2 * w["minuten"]):
            stat["warnungen"].append((w["name"], w["minuten"], round(mt)))
    return stat
