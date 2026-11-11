"""Verpflegung pro Einheit (Richtwerte für 67 kg, nach Dauer und Intensität).

Grundlagen (Sporternährung für Ausdauersport):
* Kohlenhydrate während der Einheit: unter 60 min keine, 60-90 min 30-45 g/h, 90-150 min 45-60 g/h,
  über 150 min 60-90 g/h (Glukose:Fructose 2:1 ab 60 g/h), im Rennen über 2 h bis 90 g/h.
* Vorher: 1-2 g/kg Kohlenhydrate 2-3 h vorher bei langen/harten Einheiten, kleiner Snack bei kurzen.
* Nachher: bei langen/harten Einheiten 1,0-1,2 g/kg Kohlenhydrate plus 0,3 g/kg Eiweiß innerhalb von 60 min.
* Flüssigkeit: 400-750 ml/h, Natrium 300-800 mg/h je nach Dauer und Wärme.
Magen-Darm-Verträglichkeit immer im Training üben.
"""

from __future__ import annotations

import re

GEWICHT = 67.0
MARKER = "Verpflegung"

_BLOCK = re.compile(r"\n*Verpflegung[:\n].*\Z", re.S)


def g(lo: float, hi: float | None = None) -> str:
    """Gramm pro kg -> Gramm absolut, auf 5 g gerundet."""
    a = int(round(lo * GEWICHT / 5) * 5)
    if hi is None or hi == lo:
        return f"{a} g"
    return f"{a}-{int(round(hi * GEWICHT / 5) * 5)} g"


def _gesamt(minuten: float, lo: int, hi: int) -> str:
    h = minuten / 60
    return f"insgesamt ca. {int(round(h * lo / 5) * 5)}-{int(round(h * hi / 5) * 5)} g"


NACH_HART = (f"Danach innerhalb von 60 min: {g(1.0, 1.2)} Kohlenhydrate (Reis, Kartoffeln, Nudeln, Banane, Saft) "
             f"und 20-25 g Eiweiß (Quark, Joghurt, Eier, Shake).")
NACH_LEICHT = "Danach normale Mahlzeit mit 20-25 g Eiweiß, keine Sonderverpflegung nötig."
HITZE = ("Nach der Sauna 500 ml Wasser mit einer Prise Salz zusätzlich.")


def _rad(minuten: float, hart: bool) -> str:
    if minuten <= 60 and not hart:
        zeilen = ["Vorher: normaler Snack, keine Pflicht (Banane oder Toast mit Honig, ca. 30 g Kohlenhydrate).",
                  "Währenddessen: nur Wasser, ca. 500 ml pro Stunde, keine Kohlenhydrate nötig.", NACH_LEICHT]
    elif minuten <= 90:
        zeilen = [f"Vorher (1-2 h): {g(0.5, 1.0)} Kohlenhydrate (Haferbrei, Toast mit Marmelade, Banane).",
                  f"Währenddessen: 30-45 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 30, 45)}), z. B. ein Riegel oder Gel pro Stunde "
                  "oder ein Bidon mit 30 g; 500 ml Flüssigkeit pro Stunde, 300 mg Natrium pro Stunde.",
                  NACH_HART if hart else NACH_LEICHT]
    elif minuten <= 150:
        zeilen = [f"Vorher (2-3 h): {g(1.5, 2.0)} Kohlenhydrate (Haferbrei mit Banane, Weißbrot mit Honig, Reis), dazu 400-500 ml.",
                  f"Währenddessen: 45-60 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 45, 60)}), ab der 2. Stunde auch feste Nahrung; "
                  "600 ml Flüssigkeit pro Stunde, 400 mg Natrium pro Stunde.", NACH_HART]
    else:
        zeilen = [f"Vorher (2-3 h): {g(2.0)} Kohlenhydrate (Haferbrei, Weißbrot, Reis), dazu 500 ml; 30 min vorher ein Gel (25 g).",
                  f"Währenddessen: 60-80 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 60, 80)}), alle 20 min etwas essen, "
                  "von Beginn an (nicht erst bei Hunger); Mischung Gel, Riegel, Bananen, Bidon mit 40-60 g; "
                  "600-750 ml Flüssigkeit pro Stunde, 500-600 mg Natrium pro Stunde.", NACH_HART,
                  "Abends Kohlenhydrate hoch halten, die Einheit am nächsten Tag soll nicht leer beginnen."]
    return "\n".join(zeilen)


