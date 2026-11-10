"""Stufentest-Vorlagen (Rad und Lauf) als intervals.icu-Workouts.

Rad:  Start 140 W, alle 4 min +20 W (14 Stufen bis 400 W) (Stufen wechseln automatisch). Zum vorzeitigen Ende LAP so
      oft drücken, bis "Ausfahren" erscheint. Alternativ modus="rampe": ein einziger Schritt,
      ein Lap-Druck startet das Ausfahren (weniger gut auswertbar).
Lauf: Start 9 km/h, alle 4 min +1 km/h (11 Stufen bis 19 km/h) (Stufen wechseln automatisch). Zum vorzeitigen Ende
      LAP so oft drücken, bis "Auslaufen" erscheint (Garmin-Lap springt nur einen Schritt weiter).

Auswertung (ohne Laktat):
  Leistung/Geschwindigkeit max = letzte volle Stufe
                                 + (Sekunden in der abgebrochenen Stufe / 180) x Stufenschritt
  Daraus wird die Schwelle grob geschätzt; dazu kommt die Herzfrequenz pro Stufe
  (Knick der HF-Kurve) zur Bestimmung von LTHR und Zonen.
"""

from __future__ import annotations

from datetime import date

from .plan import Einheit

STUFE_MIN = 3


def _pace(kmh: float) -> str:
    sek = 3600 / kmh
    return f"{int(sek // 60)}:{int(round(sek % 60)):02d}/km"


def rad_stufentest(datum: date, start_w: int = 140, schritt_w: int = 20, stufen: int = 14,
                   stufe_min: int = 4, name: str = "Rad-Stufentest",
                   modus: str = "stufen") -> Einheit:
    """modus="rampe": ein einziger Rampenschritt (+schritt_w alle 3 min, gleiche Steigung
    wie der Stufentest). Auf dem Wahoo ELEMNT springt die Lap-Taste in einem Workout zum
    nächsten Schritt -> Lap drücken beendet den Test und startet sofort das Ausfahren.
    modus="stufen": einzelne 3-min-Stufen (Lap springt dann nur zur nächsten Stufe)."""
    if modus == "rampe":
        ende_w = start_w + schritt_w * stufen
        zeilen = ["Warmup", f"- 10m ramp 60-{start_w}w", "",
                  f"Test: Rampe {start_w} bis {ende_w} W, entspricht +{schritt_w} W alle {stufe_min} min. "
                  "Fahren bis zur Erschöpfung, dann LAP-Taste drücken: das Ausfahren startet sofort",
                  f"- {stufe_min * stufen}m ramp {start_w}-{ende_w}w", "",
                  "Ausfahren", "- 10m 90w", "",
                  "Hinweise: ERG-Modus auf der Rolle, Trittfrequenz konstant 85-95, Brustgurt "
                  "tragen. Beim Drücken der LAP-Taste die Zeit im Test notieren (Minute:Sekunde), "
                  "daraus ergibt sich die Maximalleistung. Ausgeruht starten, Vortag locker."]
    else:
        zeilen = ["Warmup", f"- 10m {start_w}w", "",
                  f"Stufen (je {stufe_min} min +{schritt_w} W) - fahren bis zur Erschöpfung"]
        zeilen += [f"- {stufe_min}m {start_w + i * schritt_w}w" for i in range(stufen)]
        zeilen += ["", "Ausfahren", "- Ausfahren 10m 90w", "",
                   f"Ablauf: Die Stufen wechseln automatisch alle {stufe_min} min. Wenn du eine Stufe nicht "
                   "mehr schaffst, hör auf zu treten oder fahr locker und drücke die LAP-Taste so "
                   "oft, bis der Schritt Ausfahren erscheint (jeder Druck springt eine Stufe "
                   "weiter, die Rolle stellt dabei kurz die Zielwatt der übersprungenen Stufen "
                   "ein). Notiere, in welcher Stufe und nach wie viel Sekunden du ausgestiegen bist.",
                   "Hinweise: ERG-Modus auf der Rolle, Trittfrequenz konstant 85-95, Brustgurt "
                   "tragen. Ausgeruht starten, Vortag locker."]
    dauer = 20 + stufe_min * stufen
    return Einheit(datum=datum, name=name, typ="Ride", dauer_min=dauer, load=75,
                   intensitaet="test", beschreibung="\n".join(zeilen), fix=True)


def lauf_stufentest(datum: date, start_kmh: float = 9.0, schritt_kmh: float = 1.0,
                    stufen: int = 11, stufe_min: int = 4,
                    name: str = "Lauf-Stufentest") -> Einheit:
    zeilen = ["Warmup", f"- 10m {_pace(start_kmh - 1)} Pace", "",
              f"Stufen (je {stufe_min} min +{schritt_kmh:g} km/h) – laufen bis zur Erschöpfung"]
    zeilen += [f"- {stufe_min}m {_pace(start_kmh + i * schritt_kmh)} Pace" for i in range(stufen)]
    zeilen += ["", "Auslaufen", f"- Auslaufen 10m {_pace(start_kmh - 1.5)} Pace", "",
               f"Ablauf: Die Stufen wechseln automatisch alle {stufe_min} min. Wenn du die Pace nicht mehr "
               "halten kannst, hör auf zu beschleunigen, laufe locker und drücke die LAP-Taste so "
               "oft, bis der Schritt Auslaufen erscheint (jeder Druck springt eine Stufe weiter). "
               "Notiere, in welcher Stufe und nach wie viel Sekunden du ausgestiegen bist.",
               "Hinweise: Laufband (1 % Steigung) oder 400-m-Bahn, Pace exakt halten, "
               "Brustgurt tragen. Nicht am Tag nach einem harten Rad-Test."]
    dauer = 20 + stufe_min * stufen
    return Einheit(datum=datum, name=name, typ="Run", dauer_min=dauer, load=60,
                   intensitaet="test", beschreibung="\n".join(zeilen), fix=True)


def maximalwert(letzte_volle_stufe: float, sek_in_abbruchstufe: int, schritt: float,
                stufe_min: int = STUFE_MIN) -> float:
    return letzte_volle_stufe + min(sek_in_abbruchstufe, stufe_min * 60) / (stufe_min * 60) * schritt
