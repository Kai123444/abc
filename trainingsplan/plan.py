"""Einlesen des Trainingsplans (JSON oder CSV) und Umwandeln in intervals.icu-Events."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path

# Sportarten wie intervals.icu sie erwartet
TYP_MAP = {
    "rad": "Ride", "ride": "Ride", "radfahren": "Ride",
    "indoor": "VirtualRide", "rolle": "VirtualRide", "virtualride": "VirtualRide",
    "lauf": "Run", "laufen": "Run", "run": "Run",
    "schwimmen": "Swim", "swim": "Swim",
    "kraft": "WeightTraining", "weighttraining": "WeightTraining",
    "yoga": "Yoga", "walk": "Walk", "wandern": "Hike", "hike": "Hike",
    "ski": "NordicSki", "rudern": "Rowing", "rowing": "Rowing",
}

INTENSITAETEN = ("ruhe", "locker", "mittel", "hart", "test")
_TEST_WOERTER = re.compile(r"(ftp-?test|ramp-?test|leistungstest|\btest\b)", re.I)
# Termine, die nicht verschoben/verändert werden (Schule, Verein, Wettkampf)
_FIX_WOERTER = re.compile(r"(sportunterricht|schulsport|vereinstraining|wettkampf|rennen|\brace\b)", re.I)
_HART_WOERTER = re.compile(
    r"\b(vo2|vo2max|schwelle|threshold|ftp|intervall|interval|sweet ?spot|tempo|"
    r"sprint|anaerob|race|wettkampf|hit|hiit|z4|z5|z6|z7)\b", re.I)


@dataclass
class Einheit:
    datum: date
    name: str
    typ: str = "Ride"
    dauer_min: float = 60.0
    load: float | None = None          # geplante Trainingsbelastung (TSS)
    intensitaet: str = "locker"        # ruhe | locker | mittel | hart
    beschreibung: str = ""             # intervals.icu Workout-Text, z.B. "- 10m Z2"
    angepasst: list[str] = field(default_factory=list)
    # stabile ID: bleibt bei Anpassungen gleich, damit intervals.icu das Event ersetzt
    external_id: str = ""
    fix: bool = False                  # fester Termin -> wird nie angepasst
    event_id: int | None = None        # ID eines bestehenden intervals.icu-Events

    def __post_init__(self):
        if not self.external_id:
            slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
            self.external_id = f"plan-{self.datum.isoformat()}-{slug}"

    def kopie(self, **kw) -> "Einheit":
        return replace(self, angepasst=list(self.angepasst), **kw)

    def to_event(self) -> dict:
        beschreibung = self.beschreibung
        if self.angepasst:
            hinweis = "Automatisch angepasst: " + "; ".join(self.angepasst)
            beschreibung = f"{beschreibung}\n\n{hinweis}".strip()
        if self.intensitaet == "ruhe":
            return {"category": "NOTE", "start_date_local": f"{self.datum.isoformat()}T00:00:00",
                    "name": self.name, "description": beschreibung or "Ruhetag",
                    "external_id": self.external_id}
        ev = {
            "category": "WORKOUT",
            "start_date_local": f"{self.datum.isoformat()}T00:00:00",
            "type": self.typ,
            "name": self.name,
            "description": beschreibung,
            "moving_time": int(round(self.dauer_min * 60)),
            "external_id": self.external_id,
        }
        if self.load is not None:
            ev["icu_training_load"] = int(round(self.load))
        return ev


def _typ(wert: str | None) -> str:
    if not wert:
        return "Ride"
    return TYP_MAP.get(wert.strip().lower(), wert.strip())


def _intensitaet(roh: dict, name: str, beschreibung: str) -> str:
    wert = (roh.get("intensitaet") or roh.get("intensity") or "").strip().lower()
    if wert in INTENSITAETEN:
        return wert
    if _TEST_WOERTER.search(name):
        return "test"
    if _HART_WOERTER.search(f"{name} {beschreibung}"):
        return "hart"
    return "locker"


def _einheit(roh: dict) -> Einheit:
    name = (roh.get("name") or "").strip()
    if not name or not roh.get("datum"):
        raise ValueError(f"Einheit braucht mindestens 'datum' und 'name': {roh}")
    beschreibung = (roh.get("beschreibung") or roh.get("description") or "").replace("\\n", "\n")
    load = roh.get("load") or roh.get("tss")
    return Einheit(
        datum=date.fromisoformat(str(roh["datum"]).strip()),
        name=name,
        typ=_typ(roh.get("typ") or roh.get("type")),
        dauer_min=float(next((roh[k] for k in ("dauer_min", "dauer") if roh.get(k) not in (None, "")), 60)),
        load=float(load) if load not in (None, "") else None,
        intensitaet=_intensitaet(roh, name, beschreibung),
        beschreibung=beschreibung,
        fix=str(roh.get("fix", "")).strip().lower() in ("1", "true", "ja", "x")
        or bool(_FIX_WOERTER.search(name)),
    )


def einheit_aus_event(ev: dict) -> Einheit:
    """Wandelt ein bestehendes intervals.icu-WORKOUT-Event in eine Einheit."""
    name = ev.get("name") or ev.get("type") or "Workout"
    beschreibung = ev.get("description") or ""
    return Einheit(
        datum=date.fromisoformat(ev["start_date_local"][:10]),
        name=name,
        typ=ev.get("type") or "Ride",
        dauer_min=round((ev.get("moving_time") or 0) / 60),
        load=ev.get("icu_training_load"),
        intensitaet=_intensitaet({}, name, beschreibung),
        beschreibung=beschreibung,
        external_id=ev.get("external_id") or f"icu-{ev.get('id')}",
        fix=bool(_FIX_WOERTER.search(f"{name} {beschreibung}")),
        event_id=ev.get("id"),
    )


def lade_plan(pfad: str | Path) -> list[Einheit]:
    pfad = Path(pfad)
    if pfad.suffix.lower() == ".json":
        daten = json.loads(pfad.read_text(encoding="utf-8"))
        zeilen = daten["einheiten"] if isinstance(daten, dict) else daten
    elif pfad.suffix.lower() == ".csv":
        with pfad.open(encoding="utf-8-sig", newline="") as f:
            probe = f.read(2048)
            f.seek(0)
            dialekt = csv.Sniffer().sniff(probe, delimiters=",;\t")
            zeilen = list(csv.DictReader(f, dialect=dialekt))
    else:
        raise ValueError("Plan muss .json oder .csv sein")
    return sorted((_einheit(z) for z in zeilen), key=lambda e: e.datum)