def _rad_hart(minuten: float) -> str:
    return "\n".join([
        f"Vorher (2-3 h): {g(1.5, 2.0)} Kohlenhydrate (Haferbrei, Weißbrot, Reis), dazu 400-500 ml; 30-45 min vorher Banane "
        "oder Gel (25 g).",
        f"Währenddessen: 40-60 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 40, 60)}), Bidon mit 500 ml und 30-40 g, "
        "300-400 mg Natrium pro Stunde; die Intervalle laufen auf vollem Tank besser.", NACH_HART])


def _test_rad(minuten: float) -> str:
    return "\n".join([
        f"Vortag: kohlenhydratreich essen, ca. 6 g/kg ({g(6)}), wenig Ballaststoffe am Abend, 2-3 l trinken.",
        f"Frühstück 3 h vorher: {g(2.0)} Kohlenhydrate (Haferbrei, Weißbrot mit Honig, Banane) und 500 ml; "
        "45 min vorher Gel (25 g).",
        "Koffein: 3 mg/kg (ca. 200 mg) 45-60 min vorher nur, wenn du es im Training schon vertragen hast.",
        f"Währenddessen: 40-60 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 40, 60)}), Bidon mit 500 ml und 40 g, "
        "300-400 mg Natrium. Das Essen darf den Magen nicht belasten, deshalb Flüssig- statt Festnahrung.",
        NACH_HART])


def _test_lauf(minuten: float) -> str:
    return "\n".join([
        f"Vortag: kohlenhydratreich essen, ca. 5-6 g/kg ({g(5, 6)}), wenig Ballaststoffe am Abend.",
        f"Mittagessen/Frühstück 3 h vorher: {g(1.5, 2.0)} Kohlenhydrate; 30-45 min vorher ein Gel (25 g) oder Banane.",
        "Währenddessen: Wasser oder Iso in kleinen Schlucken (150 ml alle 15-20 min), keine festen Nahrungsmittel, "
        "auf der Bahn kein Gel nötig.", NACH_HART])


def _lauf_intervalle(minuten: float) -> str:
    return "\n".join([
        f"Vorher: Mahlzeit 2-3 h vorher mit {g(1.0, 1.5)} Kohlenhydrate (Reis, Nudeln, Brot), 30-45 min vorher Snack mit 20-30 g "
        "(Banane, Reiswaffel). Nach dem Kraftraum davor nur ein leichter Snack, kein Fett.",
        "Währenddessen: Wasser, 150-250 ml in den Trabpausen; keine Kohlenhydrate nötig.", NACH_HART])


def _lauf_locker(minuten: float) -> str:
    if minuten <= 60:
        return "\n".join(["Vorher: normaler Snack, nicht nüchtern bei Hunger (Banane).",
                          "Währenddessen: nur Wasser, bei weniger als 60 min keine Kohlenhydrate.", NACH_LEICHT])
    return "\n".join([f"Vorher: {g(0.5, 1.0)} Kohlenhydrate 1-2 h vorher.",
                      f"Währenddessen: 30-45 g Kohlenhydrate pro Stunde ({_gesamt(minuten, 30, 45)}), 400-500 ml pro Stunde.",
                      NACH_HART])


def _schwimmen(minuten: float) -> str:
    return "\n".join([
        "Vorher: nicht nüchtern, 60-90 min vorher Snack mit 30-60 g Kohlenhydrate (Banane, Toast, Haferriegel).",
        "Währenddessen: Trinkflasche am Beckenrand, 400-500 ml Wasser, optional mit 20-30 g Kohlenhydraten (Saftschorle).",
        NACH_HART, HITZE + " Eisbad nur nach Schwimmen/Ruhetagen, nicht nach Kraft."])


def _kraft(minuten: float) -> str:
    return "\n".join([
        "Vorher (60-90 min): 30-60 g Kohlenhydrate und 10 g Eiweiß (Joghurt mit Banane, Brot mit Quark).",
        "Währenddessen: Wasser, 300-500 ml.",
        f"Danach innerhalb von 2 h: 25-30 g Eiweiß (0,4 g/kg) und {g(0.6, 0.8)} Kohlenhydrate; kein Eisbad innerhalb von 6 h."])


