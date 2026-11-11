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


def verhaeltnis(rate: int) -> tuple[int, int, str]:
    """Aufteilung der Kohlenhydrate (g/h) in Maltodextrin/Glukose und Fructose.
    Bis 90 g/h 2:1, darüber 1:0,8 (mehr Fructose, weil Glukose-Transporter bei ca. 60 g/h sättigen)."""
    if rate <= 90:
        malto = int(round(rate * 2 / 3))
        return malto, rate - malto, "2:1"
    malto = int(round(rate / 1.8))
    return malto, rate - malto, "1:0,8"


def rate_text(rate: int) -> str:
    m, f, v = verhaeltnis(rate)
    return f"{rate} g/h = {m} g Maltodextrin/Glukose + {f} g Fructose (Verhältnis {v})"


def beispiel_pro_stunde(rate: int) -> str:
    bidon = int(round(0.65 * rate / 5) * 5)
    fluessig = "750-1000 ml" if rate >= 110 else "600-750 ml"
    text = (f"z. B. pro Stunde ein Bidon ({fluessig}) mit {bidon} g Kohlenhydraten plus {rate - bidon} g aus Gels oder "
            f"Riegeln, alle 15 min etwa {int(round(rate / 4 / 5) * 5)} g")
    if rate >= 120:
        text += (". Bei dieser Menge Lösung höchstens ca. 9 % (90 g auf 1 l), den Rest über Gels, Hydrogel-Gels (Alginat) "
                 "sind magenfreundlicher; mindestens 800-1000 ml Flüssigkeit pro Stunde")
    return text


# Renn-Zielraten (g/h) auf dem Rad / beim Laufen. Du verträgst über 100 g/h; vor dem Rennen mindestens 3x so geübt.
RENNRATEN = {"race_olympisch": (130, 95), "race_kurz": (130, 100), "race_mitteldistanz": (115, 80)}

# Darmtraining: (Datum, Sport, Rate g/h, Zusatz). Rate steigt über die Saison, jeweils bei einem langen Tag.
GUT: list[tuple[str, str, int, str]] = [
    ("2026-11-28", "Rad", 85, "Darm nach der Pause neu wecken: du hast als Profi schon über 100 g/h genommen, deshalb startet der Aufbau hoch."),
    ("2026-12-12", "Rad", 95, "Ab hier Verhältnis 1:0,8."),
    ("2027-01-09", "Rad", 105, ""),
    ("2027-01-30", "Rad", 110, ""),
    ("2027-02-13", "Rad", 115, ""),
    ("2027-02-14", "Lauf", 60, "Langer Hügellauf, kleine Portionen alle 15 min, Gel in Wasser verdünnen. Laufen verträgt der Magen schlechter als Radfahren."),
    ("2027-02-27", "Rad", 120, ""),
    ("2027-03-13", "Rad", 120, ""),
    ("2027-03-27", "Rad", 125, "RADRENNEN-FENSTER 1: ein Rennen (1,5-2 h) statt der langen Ausfahrt. Dazu Nitrat-Test (siehe Supplement-Plan)."),
    ("2027-03-28", "Lauf", 70, ""),
    ("2027-04-10", "Rad", 125, ""),
    ("2027-04-24", "Rad", 130, "RADRENNEN-FENSTER 2: ein Rennen (2-2,5 h) statt der langen Ausfahrt. PRÜFPUNKT 1: 130 g/h erstmals im Renntempo, "
                              "Magen höchstens 3/10."),
    ("2027-04-25", "Lauf", 80, "Lauf nach dem Rennwochenende, nur locker, Gel in kleinen Portionen."),
    ("2027-05-08", "Rad", 130, "Dazu Koffein-Test 3 mg/kg (200 mg) 45-60 min vor Start."),
    ("2027-05-09", "Lauf", 85, ""),
    ("2027-05-22", "Rad", 130, "RADRENNEN-FENSTER 3: ein Rennen (2-3 h) statt der langen Ausfahrt, dazu Koffein 4 mg/kg (270 mg) und Natrium 800 mg pro Stunde. "
                              "PRÜFPUNKT 2: 130 g/h zum zweiten Mal im Renntempo, sonst bleibt die DM-Rate bei 120 g/h."),
    ("2027-06-05", "Rad", 130, "Rennsimulation: Koffein als Split-Dosis testen (siehe Supplement-Plan)."),
    ("2027-06-06", "Lauf", 90, "Brick-Lauf mit Renn-Gel-Plan: 25 g alle 15 min."),
    ("2027-06-19", "Rad", 130, "RADRENNEN-FENSTER 4: ein Rennen (2-3 h) statt der langen Ausfahrt, nach Cottbus Plan überprüfen, Magen-Notizen auswerten."),
    ("2027-06-20", "Lauf", 95, "Brick: 40 min Rad im Renntempo, dann Lauf mit 95 g/h. PRÜFPUNKT Lauf: Magen höchstens 3/10, sonst DM-Rate 90 g/h."),
    ("2027-07-03", "Rad", 130, "RADRENNEN-FENSTER 5 (nur bei grüner Ampel): ein Rennen (2-3 h) statt der langen Ausfahrt, Hitzeprotokoll "
                              "(Sauna-Block läuft). Letzte Bestätigung der DM-Rate."),
    ("2027-07-04", "Lauf", 100, "Brick: 40 min Rad im Renntempo, dann Lauf mit 100 g/h exakt wie im Rennen."),
    ("2027-07-17", "Rad", 130, "Generalprobe DM: exakt der Renn-Plan inklusive Koffein und Natrium."),
    ("2027-07-18", "Lauf", 100, "Generalprobe DM: Brick, Lauf mit 100 g/h exakt wie im Rennen."),
    ("2027-08-28", "Rad", 115, "Generalprobe Hölle von Q: 90-100 km Brick, exakt der Renn-Plan."),
]
GUT_NACH_TAG = {t: (sport, rate, extra) for t, sport, rate, extra in GUT}

