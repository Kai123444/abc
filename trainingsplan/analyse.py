"""Auswertung von Trainings- und Gesundheitsdaten aus intervals.icu.

Es werden ausschließlich Daten verwendet, die intervals.icu liefert
(Wellness: CTL/ATL/Ramp, HRV, Ruhepuls, Schlaf, subjektive Werte;
Aktivitäten: Trainingsload). Fehlen Werte, wird das jeweilige Kriterium
übersprungen statt geraten.

Die Schwellenwerte sind bewusst konservative Faustregeln, keine
medizinische Diagnose.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Signal:
    name: str
    punkte: int          # 0 = unauffällig, 1 = leicht, 2 = deutlich
    text: str


@dataclass
class Bewertung:
    status: str                      # gruen | gelb | rot
    frisch: bool                     # gut erholt -> leichte Steigerung möglich
    punkte: int
    signale: list[Signal] = field(default_factory=list)
    kennzahlen: dict = field(default_factory=dict)


def _datum(eintrag: dict, *keys: str) -> date | None:
    for k in keys:
        v = eintrag.get(k)
        if v:
            return date.fromisoformat(str(v)[:10])
    return None


def _werte(wellness: list[dict], key: str, von: date, bis: date) -> list[float]:
    out = []
    for w in wellness:
        d = _datum(w, "id", "date")
        v = w.get(key)
        if d and von <= d <= bis and isinstance(v, (int, float)) and v > 0:
            out.append(float(v))
    return out


def _mittel(xs: list[float]) -> float | None:
    return statistics.fmean(xs) if xs else None


def bewerte(wellness: list[dict], aktivitaeten: list[dict], heute: date) -> Bewertung:
    signale: list[Signal] = []
    k: dict = {}
    gestern = heute - timedelta(days=1)
    w7_von = heute - timedelta(days=7)
    basis_von, basis_bis = heute - timedelta(days=60), heute - timedelta(days=8)

    # --- Fitness / Ermüdung / Form -------------------------------------
    mit_ctl = sorted((w for w in wellness if w.get("ctl") is not None and w.get("atl") is not None),
                     key=lambda w: _datum(w, "id", "date") or date.min)
    if mit_ctl:
        letzt = mit_ctl[-1]
        ctl, atl = float(letzt["ctl"]), float(letzt["atl"])
        tsb = ctl - atl
        k.update(ctl=round(ctl, 1), atl=round(atl, 1), tsb=round(tsb, 1))
        form_pct = tsb / ctl * 100 if ctl > 0 else 0.0
        k["form_pct"] = round(form_pct, 1)
        if form_pct < -30:
            signale.append(Signal("Form", 2, f"Form {form_pct:.0f}% (TSB {tsb:.0f}) – hohes Überlastungsrisiko"))
        elif form_pct < -20:
            signale.append(Signal("Form", 1, f"Form {form_pct:.0f}% (TSB {tsb:.0f}) – deutlich ermüdet"))
        ramp = letzt.get("rampRate")
        if isinstance(ramp, (int, float)):
            k["ramp_rate"] = round(float(ramp), 1)
            if ramp > 8:
                signale.append(Signal("Ramp Rate", 2 if ramp > 12 else 1,
                                      f"Fitness steigt um {ramp:.1f} CTL/Woche – zu schnell"))

    # --- HRV ------------------------------------------------------------
    hrv_key = "hrv" if _werte(wellness, "hrv", basis_von, gestern) else "hrvSDNN"
    hrv7 = _werte(wellness, hrv_key, w7_von, heute)
    hrv_basis = _werte(wellness, hrv_key, basis_von, basis_bis)
    if len(hrv7) >= 3 and len(hrv_basis) >= 14:
        m7, mb, sd = statistics.fmean(hrv7), statistics.fmean(hrv_basis), statistics.pstdev(hrv_basis)
        k.update(hrv_7d=round(m7, 1), hrv_basis=round(mb, 1))
        if sd > 0:
            z = (m7 - mb) / sd
            k["hrv_z"] = round(z, 2)
            if z < -1.5:
                signale.append(Signal("HRV", 2, f"HRV 7 Tage Ø {m7:.0f} vs. Basis {mb:.0f} – deutlich unter Normalbereich"))
            elif z < -0.75:
                signale.append(Signal("HRV", 1, f"HRV 7 Tage Ø {m7:.0f} vs. Basis {mb:.0f} – unter Normalbereich"))

    # --- Ruhepuls -------------------------------------------------------
    rhr7 = _werte(wellness, "restingHR", w7_von, heute)
    rhr_basis = _werte(wellness, "restingHR", basis_von, basis_bis)
    if len(rhr7) >= 3 and len(rhr_basis) >= 14:
        m7, mb = statistics.fmean(rhr7), statistics.fmean(rhr_basis)
        k.update(ruhepuls_7d=round(m7, 1), ruhepuls_basis=round(mb, 1))
        diff = m7 - mb
        if diff >= 7:
            signale.append(Signal("Ruhepuls", 2, f"Ruhepuls +{diff:.0f} bpm über Basis"))
        elif diff >= 4:
            signale.append(Signal("Ruhepuls", 1, f"Ruhepuls +{diff:.0f} bpm über Basis"))

    # --- Schlaf ---------------------------------------------------------
    schlaf = _werte(wellness, "sleepSecs", w7_von, heute)
    if len(schlaf) >= 3:
        h = statistics.fmean(schlaf) / 3600
        k["schlaf_h_7d"] = round(h, 1)
        if h < 6:
            signale.append(Signal("Schlaf", 2, f"Nur Ø {h:.1f} h Schlaf in den letzten 7 Tagen"))
        elif h < 7:
            signale.append(Signal("Schlaf", 1, f"Ø {h:.1f} h Schlaf in den letzten 7 Tagen"))

    # --- Subjektiv (intervals.icu Skala 1–4, höher = schlechter) -------
    for key, label in (("fatigue", "Müdigkeit"), ("soreness", "Muskelkater"), ("stress", "Stress")):
        werte = _werte(wellness, key, heute - timedelta(days=3), heute)
        if werte:
            m = statistics.fmean(werte)
            k[f"{key}_3d"] = round(m, 1)
            if m >= 3.5:
                signale.append(Signal(label, 2, f"{label} sehr hoch ({m:.1f}/4)"))
            elif m >= 3:
                signale.append(Signal(label, 1, f"{label} erhöht ({m:.1f}/4)"))
    krank = [w for w in wellness if (_datum(w, "id", "date") or date.min) >= heute - timedelta(days=3)
             and (w.get("injury") or 0) >= 3]
    if krank:
        signale.append(Signal("Verletzung/Krankheit", 2, "Verletzung/Krankheit in den letzten 3 Tagen eingetragen"))

    # --- Belastung aus Aktivitäten (Acute:Chronic) ----------------------
    def load_im(von: date, bis: date) -> float:
        s = 0.0
        for a in aktivitaeten:
            d = _datum(a, "start_date_local", "start_date")
            if d and von <= d <= bis:
                s += float(a.get("icu_training_load") or 0)
        return s

    akut = load_im(w7_von, gestern)
    chronisch = load_im(heute - timedelta(days=35), w7_von - timedelta(days=1)) / 4
    k.update(load_7d=round(akut), load_wochenschnitt_4w=round(chronisch))
    if chronisch > 0:
        acwr = akut / chronisch
        k["acwr"] = round(acwr, 2)
        if acwr > 1.5:
            signale.append(Signal("Belastungssprung", 2, f"Wochenload {acwr:.1f}× über 4-Wochen-Schnitt"))
        elif acwr > 1.3:
            signale.append(Signal("Belastungssprung", 1, f"Wochenload {acwr:.1f}× über 4-Wochen-Schnitt"))

    punkte = sum(s.punkte for s in signale)
    harte_signale = any(s.punkte == 2 for s in signale)
    if punkte >= 4 or (harte_signale and punkte >= 3):
        status = "rot"
    elif punkte >= 2 or harte_signale:
        status = "gelb"
    else:
        status = "gruen"
    frisch = status == "gruen" and punkte == 0 and k.get("form_pct", 0) > 5 and k.get("acwr", 1.0) < 1.2
    return Bewertung(status=status, frisch=frisch, punkte=punkte, signale=signale, kennzahlen=k)
