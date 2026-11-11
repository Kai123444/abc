# Trainingsplan → intervals.icu

Überträgt deinen Trainingsplan automatisch als geplante Workouts nach
[intervals.icu](https://intervals.icu), wertet deine aktuellen Trainings- und
Gesundheitsdaten aus und passt die nächsten 7 Tage des Plans daran an.

Nur Python-Standardbibliothek, keine Abhängigkeiten.

## Einrichtung

1. API-Key holen: intervals.icu → Settings → Developer Settings → API Key.
2. `export INTERVALS_API_KEY=<dein key>` (optional `INTERVALS_ATHLETE_ID`, Standard `0` = du selbst).
3. Plan als `plaene/trainingsplan.json` oder `.csv` ablegen (Vorlage: `plaene/beispiel.json`).

## Planformat

| Feld | Pflicht | Beispiel |
|---|---|---|
| `datum` | ja | `2026-11-12` |
| `name` | ja | `VO2max 5x4` |
| `typ` | nein | `Rad`, `Rolle`, `Lauf`, `Schwimmen`, `Kraft` … (oder intervals.icu-Typ) |
| `dauer_min` | nein | `70` |
| `load` | nein | geplante TSS, z.B. `85` |
| `intensitaet` | nein | `ruhe`, `locker`, `mittel`, `hart` (sonst aus Name erkannt: VO2, Schwelle, Sweet Spot, Intervall …) |
| `beschreibung` | nein | intervals.icu-Workout-Text, z.B. `- 15m ramp 50-75%` |

CSV: gleiche Spaltennamen, Trennzeichen `,` `;` oder Tab.

## Nutzung

```bash
python -m trainingsplan analyse                 # nur auswerten
python -m trainingsplan sync                    # Vorschau der angepassten Einheiten
python -m trainingsplan sync --apply            # nach intervals.icu hochladen
python -m trainingsplan sync --apply --ohne-anpassung   # Plan 1:1 übertragen
python -m trainingsplan anpassen                # bereits in intervals.icu geplante Einheiten: Vorschau
python -m trainingsplan anpassen --apply        # … und dort direkt ändern
```

python -m trainingsplan anpassen --basis-ab 2026-08-01   # Vergleich mit Normalwochen seit August
python -m trainingsplan stufentest --rad 2026-11-14 --lauf 2026-11-17 [--apply]
```

`--basis-ab`: Normalbelastung = Schnitt deiner Trainingswochen seit dem Datum
(Pausen-/Krankheitswochen < 50 % des Medians werden ignoriert). Liegt die
aktuelle Woche im gewohnten Rahmen und sind die Körperwerte normal, wird eine
stark negative Form als Wiedereinstieg gewertet statt als Überlastung.

`stufentest`: Rad 100 W +20 W / 3 min, Lauf 9 km/h +1 km/h / 3 min, jeweils bis
zur Erschöpfung. Ein vorhandener Test am selben Tag (z.B. FTP-Test) wird ersetzt.

```
`anpassen` arbeitet mit dem Kalender in intervals.icu selbst. Feste Termine
(Sportunterricht, Vereinstraining, Wettkampf) werden nie verändert. Tests
(FTP-Test, Ramp-Test …) werden bei Gelb/Rot durch eine lockere Einheit ersetzt.

Jeder Lauf schreibt einen Bericht nach `berichte/JJJJ-MM-TT.md`.
Einheiten werden über eine stabile `external_id` upserted – mehrfaches
Ausführen erzeugt keine Duplikate, angepasste Einheiten ersetzen die alten.

## Auswertung (letzte 60 Tage aus intervals.icu)

| Signal | leicht (1 Pkt.) | deutlich (2 Pkt.) |
|---|---|---|
| Form % (TSB/CTL) | < −20 % | < −30 % |
| Ramp Rate | > 8 CTL/Woche | > 12 |
| HRV 7 Tage vs. Basis (Tag 8–60) | z < −0,75 | z < −1,5 |
| Ruhepuls 7 Tage vs. Basis | +4 bpm | +7 bpm |
| Schlaf Ø 7 Tage | < 7 h | < 6 h |
| Müdigkeit / Muskelkater / Stress (3 Tage) | ≥ 3/4 | ≥ 3,5/4 |
| Akut:Chronisch-Load | > 1,3 | > 1,5 |
| Verletzung/Krankheit eingetragen | – | ja |

**Grün** (0–1 Pkt.): Plan bleibt; bei guter Form lockere Einheiten +5 %.
**Gelb** (2–3 Pkt. oder ein deutliches Signal): Umfang −15 %, harte Einheiten −25 % Wiederholungen.
Sind nur Belastungskennzahlen auffällig, HRV, Ruhepuls und Schlaf aber normal,
wird Rot auf Gelb abgestuft.
Intervallblöcke behalten ihre Intervalldauer, dafür sinkt die Anzahl der Wiederholungen.

**Rot** (≥ 4 Pkt.): nächste 3 Tage harte/mittlere Einheiten → lockere Z2-Grundlage (60 % Dauer), danach −20 %.

Faustregeln, kein ärztlicher Rat.

## Tests

```bash
python -m unittest discover -s tests -t .
```

## Saisonplan bis zur DM Kurzdistanz (08.08.2027)

`python -m trainingsplan saison [--apply] [--alten-plan-loeschen]` schreibt Wochenziele pro Sportart
und Notizen (Phasen, Wochenstruktur, Kontrollregeln, Tests, Taper) in den intervals.icu-Kalender.
Das Rennen muss dort schon stehen. Der Plan steckt in `trainingsplan/saison.py`:
Belastungsaufbau 3:1, CTL-Anstieg höchstens ~4 pro Woche, Lauf-Load nur ~10 % pro Woche, Schwimmen und
Kraft als feste Größen, 17-18 h in den Spitzenwochen (bis 20 h bei grüner Ampel), zweiwöchiger Taper.

## Workout-Bibliothek

`python -m trainingsplan bibliothek [--apply]` legt die Ordner und Workouts des Plans in der Bibliothek von intervals.icu an
(Ordner 01-07 Rad, 10-12 Lauf, 20 Koppel und Brick, 30 Schwimmen, 40 Kraft, 50 Rennen). Bestehende Einträge werden
aktualisiert, im Kalender geplante Einheiten, die noch fehlen, werden einsortiert.

## Kontext ohne Chat-Verlauf

`python -m trainingsplan kontext` liest alles Wissen über den Athleten aus intervals.icu (Einstiegsnotiz "00 START HIER",
Profil-Notizen, aktuelle Phase, Woche, Rennen, Bibliothek, Wellness). Mit `--apply` werden Einstiegsnotiz und
"Saisonübersicht: Woche für Woche" (neu) eingetragen. Persönliche Daten stehen nur in intervals.icu, nicht im Repository.
