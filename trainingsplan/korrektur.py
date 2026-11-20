"""Aktivitätsdateien korrigieren, wenn die Uhr Distanz oder Zeit falsch aufzeichnet.

* Lauf/Rad (FIT): Distanz auf einen bekannten Wert setzen (z. B. 3000 m in der Halle) und optional
  auf eine gestoppte Zeit kürzen. Lücken am Anfang/Ende, in denen die Uhr keine Bewegung erkannt
  hat, werden mit dem Tempo der ersten bzw. letzten Laufsekunden gefüllt; dazwischen bleibt der
  Tempoverlauf der Uhr und wird skaliert. Puls, Kadenz und alle anderen Felder bleiben unverändert.
* Beckenschwimmen (TCX-Export aus Garmin Connect, Sportart oft 'Other'): Die Uhr zählt beim Wechsel
  der Schwimmart manchmal Fehlbahnen. Es werden nur Bahnen gestrichen (nie hinzugefügt), bis die
  Zieldistanz stimmt und das Tempo der Runden möglichst gleichmäßig um den Schnitt liegt. Ergebnis
  ist eine FIT-Datei 'Beckenschwimmen' mit aktiven Bahnen, Pausen-Bahnen und Runden, die Strava und
  intervals.icu mit Pace und Pausen anzeigen.
* Rolle (FIT): Sendet der Rollentrainer eine falsche Geschwindigkeit (0 km/h beim Treten oder unrealistisch
  hoch), wird sie aus der Leistung berechnet (flache Straße, wie bei Rollen-Apps üblich). Sonst stimmen
  Fahrzeit und TSS in intervals.icu nicht. Leistung, Puls und Trittfrequenz bleiben unverändert.

Nur Standardbibliothek. Eingabe/Ausgabe sind Bytes; der CLI-Befehl `korrektur` lädt das Original
aus intervals.icu, schreibt die Datei nach korrekturen/ und tauscht mit --apply die Aktivität aus.
"""

from __future__ import annotations

import struct
import xml.etree.ElementTree as ET
from datetime import datetime

FIT_EPOCH = 631065600  # 1989-12-31T00:00:00Z
_CRC_T = [0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
          0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400]
_INV = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF}


def crc16(data: bytes, c: int = 0) -> int:
    for b in data:
        t = _CRC_T[c & 0xF]; c = (c >> 4) & 0x0FFF; c = c ^ t ^ _CRC_T[b & 0xF]
        t = _CRC_T[c & 0xF]; c = (c >> 4) & 0x0FFF; c = c ^ t ^ _CRC_T[(b >> 4) & 0xF]
    return c


# --------------------------------------------------------------------------- FIT lesen/patchen
def fit_nachrichten(d: bytes):
    """Liefert (start, ende, global_nr, {feld: (pos, groesse, big_endian)}) je Nachricht;
    Definitionsnachrichten mit global_nr None."""
    hs = d[0]
    size = struct.unpack("<I", d[4:8])[0]
    p, end, defs = hs, hs + size, {}
    while p < end:
        s = p
        h = d[p]; p += 1
        if h & 0x80:  # komprimierter Zeitstempel
            g, fl, dev, be = defs[(h >> 5) & 3]
        elif h & 0x40:
            be = d[p + 1]
            g = struct.unpack(">H" if be else "<H", d[p + 2:p + 4])[0]
            nf = d[p + 4]; p += 5
            fl = [tuple(d[p + 3 * i:p + 3 * i + 3]) for i in range(nf)]; p += 3 * nf
            dev = 0
            if h & 0x20:
                nd = d[p]; p += 1
                dev = sum(d[p + 3 * i + 1] for i in range(nd)); p += 3 * nd
            defs[h & 0xF] = (g, fl, dev, be)
            yield s, p, None, None
            continue
        else:
            g, fl, dev, be = defs[h & 0xF]
        felder = {}
        for num, sz, _bt in fl:
            felder[num] = (p, sz, be); p += sz
        p += dev
        yield s, p, g, felder


def _get(d, f):
    p, sz, be = f
    return int.from_bytes(d[p:p + sz], "big" if be else "little")


def _put(d, f, v):
    p, sz, be = f
    v = max(0, min(int(round(v)), _INV[sz] - 1))
    d[p:p + sz] = v.to_bytes(sz, "big" if be else "little")