_BLOCK = re.compile(r"(?m)\n*^Verpflegung:\n.*\Z", re.S)  # nur ein Block, der eine eigene Zeile beginnt


SUPPLEMENTE = {
    "olympisch": (
        "Supplements (Generalprobe für die DM, alles muss vorher im Training getestet sein): Koffein 3 mg/kg = ca. 200 mg 45-60 min "
        "vor dem Start (z. B. Koffein-Gel 75 mg plus Tablette 125 mg, Kaffee zählt mit), Gesamtmenge heute höchstens 4 mg/kg "
        "(270 mg). Natrium 600-800 mg pro Stunde im Getränk. Nitrat nur, wenn getestet: 70 ml Rote-Bete-Konzentrat (ca. 6-8 mmol "
        "Nitrat) 2-3 h vor dem Start. Kein Natriumbikarbonat. Bei Hitze: Eis-Slush 500 ml 30 min vor dem Start."),
    "kurz": (
        "Supplements (nur Getestetes): Koffein 3-4 mg/kg = 200-270 mg 45-60 min vor dem Start (Gel 75 mg plus Tablette 125-200 mg), "
        "zusätzlich 1 mg/kg (65 mg, ein Koffein-Gel) im Wechsel zum Lauf. Gesamt inkl. Kaffee höchstens 5-6 mg/kg (330-400 mg). "
        "Natrium 600-800 mg pro Stunde, bei über 25 Grad bis 1000 mg. Nitrat optional: 70 ml Konzentrat (6-8 mmol) 2-3 h vorher, "
        "wenn du es in zwei Einheiten vertragen hast. Hitze: Eis-Slush 500 ml 30 min vor dem Start, Eiswürfel im Anzug, kaltes "
        "Wasser über Kopf. Kein Natriumbikarbonat. DM: Dopingkontrollen möglich, nur Produkte mit Kölner-Liste oder Informed "
        "Sport, keine Pre-Workout-Mischungen."),
    "mittel": (
        "Supplements (nur Getestetes): Koffein niedrig und verteilt: 2 mg/kg = 130 mg 60 min vor dem Start (oder ganz ohne), "
        "dann alle 60-90 min 1 mg/kg (65 mg) ab der Rad-Hälfte, letzte Gabe vor dem Lauf, Gesamt 4-5 mg/kg (270-335 mg). "
        "Natrium 800-1000 mg pro Stunde (Kapseln zusätzlich), bei Hitze Wasser über den Kopf. Nitrat optional wie bei der DM. "
        "Kein Natriumbikarbonat (zu langer Wettkampf, Magenrisiko). Cola ab Lauf-km 5 als Koffeinquelle."),
}

