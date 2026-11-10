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

    def test_event_format(self):
        ev = self.plan[0].to_event()
        self.assertEqual(ev["category"], "WORKOUT")
        self.assertEqual(ev["type"], "Ride")
        self.assertEqual(ev["moving_time"], 5400)
        self.assertEqual(ev["start_date_local"], "2026-11-11T00:00:00")


if __name__ == "__main__":
    unittest.main()