def _fit_schliessen(header: bytes, body: bytes) -> bytes:
    h = bytearray(header)
    h[4:8] = struct.pack("<I", len(body))
    if h[0] >= 14:
        h[12:14] = struct.pack("<H", crc16(bytes(h[:12])))
    out = bytes(h) + body
    return out + struct.pack("<H", crc16(out))


def fit_pruefen(d: bytes) -> dict:
    """CRC prüfen und Kennzahlen lesen (für Tests und Kontrolle)."""
    assert d[8:12] == b".FIT", "keine FIT-Datei"
    assert crc16(d[:-2]) == struct.unpack("<H", d[-2:])[0], "Datei-CRC falsch"
    info = {"records": 0, "laps": [], "lengths": [], "session": {}}
    for _s, _e, g, fl in fit_nachrichten(d):
        if g == 20:
            info["records"] += 1
            if 5 in fl:
                info["record_distanz_ende"] = _get(d, fl[5]) / 100
        elif g == 19:
            info["laps"].append({k: _get(d, v) for k, v in fl.items()})
        elif g == 101:
            info["lengths"].append({k: _get(d, v) for k, v in fl.items()})
        elif g == 18:
            info["session"] = {k: _get(d, v) for k, v in fl.items()}
    return info


# --------------------------------------------------------------------------- Lauf/Rad
def korrigiere_distanz(fit: bytes, distanz_m: float, zeit_s: float | None = None) -> tuple[bytes, dict]:
    """Distanz-Stream, Runden und Session auf distanz_m setzen; mit zeit_s endet die Aktivität dort
    (Records danach entfallen). Lücken ohne erkannte Bewegung am Anfang/Ende werden gefüllt."""
    d = bytearray(fit)
    hs = d[0]
    msgs = list(fit_nachrichten(d))
    recs = [m for m in msgs if m[2] == 20 and 253 in m[3]]
    t0 = _get(d, recs[0][3][253])
    tt = [_get(d, m[3][253]) - t0 for m in recs]
    ende = zeit_s if zeit_s else tt[-1]
    v = []
    for i, m in enumerate(recs):
        if 73 in m[3] and _get(d, m[3][73]) != _INV[m[3][73][1]]:
            v.append(_get(d, m[3][73]) / 1000)
        elif 6 in m[3] and _get(d, m[3][6]) != _INV[m[3][6][1]]:
            v.append(_get(d, m[3][6]) / 1000)
        elif 5 in m[3] and i:
            dt = max(tt[i] - tt[i - 1], 1)
            v.append(max(_get(d, m[3][5]) - _get(d, recs[i - 1][3][5]), 0) / 100 / dt)
        else:
            v.append(0.0)
    bewegt = [i for i, x in enumerate(v) if x > 1.0 and tt[i] <= ende]
    if not bewegt:
        raise ValueError("keine Bewegung im Distanz-/Tempo-Stream gefunden")
    erst, letzt = bewegt[0], bewegt[-1]
    v0 = sum(v[erst:erst + 40]) / len(v[erst:erst + 40])
    vend = sum(v[max(erst, letzt - 9):letzt + 1]) / len(v[max(erst, letzt - 9):letzt + 1])
    vn = []
    for i, t in enumerate(tt):
        if t > ende or t == 0:
            vn.append(0.0)
        elif i < erst:
            vn.append(v0)
        elif i > letzt:
            vn.append(vend)
        else:
            vn.append(v[i])
    cum = [0.0]
    for i in range(1, len(tt)):
        cum.append(cum[-1] + vn[i] * (tt[i] - tt[i - 1]))
    i_ende = max(i for i, t in enumerate(tt) if t <= ende)
    fak = distanz_m / cum[i_ende]
    dist = [min(x * fak, distanz_m) for x in cum]
    vn = [x * fak for x in vn]
    weg = set()
    for i, m in enumerate(recs):
        if tt[i] > ende:
            weg.add(m[0]); continue
        if 5 in m[3]:
            _put(d, m[3][5], dist[i] * 100)
        if 73 in m[3]:
            _put(d, m[3][73], vn[i] * 1000)
        if 6 in m[3]:
            _put(d, m[3][6], vn[i] * 1000)

    def dist_bei(t):
        return dist[min(range(len(tt)), key=lambda i: abs(tt[i] - t))]

    runden = []
    laps = [m for m in msgs if m[2] == 19]
    for k, m in enumerate(laps):
        fl = m[3]
        a = _get(d, fl[2]) - t0
        tim = _get(d, fl[8]) / 1000
        if a >= ende:
            continue
        b = min(a + tim, ende)
        if k == len(laps) - 1 or a + tim > ende:
            tim = b - a
            for f in (7, 8):
                if f in fl:
                    _put(d, fl[f], tim * 1000)
        ld = dist_bei(b) - dist_bei(a)
        if 9 in fl:
            _put(d, fl[9], ld * 100)
        sp = ld / tim if tim else 0
        mx = max([vn[i] for i, t in enumerate(tt) if a <= t <= b] or [0])
        for f, val in ((13, sp), (110, sp), (14, mx), (111, mx)):
            if f in fl:
                _put(d, fl[f], val * 1000)
        runden.append((round(ld), round(tim, 1)))
    dauer = ende
    for _s, _e, g, fl in msgs:
        if g == 18:
            if zeit_s:
                for f in (7, 8):
                    if f in fl:
                        _put(d, fl[f], dauer * 1000)
            dauer = _get(d, fl[8]) / 1000 if 8 in fl else dauer
            _put(d, fl[9], distanz_m * 100)
            for f, val in ((14, distanz_m / dauer), (124, distanz_m / dauer), (15, max(vn)), (125, max(vn))):
                if f in fl:
                    _put(d, fl[f], val * 1000)
        elif g == 34 and zeit_s and 0 in fl:
            _put(d, fl[0], dauer * 1000)
        elif g == 21 and zeit_s and 1 in fl and _get(d, fl[1]) == 4 and _get(d, fl[253]) - t0 > ende:
            _put(d, fl[253], t0 + ende)
    body = b"".join(bytes(d[s:e]) for s, e, _g, _f in msgs if s not in weg)
    out = _fit_schliessen(bytes(d[:hs]), body)
    return out, {"faktor": fak, "luecke_start_s": tt[erst], "ende_s": dauer, "runden": runden,
                 "records_entfernt": len(weg), "pace_s_km": dauer / distanz_m * 1000}