SUPPLEMENT_REGELN = (
    "Supplement-Plan (67 kg, kein ärztlicher Rat). Grundregel: im Wettkampf nur Dinge, die du in mindestens zwei Einheiten "
    "getestet hast. Zuerst Basis prüfen: Blutbild im Winter (Ferritin, Vitamin D, B12, bei Bedarf mit dem Arzt ergänzen), "
    "bei 12-20 h Training lohnt sich das mehr als jedes Supplement.\n"
    "Koffein (wirksam): 3 mg/kg = 200 mg 45-60 min vor dem Start, in langen Rennen zusätzlich kleine Dosen von 1 mg/kg "
    "(65 mg) in der zweiten Hälfte. Maximal 6 mg/kg = 400 mg, nichts nach 15 Uhr in Trainingswochen. Wer täglich viel "
    "Kaffee trinkt, reduziert in den Wochen vor den Rennen, damit die Wirkung bleibt. Test: Schlüsseleinheiten "
    "08.05. (3 mg/kg), 22.05. (4 mg/kg), 05.06. (Split-Dosis), 17.07. (DM-Plan), 28.08. (Hölle-von-Q-Plan).\n"
    "Natrium (wirksam bei Dauer und Hitze): 500-800 mg pro Stunde, bei Hitze bis 1000 mg, als Getränk 500-1000 mg pro Liter "
    "oder Kapseln.\n"
    "Rote-Bete-Nitrat (mäßig, individuell): 6-8 mmol Nitrat, das sind 70 ml Konzentrat oder 500 ml Saft, 2-3 h vorher; "
    "bei gut Trainierten ist der Effekt klein, Test am 27.03. und 05.06., Urin und Stuhl färben sich rot.\n"
    "Beta-Alanin (optional): 3,2-6,4 g am Tag in 4 Dosen über 4-8 Wochen, hilft bei 1-4 min Belastung (Schwimmstart, "
    "Zielsprint, steile Anstiege), für die Gesamtleistung eher gering; Kribbeln ist normal. Wenn überhaupt: ab 07.06. bis zur DM.\n"
    "Natriumbikarbonat: nicht empfohlen (Magen-Darm-Probleme überwiegen bei diesen Distanzen).\n"
    "Kreatin, BCAA, Pre-Workout-Mischungen: nicht nötig, teils riskant (Dopingkontaminationen).\n"
    "Hitze: Sauna-Block 05.-25.07. (siehe Notiz), im Rennen Eis-Slush vor dem Start, Eiswürfel im Anzug, Schwamm.\n"
    "Anti-Doping: Koffein ist erlaubt. Bei der DM sind Kontrollen möglich, deshalb nur Produkte mit Kölner-Liste oder Informed "
    "Sport und keine Stimulanzien.")

GUT_REGELN = (
    "Darmtraining für hohe Kohlenhydratmengen im Rennen. Ziel für die DM: Rad 130 g/h, Lauf 100 g/h; Cottbus Rad 130 g/h, "
    "Lauf 95 g/h; Hölle von Q Rad 115 g/h, Lauf 80 g/h. Weil du als Profi schon über 100 g/h aufgenommen hast, startet der "
    "Aufbau auf dem Rad hoch und erreicht 130 g/h bereits im April. Der Darm verliert nach der Pause etwas Leistung, kommt "
    "mit regelmäßigen Reizen aber schnell zurück. Beim Laufen bleibt der Aufbau vorsichtiger, weil Radroutine nicht auf den "
    "Magen beim Laufen übertragbar ist.\n"
    "Verhältnis Maltodextrin/Glukose : Fructose: bis 90 g/h 2:1, über 90 g/h 1:0,8. Beispiele pro Stunde: 60 g = 40:20, "
    "70 g = 47:23, 80 g = 53:27, 90 g = 60:30, 100 g = 56:44, 110 g = 61:49, 120 g = 67:53, 125 g = 69:56, 130 g = 72:58.\n"
    "Aufbau im Training (jeweils bei einer langen Einheit am Wochenende): Rad 85 g/h Ende November, 95 g/h im Dezember, 105-115 "
    "g/h im Januar/Februar, 120 g/h im Februar/März, 125 g/h im März/April, 130 g/h ab 24.04. bis zur DM. Lauf: 60 g/h im "
    "Februar, 70-80 g/h im Frühjahr, 85-90 g/h im Mai/Juni, 95-100 g/h im Juni/Juli. Alle Termine siehe Kalendernotizen "
    "'Darmtraining'.\n"
    "Wichtig für die Aufnahme bei Rennbelastung: Im Wettkampftempo fließt weniger Blut in den Darm, deshalb zählt nur, was "
    "du bei Renntempo geschafft hast. Darum die Radrennen-Fenster.\n"
    "Regeln: Magen nach jeder Stunde auf 0-10 notieren (bis 3 gut, 4-5 nicht steigern, ab 6 um 10 g/h senken); Gels immer mit "
    "Wasser; Lösung höchstens ca. 9-10 %; Rate pro Einheit höchstens um 10 g/h steigern. Entscheidungsregel für die DM: "
    "Rennrate = die höchste Rate, die du zweimal in Renn-Intensität mit Magen höchstens 3/10 geschafft hast, minus 5 g/h. "
    "Prüfpunkte Rad: 24.04. und 22.05. (je 130 g/h im Renntempo), Lauf: 20.06. (95 g/h) und 04.07. (100 g/h). Zwischen den "
    "Darmtrainings ganz normal essen.")