def _event_schwimmen() -> str:
    return "\n".join([
        "Letzte größere Mahlzeit 2 h vor dem Schwimmen (Pasta, Reis, Brot), danach nur Snacks.",
        "Während der 24 h in den Pausen regelmäßig 30-40 g Kohlenhydrate pro Stunde (Banane, Reiswaffeln, Saft, "
        "Brot mit Honig) und 400-500 ml pro Stunde, nicht auf Hunger warten.", NACH_LEICHT])


def _rennen_teile(kind: str) -> dict[str, str]:
    if kind == "mittel":
        vortage = f"Zwei Tage vorher bis Vortag: {g(8, 10)} Kohlenhydrate pro Tag, ab Vortag abends ballaststoffarm, 3 l trinken."
        rad = ("Rad (ca. 2:40-2:50 h): 80-100 g Kohlenhydrate pro Stunde (gesamt 220-270 g), von Beginn an alle 15-20 min, "
               "Mischung aus Bidon (500 ml mit 60 g), Gels und Riegel; 700 ml Flüssigkeit und 600-800 mg Natrium pro Stunde; "
               "in den letzten 15 min vor dem Wechsel nichts Festes mehr.")
        lauf = ("Lauf (ca. 50 min): 40-60 g Kohlenhydrate pro Stunde, ein Gel (25 g) alle 25-30 min, Wasser und Cola an den "
                "Verpflegungsstellen, bei Hitze Salz.")
        pre = (f"Renntag, 3 h vorher: {g(2.5, 3.0)} Kohlenhydrate (Weißbrot mit Honig, Haferbrei, Reis) und 500 ml; "
               "60 min vorher 500 ml mit 500 mg Natrium; 15 min vor dem Start ein Gel (25 g). Koffein 3 mg/kg "
               "(ca. 200 mg) 45-60 min vorher, nur wenn getestet.")
    else:
        vortage = f"Zwei Tage vorher bis Vortag: {g(7, 8)} Kohlenhydrate pro Tag, ab Vortag abends ballaststoffarm, 2-3 l trinken."
        rad = ("Rad (ca. 65-75 min): 60-90 g Kohlenhydrate pro Stunde, z. B. zwei Bidons mit je 500 ml und 40-45 g plus ein "
               "Gel (25 g) nach 40 min; 500-700 mg Natrium pro Stunde (Elektrolytgetränk).")
        lauf = ("Lauf (ca. 40-45 min): ein Gel (25 g) vor km 1 oder bei km 3 und Wasser an den Verpflegungsstellen; "
                "Magen nicht überladen.")
        pre = (f"Renntag, 3 h vorher: {g(2.0, 3.0)} Kohlenhydrate (Weißbrot mit Honig, Haferbrei, Reis) und 500 ml; "
               "60 min vorher 500 ml mit 500 mg Natrium; 15 min vor dem Start ein Gel (25 g). Koffein 3 mg/kg (ca. 200 mg) "
               "45-60 min vorher, nur wenn getestet.")
        if kind == "olympisch":
            pre += " Cottbus ist die Generalprobe: genau so üben, wie du es bei der DM machst."
    post = f"Danach sofort: {g(1.2)} Kohlenhydrate und 25 g Eiweiß, in den nächsten Stunden weiter essen und trinken."
    return {"vortage": vortage, "pre": pre, "swim": "Schwimmen: nichts mehr, vorher das Gel wie oben.",
            "rad": rad, "lauf": lauf, "post": post}


def _rennen(kind: str, teil: str | None = None) -> str:
    t = _rennen_teile(kind)
    if teil == "swim":
        return "\n".join([t["vortage"], t["pre"], t["swim"]])
    if teil == "rad":
        return t["rad"] + "\nWechsel auf den Lauf: Gel erst nach 5-10 min, Magen beruhigen lassen."
    if teil == "lauf":
        return "\n".join([t["lauf"], t["post"]])
    return "\n".join([t["vortage"], t["pre"], t["swim"], t["rad"], t["lauf"], t["post"]])