# --------------------------------------------------------------------------- Becken falsch eingestellt
_SKAL = {20: (5, 6, 73), 19: (9, 13, 14, 110, 111), 18: (9, 14, 15, 124, 125), 101: (6,)}


def becken_korrigieren(fit: bytes, bahn_m: float) -> tuple[bytes, dict]:
    """Beckenschwimmen (FIT von der Uhr) mit falsch eingestellter Beckenlänge: Beckenlänge setzen und alle
    Distanzen und Geschwindigkeiten im Verhältnis neu/alt skalieren (Records, Runden, Session, Bahnen).
    Zeiten, Puls, Züge und die Zahl der Bahnen bleiben."""
    d = bytearray(fit)
    msgs = list(fit_nachrichten(d))
    alt = None
    for _s, _e, g, fl in msgs:
        if g == 18 and 44 in fl:
            alt = _get(d, fl[44]) / 100
    if not alt:
        raise ValueError("keine Beckenlänge in der Datei (kein Beckenschwimmen?)")
    fak = bahn_m / alt
    for _s, _e, g, fl in msgs:
        for f in _SKAL.get(g, ()):
            if f in fl and _get(d, fl[f]) != _INV[fl[f][1]]:
                _put(d, fl[f], _get(d, fl[f]) * fak)
        if g == 18 and 44 in fl:
            _put(d, fl[44], bahn_m * 100)
    hs = d[0]
    out = _fit_schliessen(bytes(d[:hs]), bytes(d[hs:-2]))
    info = fit_pruefen(out)
    return out, {"becken_alt": alt, "becken_neu": bahn_m, "faktor": fak, "distanz": info["session"].get(9, 0) / 100,
                 "bahnen_aktiv": sum(1 for x in info["lengths"] if x.get(12) == 1)}


# --------------------------------------------------------------------------- Rolle
def v_aus_leistung(p: float, masse_kg: float = 75.0, cda: float = 0.32, crr: float = 0.004) -> float:
    """Geschwindigkeit (m/s) auf flacher Straße bei Leistung p (W), Antriebsverlust 2,5 %."""
    if p <= 0:
        return 0.0
    lo, hi = 0.0, 30.0
    for _ in range(50):
        m = (lo + hi) / 2
        if 0.5 * 1.2 * cda * m ** 3 + crr * masse_kg * 9.81 * m < p * 0.975:
            lo = m
        else:
            hi = m
    return lo


