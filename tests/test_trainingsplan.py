import unittest
from datetime import date, timedelta
from pathlib import Path

from trainingsplan.analyse import bewerte
from trainingsplan.anpassen import passe_an, skaliere_beschreibung
from trainingsplan.plan import lade_plan

HEUTE = date(2026, 11, 11)
BEISPIEL = Path(__file__).resolve().parent.parent / "plaene" / "beispiel.json"


def wellness(hrv_jetzt=60, rhr_jetzt=50, schlaf_h=8, ctl=60, atl=60):
    out = []
    for i in range(60, -1, -1):
        d = HEUTE - timedelta(days=i)
        jung = i <= 7
        out.append({"id": d.isoformat(), "ctl": ctl, "atl": atl, "rampRate": 3,
                    "hrv": (hrv_jetzt if jung else 60 + (i % 5) - 2),
                    "restingHR": (rhr_jetzt if jung else 50 + (i % 3) - 1),
                    "sleepSecs": schlaf_h * 3600})
    return out


def aktivitaeten(pro_tag=60, letzte_woche=60):
    return [{"start_date_local": (HEUTE - timedelta(days=i)).isoformat() + "T08:00:00",
             "icu_training_load": letzte_woche if i <= 7 else pro_tag} for i in range(1, 36)]


class TestAnalyse(unittest.TestCase):
    def test_gruen(self):
        b = bewerte(wellness(), aktivitaeten(), HEUTE)
        self.assertEqual(b.status, "gruen", b.signale)

    def test_rot_bei_niedriger_hrv_hohem_ruhepuls_wenig_schlaf(self):
        b = bewerte(wellness(hrv_jetzt=45, rhr_jetzt=58, schlaf_h=5.5), aktivitaeten(), HEUTE)
        self.assertEqual(b.status, "rot")

    def test_gelb_bei_belastungssprung(self):
        b = bewerte(wellness(), aktivitaeten(letzte_woche=95), HEUTE)
        self.assertEqual(b.status, "gelb")

    def test_frisch(self):
        b = bewerte(wellness(ctl=60, atl=50), aktivitaeten(), HEUTE)
        self.assertTrue(b.frisch)

    def test_leere_daten(self):
        b = bewerte([], [], HEUTE)
        self.assertEqual(b.status, "gruen")


class TestKoerperOk(unittest.TestCase):
    def test_nur_belastung_auffaellig_wird_gelb(self):
        b = bewerte(wellness(ctl=26, atl=40), aktivitaeten(pro_tag=7, letzte_woche=47), HEUTE)
        self.assertEqual(b.status, "gelb")
        self.assertIn("hinweis", b.kennzahlen)