def klasse(ev: dict) -> str | None:
    """Art der Einheit aus dem Kalender-Event ableiten."""
    name = (ev.get("name") or "").lower()
    typ = ev.get("type") or ""
    kat = ev.get("category") or ""
    minuten = (ev.get("moving_time") or 0) / 60
    beschr = (ev.get("description") or "").lower()
    if kat.startswith("RACE"):
        if "dm kurzdistanz" in name:
            return "race_kurz"
        if "cottbus" in name:
            return "race_olympisch"
        if "hölle von q" in name:
            return "race_mitteldistanz"
        return None
    if kat != "WORKOUT":
        return None
    if typ == "WeightTraining":
        return "kraft"
    if typ in ("Swim", "OpenWaterSwim"):
        return "event_schwimm" if "schulevent" in name or "24-stunden" in name else "schwimmen"
    if typ == "Run":
        if "stufentest" in name:
            return "test_lauf"
        if "bahn" in name or "intervall" in name or "sportunterricht" in name:
            return "lauf_intervalle"
        return "lauf_locker"
    if typ in ("Ride", "VirtualRide", "MountainBikeRide", "GravelRide"):
        if "stufentest" in name:
            return "test_rad"
        if any(k in name for k in ("sweet spot", "schwelle", "schlüssel", "vo2")) or "ramp 50-75" in beschr:
            return "rad_hart"
        return "rad"
    return None


def block_fuer_event(ev: dict) -> str | None:
    k = klasse(ev)
    if not k:
        return None
    minuten = (ev.get("moving_time") or 0) / 60
    if k == "kraft":
        text = _kraft(minuten)
    elif k == "schwimmen":
        text = _schwimmen(minuten)
    elif k == "event_schwimm":
        text = _event_schwimmen()
    elif k == "test_rad":
        text = _test_rad(minuten)
    elif k == "test_lauf":
        text = _test_lauf(minuten)
    elif k == "lauf_intervalle":
        text = _lauf_intervalle(minuten)
    elif k == "lauf_locker":
        text = _lauf_locker(minuten)
    elif k == "rad_hart":
        text = _rad_hart(minuten)
    elif k == "rad":
        text = _rad(minuten, hart=False)
    elif k == "race_kurz":
        text = _rennen("kurz")
    elif k == "race_olympisch":
        text = _rennen("olympisch")
    elif k == "race_mitteldistanz":
        n = (ev.get("name") or "").lower()
        teil = "swim" if "schwimmen" in n else "rad" if "rad" in n else "lauf" if "lauf" in n else None
        text = _rennen("mittel", teil)
    else:
        return None
    return f"{MARKER}:\n{text}\n(Richtwerte für {GEWICHT:.0f} kg, im Training üben.)"


def mit_block(beschreibung: str | None, block: str) -> str:
    """Beschreibung ohne alten Verpflegungsblock plus neuem Block."""
    basis = _BLOCK.sub("", (beschreibung or "").rstrip())
    return f"{basis}\n\n{block}".strip()


GRUNDREGELN = (
    "Tagesbedarf (67 kg), Richtwerte:\n"
    "Kohlenhydrate: Ruhe-/Erholungstage und kurze lockere Tage 5-6 g/kg (335-400 g), normale Trainingstage 6-8 g/kg "
    "(400-535 g), lange oder harte Tage und die zwei Tage vor Rennen 8-10 g/kg (535-670 g).\n"
    "Eiweiß: 1,6-2,0 g/kg (110-135 g) auf 4-5 Mahlzeiten à 25-30 g verteilt, nach Kraft und harten Einheiten gleich "
    "danach.\n"
    "Fett: ca. 1 g/kg, nicht vor harten Einheiten.\n"
    "Flüssigkeit: 35-40 ml/kg am Tag (2,5 l) plus 500 ml pro Trainingsstunde, nach Sauna 500 ml mehr; Urin hellgelb. "
    "Natrium bei Einheiten über 60 min und bei Hitze zusätzlich.\n"
    "Bei 12-20 h Training nicht zu wenig essen: Energiemangel kostet Leistung, Schlaf und HRV. Vor Schlüsseleinheiten nie "
    "nüchtern, 'Train low' höchstens bei lockeren Einheiten bis 60 min und nicht an Kraft- oder Intervalltagen.\n"
    "Jede Einheit im Kalender hat unten einen Block 'Verpflegung' mit den passenden Mengen.")