def rolle_geschwindigkeit(fit: bytes, masse_kg: float = 75.0) -> tuple[bytes, dict]:
    """Geschwindigkeit und Distanz einer Rollenfahrt aus der Leistung neu berechnen
    (Records, Runden, Session); Pausen über 2 s zählen nicht zur Distanz."""
    d = bytearray(fit)
    msgs = list(fit_nachrichten(d))
    recs = [m for m in msgs if m[2] == 20 and 253 in m[3]]
    alt_dist = None
    t_prev, dist, vmax, ts_dist = None, 0.0, 0.0, []
    for _s, _e, _g, fl in recs:
        t = _get(d, fl[253])
        p = _get(d, fl[7]) if 7 in fl else 0
        if 7 in fl and p == _INV[fl[7][1]]:
            p = 0
        v = v_aus_leistung(p, masse_kg)
        vmax = max(vmax, v)
        if t_prev is not None and t - t_prev <= 2:
            dist += v * (t - t_prev)
        t_prev = t
        if 5 in fl:
            alt_dist = _get(d, fl[5]) / 100
            _put(d, fl[5], dist * 100)
        for f in (6, 73):
            if f in fl:
                _put(d, fl[f], v * 1000)
        ts_dist.append((t, dist))

    def dist_bei(ts):
        best = 0.0
        for t, x in ts_dist:
            if t > ts:
                break
            best = x
        return best

    for _s, _e, g, fl in msgs:
        if g not in (18, 19) or 2 not in fl:
            continue
        a = _get(d, fl[2])
        el = _get(d, fl[7]) / 1000 if 7 in fl else 0
        tim = _get(d, fl[8]) / 1000 if 8 in fl else el
        dd = dist if g == 18 else dist_bei(a + el) - dist_bei(a)
        if 9 in fl:
            _put(d, fl[9], dd * 100)
        avg, mx = (13, 14) if g == 19 else (14, 15)
        for f, val in ((avg, dd / tim if tim else 0), (mx, vmax), (110 if g == 19 else 124, dd / tim if tim else 0),
                       (111 if g == 19 else 125, vmax)):
            if f in fl:
                _put(d, fl[f], val * 1000)
    hs = d[0]
    out = _fit_schliessen(bytes(d[:hs]), bytes(d[hs:-2]))
    return out, {"distanz_alt_km": (alt_dist or 0) / 1000, "distanz_km": dist / 1000, "vmax_kmh": vmax * 3.6}


# --------------------------------------------------------------------------- Schwimmen
_T = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"


def _fts(iso: str) -> float:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() - FIT_EPOCH


def tcx_runden(tcx: bytes | str) -> tuple[list[dict], int | None]:
    root = ET.fromstring(tcx)
    laps = []
    for lap in root.iter(_T + "Lap"):
        pts = []
        for p in lap.iter(_T + "Trackpoint"):
            h = p.find(_T + "HeartRateBpm/" + _T + "Value")
            pts.append((_fts(p.find(_T + "Time").text), int(h.text) if h is not None else None))
        cal = lap.find(_T + "Calories")
        laps.append({"start": _fts(lap.get("StartTime")), "dauer": float(lap.find(_T + "TotalTimeSeconds").text),
                     "distanz": float(lap.find(_T + "DistanceMeters").text),
                     "kcal": int(cal.text) if cal is not None else 0, "punkte": pts})
    dev = root.find(".//" + _T + "Creator/" + _T + "UnitId")
    return laps, (int(dev.text) if dev is not None else None)


def bahnen_verteilen(runden: list[tuple[float, int]], ziel_bahnen: int, bahn_m: float) -> list[int]:
    """runden: (Dauer s, gezählte Bahnen) der aktiven Runden. Streicht Bahnen (mind. 1 je Runde),
    bis ziel_bahnen erreicht sind und das Tempo möglichst nah am Schnitt liegt (exakte DP)."""
    if ziel_bahnen > sum(n for _t, n in runden) or ziel_bahnen < len(runden):
        raise ValueError("Zieldistanz passt nicht zu den gezählten Bahnen (es wird nur gestrichen)")
    p0 = sum(t for t, _n in runden) / (ziel_bahnen * bahn_m) * 100
    dp = {0: (0.0, [])}
    for t, m in runden:
        nd = {}
        for s, (c, wahl) in dp.items():
            for n in range(1, m + 1):
                if s + n > ziel_bahnen:
                    break
                cc = c + n * (t / (n * bahn_m) * 100 - p0) ** 2
                if s + n not in nd or cc < nd[s + n][0]:
                    nd[s + n] = (cc, wahl + [n])
        dp = nd
    return dp[ziel_bahnen][1]


