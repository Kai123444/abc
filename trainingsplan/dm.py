"""DM Kurzdistanz 2027 (Altersklassen) = 20. NordseeMan, Wilhelmshaven, So 08.08.2027.

Quelle: nordseeman.de (Seite Olympische Distanz) und Ausschreibung 2027 (Stand beim Abruf). Termine und Regeln
können sich ändern: vor der Anreise Ausschreibung und Wettkampfbesprechung prüfen.
"""

from __future__ import annotations

STRECKEN = (
    "DM Kurzdistanz (Altersklassen) beim 20. NordseeMan, Wilhelmshaven, Banter Deich 1A am Pumpwerk. "
    "So 08.08.2027, Start 11:30 Uhr als Rolling-Start in Startgruppen nach Schwimmzeiten, Zielschluss 15:00 Uhr.\n"
    "SCHWIMMEN 1,5 km: Hafenbecken (Großer Hafen vor dem Bontekai), Salzwasser, Wellengang möglich, 750-m-Wendekurs mit "
    "Bojen, Ein- und Ausstieg über die Holztreppe bei der DLRG. Ob Neopren erlaubt ist, entscheiden die Kampfrichter am "
    "Wettkampftag nach der DTU-Temperaturtabelle: beides trainieren. Vom Veranstalter ausgegebene Badekappe tragen.\n"
    "RAD 40 km: 2 Runden, für den Verkehr gesperrt, guter Asphalt, vorwiegend flach, die Jachmannbrücke bringt insgesamt "
    "ca. 40 Höhenmeter. Vom Pumpwerk über die Deichbrücke, Weserstraße, Ahrstraße und Jachmannbrücke auf die Osttangente "
    "am Marinestützpunkt vorbei in den Norden zum Wendepunkt unter der Autobahn (Verpflegungsstelle). Südliche Wende über "
    "Ebertstraße, Ahrstraße und Rheinstraße zurück über die Jachmannbrücke. WINDSCHATTENFAHREN VERBOTEN, Nordseewind, "
    "Helmpflicht. Es gibt nur eine Verpflegungsstelle auf der Strecke.\n"
    "LAUFEN 10 km: 2 Runden, flache Wendepunktstrecke: Pumpwerk, Jadeallee, Kreisel hinter der Banter Ruine, Grodendamm, "
    "Deich an der Nordsee bis zum Wendepunkt beim Fischerdorf, zurück über den Grodendamm zum Kreisel, links in die "
    "Emsstraße (2. Runde), Ziel auf der Jadeallee. Oberkörperbekleidung ist Pflicht, Begleitung verboten, Wind von der "
    "Nordsee. Streckenverpflegung: Wasser, Cola, IsoDrink, Obst, Müsliriegel.\n"
    "ZEITPLAN: Sa 07.08. Startunterlagen 17-19 Uhr, Pasta-Party 18 Uhr im Pumpwerk (bei der Anmeldung buchen, 15 EUR). "
    "So 08.08. Startunterlagen 7:30-9:30, Rad-Check-In 9:30-11:00, Wettkampfbesprechung 11:00 (Pflicht), Start 11:30, "
    "Rad-Check-Out 15:30-16:30, Siegerehrung ca. 16:00. Startpass oder Tageslizenz (15 EUR) mitbringen.\n"
    "ANMELDUNG: 324 Startplätze, Anmeldeschluss 24.07.2027. Laut Website waren alle Distanzen ausgebucht (Warteliste: "
    "organisation@nordseeman.de). Bei der Anmeldung eine realistische Schwimmzeit angeben, danach werden die Startgruppen "
    "gebildet.")

RENNTAG = (
    "Renntag So 08.08.2027 (Start 11:30, bei Rolling-Start später je nach Gruppe):\n"
    "07:30 aufstehen, 08:00 Frühstück 170-200 g Kohlenhydrate (Weißbrot mit Honig, Haferbrei) und 500 ml\n"
    "08:30 Startunterlagen holen (7:30-9:30), 09:30 Rad-Check-In (bis 11:00), Rad, Helm, Verpflegung aufbauen\n"
    "10:00 Snack 30-40 g (Banane, Riegel), 10:15 Einschwimmen/Aufwärmen 10-15 min locker mit 3 Steigerungen\n"
    "10:30 500 ml mit 500 mg Natrium, 10:45 Koffein 3-4 mg/kg (nur wenn getestet), 11:00 Wettkampfbesprechung (Pflicht)\n"
    "11:15 Gel 25 g, Neopren-Entscheidung beachten, 11:30 Start\n"
    "Danach sofort 80 g Kohlenhydrate und 25 g Eiweiß. Zielschluss 15:00, Rad-Check-Out 15:30-16:30.")