RADRENNEN = [
    ("2027-03-27", "2027-03-28", 125, "1,5-2 h", "Saisonstart, erster Test der Aufnahme im Renntempo"),
    ("2027-04-24", "2027-04-25", 130, "2-2,5 h", "PRÜFPUNKT 1, nach der Erholungswoche 12.04. frisch"),
    ("2027-05-22", "2027-05-23", 130, "2-3 h", "PRÜFPUNKT 2, erster Block der Wettkampfphase, dazu Koffein-Test"),
    ("2027-06-19", "2027-06-20", 130, "2-3 h", "Eine Woche nach Cottbus, Plan auswerten"),
    ("2027-07-03", "2027-07-04", 130, "2-3 h", "Letzte Bestätigung, nur bei grüner Ampel, danach Erholungswoche 05.07."),
]

GUT_TERMINE = GUT


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


def _gut_block(minuten: float, sport: str, rate: int, extra: str) -> str:
    m, f, v = verhaeltnis(rate)
    pro = f"{rate} g/h = {m} g Maltodextrin/Glukose + {f} g Fructose (Verhältnis {v})"
    h = minuten / 60
    zeilen = [f"DARMTRAINING: heutiges Ziel {pro}. Insgesamt für diese Einheit ca. {int(round(h * rate / 5) * 5)} g "
              f"({int(round(h * m / 5) * 5)} g Maltodextrin + {int(round(h * f / 5) * 5)} g Fructose).",
              f"Umsetzung: {beispiel_pro_stunde(rate)}; 600-750 ml Flüssigkeit und 500-800 mg Natrium pro Stunde.",
              "Vorher: " + (f"{g(2.0)} Kohlenhydrate 2-3 h vorher, 30 min vorher ein Gel (25 g)." if sport == "Rad"
                            else f"{g(1.5)} Kohlenhydrate 2-3 h vorher."),
              "Magen nach jeder Stunde auf einer Skala 0-10 notieren (0 = ruhig). Ab 4 Rate in der nächsten Einheit nicht "
              "erhöhen, ab 6 um 10 g/h senken. Die Rate wird erst gesteigert, wenn die vorige zweimal gut lief."]
    if extra:
        zeilen.append(extra)
    zeilen.append(NACH_HART)
    return "\n".join(zeilen)


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
    key = {"kurz": "race_kurz", "olympisch": "race_olympisch", "mittel": "race_mitteldistanz"}[kind]
    rad_rate, lauf_rate = RENNRATEN[key]
    rm, rf, rv = verhaeltnis(rad_rate)
    lm, lf, lv = verhaeltnis(lauf_rate)
    if kind == "mittel":
        dauer_rad, dauer_lauf, lauf_min = 2.75, 0.8, 50
        vortage = f"Zwei Tage vorher bis Vortag: {g(8, 10)} Kohlenhydrate pro Tag, ab Vortag abends ballaststoffarm, 3 l trinken."
        rad_zeit = "ca. 2:40-2:50 h"
    else:
        dauer_rad, dauer_lauf, lauf_min = 1.2, 0.75, 45
        vortage = f"Zwei Tage vorher bis Vortag: {g(7, 8)} Kohlenhydrate pro Tag, ab Vortag abends ballaststoffarm, 2-3 l trinken."
        rad_zeit = "ca. 65-75 min"
    rad = (f"Rad ({rad_zeit}): {rad_rate} g Kohlenhydrate pro Stunde = {rm} g Maltodextrin/Glukose + {rf} g Fructose "
           f"(Verhältnis {rv}), insgesamt ca. {int(round(dauer_rad * rad_rate / 5) * 5)} g; {beispiel_pro_stunde(rad_rate)}. "
           f"Von der ersten Minute an alle 15 min, {'800-1000' if rad_rate >= 110 else '700'} ml Flüssigkeit und 600-800 mg Natrium pro Stunde (bei Hitze bis 1000 mg); "
           "in den letzten 10 min vor dem Wechsel nur noch Wasser.")
    lauf = (f"Lauf (ca. {lauf_min} min): {lauf_rate} g Kohlenhydrate pro Stunde = {lm} g Maltodextrin/Glukose + {lf} g Fructose "
            f"(Verhältnis {lv}), insgesamt ca. {int(round(lauf_min * lauf_rate / 60 / 5) * 5)} g: ein Gel (25 g) alle "
            f"{int(round(60 * 25 / lauf_rate))} min, jeweils mit Wasser aus der Verpflegungsstelle, bei Hitze Cola und "
            "Schwamm zum Kühlen. Magen ruhig halten: ab km 5 zuerst Cola/Wasser.")
    pre = (f"Renntag, 3 h vorher: {g(2.5, 3.0)} Kohlenhydrate (Weißbrot mit Honig, Haferbrei, Reis) und 500 ml; "
           "60 min vorher 500 ml mit 500 mg Natrium; 15 min vor dem Start ein Gel (25 g).")
    if kind == "olympisch":
        pre += " Cottbus ist die Generalprobe: genau so üben, wie du es bei der DM machst, auch die hohe Rate."
    if kind == "kurz":
        pre = (f"Renntag (Start 11:30, bei Rolling-Start je nach Gruppe später): Frühstück ca. 8:00 mit {g(2.5, 3.0)} Kohlenhydraten "
               "(Weißbrot mit Honig, Haferbrei) und 500 ml; 10:00 Snack 30-40 g (Banane, Riegel); 10:30 500 ml mit 500 mg Natrium; "
               "10:45 Koffein 3-4 mg/kg (nur wenn getestet); 11:15 Gel 25 g nach der Wettkampfbesprechung um 11:00.")
        rad += (" Auf der Strecke gibt es nur eine Verpflegungsstelle (Nordwende), deshalb alles Wichtige selbst mitführen "
                "(Aero-Bidon oder Rahmen-Bidons plus Gels im Anzug).")
        lauf += " Auf der Laufstrecke gibt es Wasser, Cola, IsoDrink, Obst und Riegel; die Gels trägst du selbst."
    post = f"Danach sofort: {g(1.2)} Kohlenhydrate und 25 g Eiweiß, in den nächsten Stunden weiter essen und trinken."
    return {"vortage": vortage, "pre": pre, "swim": "Schwimmen: nichts mehr, vorher das Gel wie oben.",
            "rad": rad, "lauf": lauf, "post": post, "supp": SUPPLEMENTE[kind]}