_BT = {"enum": (0x00, "B", 0xFF), "u8": (0x02, "B", 0xFF), "u16": (0x84, "H", 0xFFFF),
       "u32": (0x86, "I", 0xFFFFFFFF), "u32z": (0x8C, "I", 0)}
_MSG = {
    "file_id": (0, [("type", 0, "enum"), ("manufacturer", 1, "u16"), ("product", 2, "u16"),
                    ("serial", 3, "u32z"), ("time_created", 4, "u32")]),
    "event": (21, [("ts", 253, "u32"), ("event", 0, "enum"), ("event_type", 1, "enum"), ("group", 4, "u8")]),
    "record": (20, [("ts", 253, "u32"), ("hr", 3, "u8"), ("dist", 5, "u32")]),
    "length": (101, [("ts", 253, "u32"), ("idx", 254, "u16"), ("event", 0, "enum"), ("event_type", 1, "enum"),
                     ("start", 2, "u32"), ("elapsed", 3, "u32"), ("timer", 4, "u32"), ("speed", 6, "u16"),
                     ("stroke", 7, "enum"), ("cal", 11, "u16"), ("ltype", 12, "enum")]),
    "lap": (19, [("ts", 253, "u32"), ("idx", 254, "u16"), ("event", 0, "enum"), ("event_type", 1, "enum"),
                 ("start", 2, "u32"), ("elapsed", 7, "u32"), ("timer", 8, "u32"), ("dist", 9, "u32"),
                 ("cal", 11, "u16"), ("speed", 13, "u16"), ("maxspeed", 14, "u16"), ("hr", 15, "u8"),
                 ("maxhr", 16, "u8"), ("trigger", 24, "enum"), ("sport", 25, "enum"), ("nlen", 32, "u16"),
                 ("first_len", 35, "u16"), ("stroke", 38, "enum"), ("subsport", 39, "enum"), ("nact", 40, "u16")]),
    "session": (18, [("ts", 253, "u32"), ("idx", 254, "u16"), ("event", 0, "enum"), ("event_type", 1, "enum"),
                     ("start", 2, "u32"), ("sport", 5, "enum"), ("subsport", 6, "enum"), ("elapsed", 7, "u32"),
                     ("timer", 8, "u32"), ("dist", 9, "u32"), ("cal", 11, "u16"), ("speed", 14, "u16"),
                     ("maxspeed", 15, "u16"), ("hr", 16, "u8"), ("maxhr", 17, "u8"), ("first_lap", 25, "u16"),
                     ("nlaps", 26, "u16"), ("trigger", 28, "enum"), ("nlen", 33, "u16"), ("stroke", 43, "enum"),
                     ("pool", 44, "u16"), ("pool_unit", 46, "enum"), ("nact", 47, "u16")]),
    "activity": (34, [("ts", 253, "u32"), ("timer", 0, "u32"), ("nsess", 1, "u16"), ("type", 2, "enum"),
                      ("event", 3, "enum"), ("event_type", 4, "enum"), ("local_ts", 5, "u32")]),
}


class _FitSchreiber:
    def __init__(self):
        self.buf = bytearray()
        self.local: dict[str, int] = {}

    def add(self, name: str, **v):
        g, fields = _MSG[name]
        if name not in self.local:
            self.local[name] = len(self.local)
            self.buf += struct.pack("<BBBHB", 0x40 | self.local[name], 0, 0, g, len(fields))
            for _k, num, t in fields:
                self.buf += struct.pack("<BBB", num, struct.calcsize(_BT[t][1]), _BT[t][0])
        self.buf += bytes([self.local[name]])
        for key, _num, t in fields:
            x = v.get(key)
            self.buf += struct.pack("<" + _BT[t][1], _BT[t][2] if x is None else int(round(x)))

    def bytes(self) -> bytes:
        h = struct.pack("<BBHI4s", 14, 0x20, 2140, 0, b".FIT") + b"\0\0"
        return _fit_schliessen(h, bytes(self.buf))