class TestAnpassen(unittest.TestCase):
    def setUp(self):
        self.plan = lade_plan(BEISPIEL)

    def test_plan_laden(self):
        self.assertEqual(len(self.plan), 5)
        self.assertEqual(self.plan[1].intensitaet, "hart")
        self.assertEqual(self.plan[3].intensitaet, "hart")  # über "Sweet Spot" erkannt
        self.assertEqual(self.plan[4].typ, "Run")

    def test_skaliere_beschreibung(self):
        self.assertEqual(skaliere_beschreibung("- 10m Z2\n- 1h30m 70%", 0.8), "- 8m Z2\n- 72m 70%")
        self.assertEqual(skaliere_beschreibung("Main Set 5x\n- 4m 115%", 1.0, 0.75),
                         "Main Set 4x\n- 4m 115%")
        # Intervalle im Block bleiben gleich lang, nur Anzahl sinkt
        self.assertEqual(skaliere_beschreibung("- 15m 50%\n\nMain Set 6x\n- 1m 68%\n- 6m 65%\n\n- 15m 55%", 0.85, 0.85),
                         "- 13m 50%\n\nMain Set 5x\n- 1m 68%\n- 6m 65%\n\n- 13m 55%")
        self.assertEqual(skaliere_beschreibung("- 2km Z2", 0.5), "- 2km Z2")

    def test_rot_streicht_intensitaet(self):
        b = bewerte(wellness(hrv_jetzt=45, rhr_jetzt=58, schlaf_h=5.5), aktivitaeten(), HEUTE)
        neu = passe_an(self.plan, b, HEUTE)
        vo2 = neu[1]
        self.assertEqual(vo2.intensitaet, "locker")
        self.assertEqual(vo2.beschreibung, "- 42m Z2 HR")
        self.assertEqual(vo2.external_id, self.plan[1].external_id)  # gleiches Event wird ersetzt
        self.assertEqual(neu[2].dauer_min, 0)  # Ruhetag bleibt

    def test_gruen_unveraendert(self):
        b = bewerte(wellness(), aktivitaeten(), HEUTE)
        neu = passe_an(self.plan, b, HEUTE)
        self.assertEqual([e.to_event() for e in neu], [e.to_event() for e in self.plan])

    def test_event_import_fix_und_test(self):
        from trainingsplan.plan import einheit_aus_event
        sport = einheit_aus_event({"id": 1, "start_date_local": "2026-11-13T00:00:00", "type": "Run",
                                   "name": "3000 m Sportunterricht (Run)", "moving_time": 1980})
        ftp = einheit_aus_event({"id": 2, "start_date_local": "2026-11-14T00:00:00", "type": "Ride",
                                 "name": "FTP-Test (Ride)", "moving_time": 3960,
                                 "icu_training_load": 79, "description": "- 20m 100%"})
        self.assertTrue(sport.fix)
        self.assertEqual(ftp.intensitaet, "test")
        self.assertEqual(ftp.external_id, "icu-2")
        b = bewerte(wellness(ctl=26, atl=40), aktivitaeten(pro_tag=7, letzte_woche=47), HEUTE)
        self.assertEqual(b.status, "gelb")
        neu = passe_an([sport, ftp], b, HEUTE)
        self.assertFalse(neu[0].angepasst)
        self.assertEqual(neu[1].intensitaet, "test")  # bei Gelb bleibt der Test
        rot = bewerte(wellness(hrv_jetzt=45, rhr_jetzt=58, schlaf_h=5.5), aktivitaeten(), HEUTE)
        neu = passe_an([ftp], rot, HEUTE)
        self.assertEqual(neu[0].intensitaet, "locker")
        self.assertEqual(neu[0].event_id, 2)

    def test_basis_ab_wiedereinstieg(self):
        # 6 Normalwochen à 350, dann 3 Wochen Pause, jetzt wieder 330
        akt = []
        for i in range(1, 64):
            tag = HEUTE - timedelta(days=i)
            load = 47 if i <= 7 else (0 if i <= 28 else 50)
            akt.append({"start_date_local": tag.isoformat() + "T08:00:00", "icu_training_load": load})
        ohne = bewerte(wellness(ctl=26, atl=40), akt, HEUTE)
        mit = bewerte(wellness(ctl=26, atl=40), akt, HEUTE, basis_ab=HEUTE - timedelta(days=63))
        self.assertNotEqual(ohne.status, "gruen")
        self.assertEqual(mit.status, "gruen")
        self.assertEqual(mit.kennzahlen["pausewochen"], 3)

    def test_stufentests(self):
        from trainingsplan.stufentest import lauf_stufentest, maximalwert, rad_stufentest
        r = rad_stufentest(HEUTE)
        self.assertIn("- 4m 300w", r.beschreibung)
        self.assertIn("- Ausfahren 10m 90w", r.beschreibung)
        self.assertEqual(r.dauer_min, 76)
        self.assertIn("- 56m ramp 140-420w", rad_stufentest(HEUTE, modus="rampe").beschreibung)
        self.assertTrue(r.fix)
        l = lauf_stufentest(HEUTE)
        self.assertIn("- 4m 4:00/km Pace", l.beschreibung)
        self.assertEqual(l.dauer_min, 64)
        self.assertEqual(maximalwert(300, 120, 20, 4), 310)

    def test_saisonplan(self):
        from trainingsplan import saison
        ziele = saison.ziel_events()
        self.assertEqual(len(ziele), len(saison.WOCHEN) * 4)
        for tag, tss, rec in saison.WOCHEN:
            v = saison.verteilung(tss, tag, rec)
            self.assertEqual(sum(v.values()), tss)
            self.assertTrue(all(x >= 0 for x in v.values()), (tag, v))
            saison.montag(tag)  # wirft bei Nicht-Montag
        werte = list(saison.WOCHEN)
        for i, (tag, tss, rec) in enumerate(werte):
            if rec and tag not in saison.TAPER_WOCHEN:
                self.assertLess(tss, werte[i - 1][1] * 0.8)
        # keine Steigerung über 8 % von Woche zu Woche (außer nach Erholungs-/Taperwoche)
        for (ta, a, ra), (_, b, rb) in zip(werte, werte[1:]):
            if not ra and not rb and ta >= "2026-11-23":  # Testwochen davor zählen nicht
                self.assertLessEqual(b / a, 1.08)
        # Lauf-Load wächst gegenüber der letzten Belastungswoche höchstens ~13 % pro Woche
        letzte = None
        for tag, tss, rec in werte:
            if rec or tag < "2026-11-23":  # Testwochen zählen nicht als Ausgangspunkt
                continue
            lauf = saison.verteilung(tss, tag, rec)["Run"]
            if letzte:
                self.assertLessEqual(lauf / letzte, 1.13, tag)
            letzte = lauf

    def test_saison_stunden(self):
        from trainingsplan import saison
        h = {tag: saison.stunden(tss, tag, rec) for tag, tss, rec in saison.WOCHEN}
        self.assertLessEqual(max(h.values()), 20)       # nie über deiner Obergrenze
        self.assertGreaterEqual(max(h.values()), 17)    # Spitzenblöcke nutzen die Zeit
        self.assertLessEqual(h["2026-11-30"], 15)       # Wiedereinstieg bleibt moderat

    def test_sauna_eisbad_wird_eingeordnet(self):
        from trainingsplan.analyse import expositionen
        w = wellness()
        # Sauna und Eisbad am Vortag: Morgenwerte von HEUTE sind schlecht, dürfen die Ampel nicht kippen
        w[-2]["comments"] = "Sauna 2x15 min bei 90 Grad, danach Eistonne 1 min"
        w[-1]["hrv"], w[-1]["restingHR"] = 45, 60
        e = expositionen(w)
        self.assertEqual(e[HEUTE - timedelta(days=1)], {"sauna", "kalt"})
        mit = bewerte(w, aktivitaeten(), HEUTE)
        self.assertEqual(mit.kennzahlen["tage_nach_sauna_kalt"], 1)
        self.assertTrue(any(s.name == "Sauna/Eisbad" and s.punkte == 0 for s in mit.signale))
        ohne = [dict(x, comments=None) for x in w]
        schlecht = bewerte(ohne, aktivitaeten(), HEUTE)
        self.assertLess(mit.punkte, schlecht.punkte + 1)  # Einordnung kostet keine Punkte
        self.assertLessEqual(mit.kennzahlen.get("ruhepuls_7d", 0), schlecht.kennzahlen.get("ruhepuls_7d", 99))

    def test_verpflegung(self):
        from trainingsplan.verpflegung import block_fuer_event, klasse, mit_block
        lang = {"category": "WORKOUT", "type": "Ride", "name": "Rad in den Bergen", "moving_time": 200 * 60}
        b = block_fuer_event(lang)
        self.assertIn("60-80 g Kohlenhydrate pro Stunde", b)
        self.assertIn("insgesamt ca. 200-265 g", b)
        locker = {"category": "WORKOUT", "type": "Ride", "name": "Rad locker", "moving_time": 45 * 60}
        self.assertIn("keine Kohlenhydrate nötig", block_fuer_event(locker))
        self.assertEqual(klasse({"category": "WORKOUT", "type": "Run", "name": "Lauf-Stufentest"}), "test_lauf")
        self.assertEqual(klasse({"category": "RACE_A", "name": "dm kurzdistanz"}), "race_kurz")
        # idempotent: Block wird ersetzt, nicht verdoppelt
        d1 = mit_block("- 60m 60%", b)
        self.assertEqual(mit_block(d1, b), d1)
        self.assertEqual(d1.count("Verpflegung:"), 1)
        self.assertTrue(d1.startswith("- 60m 60%"))

    def test_darmtraining_und_verhaeltnis(self):
        from datetime import date as d
        from trainingsplan import verpflegung as vp
        self.assertEqual(vp.verhaeltnis(90), (60, 30, "2:1"))
        self.assertEqual(vp.verhaeltnis(100), (56, 44, "1:0,8"))
        self.assertEqual(vp.verhaeltnis(120), (67, 53, "1:0,8"))
        for tag, sport, rate, _ in vp.GUT:
            self.assertEqual(d.fromisoformat(tag).weekday(), 5 if sport == "Rad" else 6, tag)  # Sa Rad, So Lauf
        rad = [r for _, s_, r, _ in vp.GUT if s_ == "Rad"]
        self.assertEqual(rad[0], 70)
        self.assertEqual(max(rad), 130)
        lauf = [r for _, s_, r, _ in vp.GUT if s_ == "Lauf"]
        self.assertEqual(max(lauf), 100)
        self.assertTrue(all(b - a_ <= 10 for a_, b in zip(lauf, lauf[1:])))
        self.assertEqual(len(vp.RADRENNEN), 5)
        for sa, so, *_ in vp.RADRENNEN:
            self.assertEqual(d.fromisoformat(sa).weekday(), 5)
            self.assertEqual(d.fromisoformat(so).weekday(), 6)
        # Rate steigt höchstens um 10 g/h von Einheit zu Einheit
        self.assertTrue(all(b - a_ <= 10 for a_, b in zip(rad, rad[1:])))
        lang = {"category": "WORKOUT", "type": "Ride", "name": "Rad in den Bergen", "moving_time": 200 * 60,
                "start_date_local": "2026-11-28T00:00:00"}
        self.assertIn("DARMTRAINING", vp.block_fuer_event(lang))
        dm = vp.block_fuer_event({"category": "RACE_A", "name": "dm kurzdistanz"})
        self.assertIn("130 g Kohlenhydrate pro Stunde", dm)
        self.assertIn("72 g Maltodextrin/Glukose + 58 g Fructose", dm)
        self.assertIn("100 g Kohlenhydrate pro Stunde", dm)
        self.assertIn("Koffein", dm)

    def test_event_format(self):
        ev = self.plan[0].to_event()
        self.assertEqual(ev["category"], "WORKOUT")
        self.assertEqual(ev["type"], "Ride")
        self.assertEqual(ev["moving_time"], 5400)
        self.assertEqual(ev["start_date_local"], "2026-11-11T00:00:00")


if __name__ == "__main__":
    unittest.main()