VORTAG = (
    "Sa 07.08.2027: Anreise so planen, dass du die Strecke besichtigen kannst: Radstrecke (Wenden, Jachmannbrücke, "
    "Wind) mit lockerem Rad, Laufstrecke 15 min, Einstieg und Ausstieg an der DLRG-Treppe im Hafen (20 min locker "
    "schwimmen, wenn erlaubt). Startunterlagen 17-19 Uhr, Pasta-Party 18 Uhr (Kohlenhydrate 7-8 g/kg über den Tag, "
    "ab abends ballaststoffarm). Rad-Check-In ist erst am Sonntag. 8-9 h Schlaf.")

ABGLEICH = (
    "Abgleich Training und DM-Strecke (nach Ausschreibung 2027):\n"
    "RAD: flach, windschattenfrei, Wenden, Nordseewind. Das verlangt Zeitfahren: gleichmäßige Leistung in Aeroposition, "
    "keine Gruppenfahrt. Der Plan war bergbetont; Berge bleiben die Beinkraft im Aufbau, ab Phase 4 aber überwiegend "
    "flach. Änderungen: (1) Do-Schlüssel ab Dezember mindestens 20 min in Aeroposition, ab März 2 Einheiten pro Woche "
    "in Aeroposition; (2) Zeitfahrtest 40 km solo, flach, Sa 15.05. (Erholungswoche), daraus die Renn-Leistung "
    "ableiten (Richtwert 88-92 % FTP, weil danach noch 10 km laufen); (3) ab Phase 4 Samstag nur jede dritte Woche Berge, "
    "sonst flach: 3x12 min oder 2x20 min bei 95-100 % FTP und 40-km-Blöcke im Renntempo in Aeroposition; (4) Wenden üben "
    "(U-Turns und Antritte, 6-8 pro Einheit); (5) bei Wind trainieren, Gegenwind-Intervalle einplanen. Lausitz und "
    "Cottbus sind flach, das passt zum Training.\n"
    "LAUFEN: flach, Wendepunkte, Wind. Hügelläufe sind im Aufbau gut, ab Mai laufen die Brick- und Renntempoläufe flach, "
    "Wenden sind kein Problem. Mittwochs-Bahnintervalle bleiben.\n"
    "SCHWIMMEN: Hafenbecken mit Salzwasser, Wellen, Wendekurs 750 m, Rolling-Start, Schwimmen im Pulk (Windschatten im "
    "Wasser erlaubt). Änderungen: ab Mai 1x pro Woche Freiwasser, mindestens 2x bei Wind/Wellen, mit und ohne Neopren; "
    "Bojenwenden und Pulk-Schwimmen üben; im Juli 1-2 Einheiten im Salzwasser (Küste), sonst Erinnerung: Salz im Mund "
    "und Schaukeln kosten Konzentration. Realistische Schwimmzeit bei der Anmeldung angeben.\n"
    "UHRZEIT 11:30: Frühstück 8:00, Koffein 10:45, Gel 11:15. Die Generalprobe 17./18.07. starten wir ebenfalls um 11:30 "
    "und essen genauso. Mittagshitze ist möglich: der Sauna-Block 05.-25.07. passt.\n"
    "VERPFLEGUNG: Rad hat nur eine Verpflegungsstelle, deshalb alles mitführen (Aero-Bidon oder Rahmen-Bidons plus Gels); "
    "Lauf: Cola und Wasser, Gels selbst mitnehmen.\n"
    "STARTPLATZ: Die Website nannte alle Distanzen ausgebucht (Warteliste). Falls noch nicht erledigt, Anmeldung oder "
    "Warteliste klären.")

def beschreibung_rennen() -> str:
    return STRECKEN


def notiz_events() -> list[dict]:
    return [
        {"category": "NOTE", "name": "DM-Strecke: Training abgleichen", "description": ABGLEICH,
         "start_date_local": "2026-11-11T00:00:00", "external_id": "dm-abgleich"},
        {"category": "NOTE", "name": "DM Vortag: Anreise und Strecke", "description": VORTAG,
         "start_date_local": "2027-08-07T00:00:00", "external_id": "dm-vortag"},
        {"category": "NOTE", "name": "DM Renntag: Zeitplan", "description": RENNTAG,
         "start_date_local": "2027-08-08T00:00:00", "external_id": "dm-renntag"},
    ]