def schwimmen_tcx_zu_fit(tcx: bytes | str, distanz_m: float, bahn_m: float = 50.0,
                         utc_offset_h: float = 1.0) -> tuple[bytes, dict]:
    laps, serial = tcx_runden(tcx)
    aktiv = [L for L in laps if L["distanz"] > 0]
    ziel = int(round(distanz_m / bahn_m))
    wahl = bahnen_verteilen([(L["dauer"], int(round(L["distanz"] / bahn_m))) for L in aktiv], ziel, bahn_m)
    it = iter(wahl)
    f = _FitSchreiber()
    t0 = laps[0]["start"]
    tend = laps[-1]["start"] + laps[-1]["dauer"]
    f.add("file_id", type=4, manufacturer=1, product=3992, serial=serial, time_created=t0)
    f.add("event", ts=t0, event=0, event_type=0, group=0)
    msgs, cum, li, maxsp, hr_all, runden = [], 0.0, 0, 0.0, [], []
    for i, L in enumerate(laps):
        n = next(it) if L["distanz"] > 0 else 0
        dd, first = n * bahn_m, li
        per = L["dauer"] / n if n else L["dauer"]
        sp = bahn_m / per if n else 0.0
        maxsp = max(maxsp, sp)
        for k in range(n or 1):
            s0 = L["start"] + k * per
            msgs.append((s0 + per, 1, "length", dict(
                idx=li, event=28, event_type=1, start=s0, elapsed=per * 1000, timer=per * 1000,
                speed=sp * 1000 if n else None, stroke=0 if n else None,
                cal=round(L["kcal"] / (n or 1)), ltype=1 if n else 0)))
            li += 1
        for ts, hr in L["punkte"]:
            frac = min(max((ts - L["start"]) / L["dauer"], 0), 1) if L["dauer"] else 1
            msgs.append((ts, 0, "record", dict(ts=ts, hr=hr, dist=(cum + dd * frac) * 100)))
            if hr:
                hr_all.append(hr)
        hrs = [h for _t, h in L["punkte"] if h]
        msgs.append((L["start"] + L["dauer"], 2, "lap", dict(
            idx=i, event=9, event_type=1, start=L["start"], elapsed=L["dauer"] * 1000, timer=L["dauer"] * 1000,
            dist=dd * 100, cal=L["kcal"], speed=(dd / L["dauer"]) * 1000 if n else 0,
            maxspeed=sp * 1000 if n else 0, hr=sum(hrs) / len(hrs) if hrs else None,
            maxhr=max(hrs) if hrs else None, trigger=0, sport=5, nlen=n or 1, first_len=first,
            stroke=5 if n else None, subsport=17, nact=n)))
        if n:
            runden.append((int(L["distanz"]), int(dd), round(L["dauer"])))
        cum += dd
    msgs.sort(key=lambda m: (m[0], m[1]))
    for ts, _prio, name, v in msgs:
        v.setdefault("ts", ts)
        f.add(name, **v)
    total = tend - t0
    f.add("event", ts=tend, event=0, event_type=4, group=0)
    f.add("session", ts=tend, idx=0, event=8, event_type=1, start=t0, sport=5, subsport=17,
          elapsed=total * 1000, timer=total * 1000, dist=cum * 100, cal=sum(L["kcal"] for L in laps),
          speed=cum / total * 1000, maxspeed=maxsp * 1000,
          hr=sum(hr_all) / len(hr_all) if hr_all else None, maxhr=max(hr_all) if hr_all else None,
          first_lap=0, nlaps=len(laps), trigger=0, nlen=li, stroke=5, pool=bahn_m * 100, pool_unit=0, nact=ziel)
    f.add("activity", ts=tend, timer=total * 1000, nsess=1, type=0, event=26, event_type=1,
          local_ts=tend + utc_offset_h * 3600)
    aktiv_s = sum(L["dauer"] for L in aktiv)
    return f.bytes(), {"distanz_uhr": sum(L["distanz"] for L in laps), "distanz": cum, "bahnen": ziel,
                       "pausen": li - ziel, "aktiv_min": aktiv_s / 60, "pace_s_100": aktiv_s / cum * 100,
                       "runden": runden}