def _rennen(kind: str, teil: str | None = None) -> str:
    t = _rennen_teile(kind)
    if teil == "swim":
        return "\n".join([t["vortage"], t["pre"], t["swim"], t["supp"]])
    if teil == "rad":
        return (t["rad"] + "\nWechsel auf den Lauf: Gel erst nach 5-10 min, Magen beruhigen lassen."
                + ("\n" + t["supp"] if kind == "mittel" else ""))
    if teil == "lauf":
        return "\n".join([t["lauf"], t["post"]])
    return "\n".join([t["vortage"], t["pre"], t["swim"], t["rad"], t["lauf"], t["supp"], t["post"]])


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
    tag = (ev.get("start_date_local") or "")[:10]
    if tag in GUT_NACH_TAG and k in ("rad", "rad_hart", "lauf_locker") and minuten >= 90:
        sport, rate, extra = GUT_NACH_TAG[tag]
        if (sport == "Rad" and k.startswith("rad")) or (sport == "Lauf" and k == "lauf_locker"):
            return f"{MARKER}:\n{_gut_block(minuten, sport, rate, extra)}\n(Richtwerte für {GEWICHT:.0f} kg, im Training üben.)"
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
    "Verhältnis Maltodextrin/Glukose : Fructose: bis 90 g/h 2:1 (60 g = 40:20, 80 g = 53:27, 90 g = 60:30), über 90 g/h "
    "1:0,8 (100 g = 56:44, 110 g = 61:49, 120 g = 67:53, 130 g = 72:58).\n"
    "Rennziele: Cottbus Rad 130 g/h, Lauf 95 g/h. DM Rad 130 g/h, Lauf 100 g/h. Hölle von Q Rad 115 g/h, Lauf 80 g/h "
    "(Rennrate immer erst nach den Prüfpunkten fixieren, siehe Darmtraining).\n"
    "Jede Einheit im Kalender hat unten einen Block 'Verpflegung' mit den passenden Mengen.")


