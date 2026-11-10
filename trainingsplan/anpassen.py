"""Passt kommende Einheiten anhand der Bewertung an.

Regeln (Horizont = nächste 7 Tage ab heute, weiter entfernte Einheiten
bleiben unverändert):

* gruen  – keine Änderung; wenn zusätzlich "frisch": lockere Einheiten +5 %.
* gelb   – Umfang aller Einheiten -15 % (Ein-/Ausfahren kürzer, Intervall-
           blöcke mit weniger Wiederholungen statt kürzeren Intervallen),
           harte Einheiten: Wiederholungen -25 %; Tests bleiben.
* feste Termine (Sportunterricht, Vereinstraining, Wettkampf) bleiben immer.
* rot    – Tests werden zu locker; nächste 3 Tage: harte/mittlere Einheiten werden zu lockerer
           Grundlage (Z2, 60 % der Dauer); danach Umfang -20 %.
"""

from __future__ import annotations

import re
from datetime import date, timedelta

from .analyse import Bewertung
from .plan import Einheit

_DAUER = re.compile(r"(?<![\w.])(?:(\d+)h)?(?:(\d+)m(?![a-z]))?(?:(\d+)s)?(?![\w])")
_WDH = re.compile(r"(?<![\w.])(\d+)\s*x(?![a-z])", re.I)


def _fmt(sek: int) -> str:
    sek = max(10, int(round(sek / 10.0)) * 10 if sek < 120 else int(round(sek / 60.0)) * 60)
    m, s = divmod(sek, 60)
    return (f"{m}m" if m else "") + (f"{s}s" if s else "")


def skaliere_beschreibung(text: str, faktor: float, wdh_faktor: float = 1.0) -> str:
    """Skaliert einen intervals.icu-Workout-Text.

    * Stufen außerhalb von Wiederholungsblöcken ('- 15m ramp 50-65%'):
      Dauer x faktor.
    * Wiederholungsblöcke ('Main Set 6x' bis zur nächsten Leerzeile):
      Intervalldauern bleiben unverändert (Reiz bleibt erhalten),
      stattdessen Anzahl x wdh_faktor.
    """
    zeilen = []
    im_block = False
    for zeile in text.splitlines():
        if not zeile.strip():
            im_block = False
        elif zeile.lstrip().startswith("-"):
            if faktor != 1.0 and not im_block:
                def dauer(m: re.Match) -> str:
                    if not any(m.groups()):
                        return m.group(0)
                    h, mi, s = (int(g) if g else 0 for g in m.groups())
                    return _fmt((h * 3600 + mi * 60 + s) * faktor)
                kopf, rest = zeile.split("-", 1)
                zeile = kopf + "-" + _DAUER.sub(dauer, rest)
        elif _WDH.search(zeile):
            im_block = True
            if wdh_faktor != 1.0:
                zeile = _WDH.sub(lambda m: f"{max(1, round(int(m.group(1)) * wdh_faktor))}x", zeile)
        zeilen.append(zeile)
    return "\n".join(zeilen)


def _skaliere(e: Einheit, grund: str, dauer: float = 1.0, stufen: float = 1.0,
              wdh: float | None = None, load: float | None = None) -> Einheit:
    """dauer: Gesamtdauer, stufen: Stufendauern außerhalb von Blöcken,
    wdh: Wiederholungszahlen (Standard = stufen), load: Trainingsload (Standard = dauer)."""
    wdh = stufen if wdh is None else wdh
    neu = e.kopie(dauer_min=round(e.dauer_min * dauer),
                  load=round(e.load * (load if load is not None else dauer)) if e.load else e.load)
    if e.typ in ("Swim", "OpenWaterSwim"):
        # bei Schwimmen ist "m" meist Meter -> nur Wiederholungen kürzen
        stufen = 1.0
    neu.beschreibung = skaliere_beschreibung(e.beschreibung, stufen, wdh)
    neu.angepasst.append(grund)
    return neu


def _locker(e: Einheit, grund: str) -> Einheit:
    dauer = max(30, round(e.dauer_min * 0.6))
    text = (f"- {dauer}m Z2 HR" if e.typ not in ("Swim", "OpenWaterSwim")
            else "Locker schwimmen, Technikfokus, keine Intervalle")
    neu = e.kopie(name=f"{e.name} → locker", dauer_min=dauer, intensitaet="locker",
                  load=round(e.load * 0.45) if e.load else None, beschreibung=text)
    neu.angepasst.append(grund)
    return neu


def passe_an(plan: list[Einheit], bewertung: Bewertung, heute: date,
             horizont_tage: int = 7) -> list[Einheit]:
    ende = heute + timedelta(days=horizont_tage - 1)
    ergebnis = []
    for e in plan:
        if not (heute <= e.datum <= ende) or e.intensitaet == "ruhe" or e.fix:
            ergebnis.append(e)
            continue
        tag = (e.datum - heute).days
        if e.intensitaet == "test" and bewertung.status == "gelb":
            ergebnis.append(e)  # Tests bleiben bei Gelb (Stufentests begrenzen sich selbst)
            continue
        if e.intensitaet == "test" and bewertung.status == "rot":
            e = _locker(e, "Test verschoben – bei Ermüdung wäre das Ergebnis zu niedrig; "
                           "neu ansetzen, sobald der Status grün ist")
        elif bewertung.status == "rot":
            if tag < 3 and e.intensitaet in ("hart", "mittel"):
                e = _locker(e, "Erholungsbedarf (rot) – Intensität gestrichen")
            elif tag < 3:
                e = _skaliere(e, "Erholungsbedarf (rot) – Umfang -20 %", dauer=0.8, stufen=0.8)
            else:
                e = _skaliere(e, "Nachwirkung rot – Umfang -20 %", dauer=0.8, stufen=0.8)
        elif bewertung.status == "gelb":
            if e.intensitaet in ("hart", "test"):
                e = _skaliere(e, "Erhöhte Ermüdung (gelb) – Wiederholungen -25 %",
                              dauer=0.85, stufen=1.0, wdh=0.75, load=0.8)
            else:
                e = _skaliere(e, "Erhöhte Ermüdung (gelb) – Umfang -15 %", dauer=0.85, stufen=0.85)
        elif bewertung.frisch and e.intensitaet == "locker":
            e = _skaliere(e, "Gut erholt – Umfang +5 %", dauer=1.05, stufen=1.05)
        ergebnis.append(e)
    return ergebnis
