"""Stufentest-Vorlagen (Rad und Lauf) als intervals.icu-Workouts.

Rad:  Start 100 W, alle 3 min +20 W bis zur Erschöpfung.
Lauf: Start 9 km/h, alle 3 min +1 km/h bis zur Erschöpfung.

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


def rad_stufentest(datum: date, start_w: int = 100, schritt_w: int = 20, stufen: int = 14,
                   name: str = "Rad-Stufentest") -> Einheit:
    zeilen = ["Warmup", f"- 10m {start_w}w", "",
              f"Stufen (je {STUFE_MIN} min +{schritt_w} W) – fahren bis zur Erschöpfung"]
    zeilen += [f"- {STUFE_MIN}m {start_w + i * schritt_w}w" for i in range(stufen)]
    zeilen += ["", "Cooldown", "- 10m 90w", "",
               "Hinweise: ERG-Modus (Rolle) oder gleichmäßige flache Strecke, Trittfrequenz "
               "konstant 85–95, Brustgurt tragen. Abbruch, wenn die Leistung nicht mehr gehalten "
               "wird – Sekunden in der letzten Stufe notieren. Ausgeruht starten, Vortag locker."]
    dauer = 20 + STUFE_MIN * stufen
    return Einheit(datum=datum, name=name, typ="Ride", dauer_min=dauer, load=75,
                   intensitaet="test", beschreibung="\n".join(zeilen), fix=True)


def lauf_stufentest(datum: date, start_kmh: float = 9.0, schritt_kmh: float = 1.0,
                    stufen: int = 9, name: str = "Lauf-Stufentest") -> Einheit:
    zeilen = ["Warmup", f"- 10m {_pace(start_kmh - 1)} Pace", "",
              f"Stufen (je {STUFE_MIN} min +{schritt_kmh:g} km/h) – laufen bis zur Erschöpfung"]
    zeilen += [f"- {STUFE_MIN}m {_pace(start_kmh + i * schritt_kmh)} Pace" for i in range(stufen)]
    zeilen += ["", "Cooldown", f"- 10m {_pace(start_kmh - 1.5)} Pace", "",
               "Hinweise: Laufband (1 % Steigung) oder 400-m-Bahn, Pace exakt halten, "
               "Brustgurt tragen. Abbruch, wenn die Pace nicht mehr gehalten wird – Sekunden in "
               "der letzten Stufe notieren. Nicht am Tag nach einem harten Rad-Test."]
    dauer = 20 + STUFE_MIN * stufen
    return Einheit(datum=datum, name=name, typ="Run", dauer_min=dauer, load=60,
                   intensitaet="test", beschreibung="\n".join(zeilen), fix=True)


def maximalwert(letzte_volle_stufe: float, sek_in_abbruchstufe: int, schritt: float) -> float:
    return letzte_volle_stufe + min(sek_in_abbruchstufe, STUFE_MIN * 60) / (STUFE_MIN * 60) * schritt