def gut_training_events() -> list[dict]:
    """Kalendernotizen für die Darmtraining-Termine (NOTE) plus Regeln und Supplement-Plan."""
    out = []
    for tag, sport, rate, extra in GUT:
        m, f, v = verhaeltnis(rate)
        text = (f"Heute Darmtraining {sport}: {rate_text(rate)}. {beispiel_pro_stunde(rate)}. "
                f"Für 3 h: ca. {3 * rate} g, für 4 h: ca. {4 * rate} g. {extra}".strip())
        out.append({"category": "NOTE", "name": f"Darmtraining {sport}: {rate} g/h ({v})", "description": text,
                    "start_date_local": f"{tag}T00:00:00", "external_id": f"verpflegung-gut-{tag}"})
    for n, (sa, so, rate, dauer, grund) in enumerate(RADRENNEN, 1):
        m, f, v = verhaeltnis(rate)
        text = (f"Radrennen-Fenster {n}: Sa {sa[8:10]}.{sa[5:7]}. oder So {so[8:10]}.{so[5:7]}. {grund}.\n"
                f"Gesucht: Straßenrennen, Kriterium (mindestens 60 min), Jedermann-/Marathonrennen oder MTB-Marathon mit "
                f"{dauer}, echtes Renntempo (nicht Gruppenausfahrt). Termine z. B. über rad-net.de (Terminkalender des BDR). "
                f"Sobald du ein Rennen hast: in intervals.icu als Rennen (C) eintragen, dann plane ich die Woche darum.\n"
                f"Verpflegungsziel im Rennen: {rate_text(rate)}. {beispiel_pro_stunde(rate)}.\n"
                f"Ersetzt die lange Ausfahrt am Samstag. Do Rad-Schlüssel wie geplant, Fr locker 45 min. Sonntag nach einem "
                f"Samstagsrennen nur Lauf locker 45 min; bei Sonntagsrennen am Samstag 60-90 min locker. Montag danach nur "
                f"leichte Beine. Kein Rennen in einer Erholungswoche oder in den 2 Wochen vor Cottbus und der DM. Danach "
                f"Magen-Notizen (0-10 pro Stunde) und Zielrate in den Wellness-Kommentar schreiben.")
        out.append({"category": "NOTE", "name": f"Radrennen-Fenster {n}: {sa[8:10]}.{sa[5:7]}./{so[8:10]}.{so[5:7]}. ({rate} g/h)",
                    "description": text, "start_date_local": f"{sa}T00:00:00",
                    "external_id": f"verpflegung-rennfenster-{n}"})
    out.append({"category": "NOTE", "name": "Darmtraining: Plan und Regeln", "description": GUT_REGELN,
                "start_date_local": "2026-11-11T00:00:00", "external_id": "verpflegung-gut-regeln"})
    out.append({"category": "NOTE", "name": "Supplements: Plan und Regeln", "description": SUPPLEMENT_REGELN,
                "start_date_local": "2026-11-11T00:00:00", "external_id": "verpflegung-supplements"})
    return out
