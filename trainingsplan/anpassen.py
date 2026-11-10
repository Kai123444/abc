"""Passt kommende Einheiten anhand der Bewertung an.

Regeln (Horizont = nächste 7 Tage ab heute, weiter entfernte Einheiten
bleiben unverändert):

* gruen  – keine Änderung; wenn zusätzlich "frisch": lockere Einheiten +5 %.
* gelb   – Umfang aller Einheiten -15 %, harte Einheiten: Wiederholungen -25 %.
* rot    – nächste 3 Tage: harte/mittlere Einheiten werden zu lockerer
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
    """Skaliert Stufendauern in Zeilen wie '- 10m Z2' sowie 'Nx'-Wiederholungen."""
    zeilen = []
    for zeile in text.splitlines():
        if zeile.lstrip().startswith("-") and faktor != 1.0:
            def dauer(m: re.Match) -> str:
                if not any(m.groups()):
                    return m.group(0)
                h, mi, s = (int(g) if g else 0 for g in m.groups())
                return _fmt((h * 3600 + mi * 60 + s) * faktor)
            teile = zeile.split("-", 1)
            neu, n = _DAUER.subn(dauer, teile[1], count=0)
            zeile = teile[0] + "-" + neu if n else zeile
        elif wdh_faktor != 1.0:
            zeile = _WDH.sub(lambda m: f"{max(1, round(int(m.group(1)) * wdh_faktor))}x", zeile)
        zeilen.append(zeile)
    return "\n".join(zeilen)


def _skaliere(e: Einheit, grund: str, dauer: float = 1.0, stufen: float = 1.0,
              wdh: float = 1.0, load: float | None = None) -> Einheit:
    """dauer: Gesamtdauer, stufen: Stufendauern im Workout-Text,
    wdh: Wiederholungszahlen, load: Trainingsload (Standard = dauer)."""
    neu = e.kopie(dauer_min=round(e.dauer_min * dauer),
                  load=round(e.load * (load if load is not None else dauer)) if e.load else e.load)
    if e.typ != "Swim":  # bei Schwimmen ist "m" meist Meter, nicht Minuten
        neu.beschreibung = skaliere_beschreibung(e.beschreibung, stufen, wdh)
    neu.angepasst.append(grund)
    return neu


def _locker(e: Einheit, grund: str) -> Einheit:
    dauer = max(30, round(e.dauer_min * 0.6))
    neu = e.kopie(name=f"{e.name} → locker", dauer_min=dauer, intensitaet="locker",
                  load=round(e.load * 0.45) if e.load else None,
                  beschreibung=f"- {dauer}m Z2 HR")
    neu.angepasst.append(grund)
    return neu


def passe_an(plan: list[Einheit], bewertung: Bewertung, heute: date,
             horizont_tage: int = 7) -> list[Einheit]:
    ende = heute + timedelta(days=horizont_tage - 1)
    ergebnis = []
    for e in plan:
        if not (heute <= e.datum <= ende) or e.intensitaet == "ruhe":
            ergebnis.append(e)
            continue
        tag = (e.datum - heute).days
        if bewertung.status == "rot":
            if tag < 3 and e.intensitaet in ("hart", "mittel"):
                e = _locker(e, "Erholungsbedarf (rot) – Intensität gestrichen")
            elif tag < 3:
                e = _skaliere(e, "Erholungsbedarf (rot) – Umfang -20 %", dauer=0.8, stufen=0.8)
            else:
                e = _skaliere(e, "Nachwirkung rot – Umfang -20 %", dauer=0.8, stufen=0.8)
        elif bewertung.status == "gelb":
            if e.intensitaet == "hart":
                e = _skaliere(e, "Erhöhte Ermüdung (gelb) – Wiederholungen -25 %",
                              dauer=0.85, wdh=0.75, load=0.8)
            else:
                e = _skaliere(e, "Erhöhte Ermüdung (gelb) – Umfang -15 %", dauer=0.85, stufen=0.85)
        elif bewertung.frisch and e.intensitaet == "locker":
            e = _skaliere(e, "Gut erholt – Umfang +5 %", dauer=1.05, stufen=1.05)
        ergebnis.append(e)
    return ergebnis
