"""Schwarz-weiß-Illustrationen (inline SVG) für das Skizzenbuch."""
import math
import random

_id = [0]


def uid(p="g"):
    _id[0] += 1
    return f"{p}{_id[0]}"


def f(n):
    return f"{n:.1f}"


def svg(w, h, body, style=""):
    return (f'<svg class="ill" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="{style}">{body}</svg>')


def line(a, b, c="ln"):
    return f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" class="{c}"/>'


def poly(pts, c="ln", closed=True, extra=""):
    tag = "polygon" if closed else "polyline"
    s = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    return f'<{tag} points="{s}" class="{c}" {extra}/>'


def circ(cx, cy, r, c="ln", extra=""):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{c}" {extra}/>'


def ell(cx, cy, rx, ry, c="ln", rot=0, extra=""):
    if isinstance(rot, str):
        extra, rot = rot, 0
    t = f' transform="rotate({f(rot)} {f(cx)} {f(cy)})"' if rot else ""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" class="{c}"{t} {extra}/>'


def path(d, c="ln", extra=""):
    return f'<path d="{d}" class="{c}" {extra}/>'


def text(x, y, s, c="lab", anchor="start"):
    return f'<text x="{f(x)}" y="{f(y)}" class="{c}" text-anchor="{anchor}">{s}</text>'


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-9:
        return p2
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def smooth(pts, closed=False, k=0.5):
    """Catmull-Rom-Spline durch Punkte -> SVG-Pfad."""
    n = len(pts)
    if closed:
        P = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        P = [pts[0]] + pts + [pts[-1]]
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    rng = n if closed else n - 1
    for i in range(1, rng + 1):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 3, p1[1] + (p2[1] - p0[1]) * k / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 3, p2[1] - (p3[1] - p1[1]) * k / 3)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + (" Z" if closed else "")


def leader(p, q, label, anchor="start", c="labs"):
    dx = 3 if anchor == "start" else -3
    return line(p, q, "lead") + circ(p[0], p[1], 1.6, "dot") + text(q[0] + dx, q[1] + 3, label, c, anchor)


def arrow(a, b, c="ln"):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    l = 8
    p1 = (b[0] - l * math.cos(ang - 0.4), b[1] - l * math.sin(ang - 0.4))
    p2 = (b[0] - l * math.cos(ang + 0.4), b[1] - l * math.sin(ang + 0.4))
    return line(a, b, c) + poly([b, p1, p2], "fillk")


def hatch(x, y, w, h, angle, sp, c="hat", clip_shape=None):
    cid = uid("clip")
    shape = clip_shape or f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/>'
    out = f'<clipPath id="{cid}">{shape}</clipPath><g clip-path="url(#{cid})">'
    cx, cy = x + w / 2, y + h / 2
    R = math.hypot(w, h)
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    t = -R
    while t <= R:
        px, py = cx + nx * t, cy + ny * t
        out += line((px - dx * R, py - dy * R), (px + dx * R, py + dy * R), c)
        t += sp
    return out + "</g>"


# ---------------------------------------------------------------- Material

def pencil_scale():
    grades = [("4H", "#f2f2f2"), ("2H", "#e2e2e2"), ("HB", "#c4c4c4"), ("2B", "#9e9e9e"),
              ("4B", "#727272"), ("6B", "#474747"), ("8B", "#1e1e1e")]
    b = ""
    w = 64
    for i, (g, col) in enumerate(grades):
        x = 10 + i * (w + 6)
        b += f'<rect x="{x}" y="70" width="{w}" height="34" style="fill:{col}" class="lt"/>'
        b += text(x + w / 2, 122, g, "labb", "middle")
    # Bleistift
    b += poly([(40, 22), (440, 22), (440, 46), (40, 46)], "ln")
    b += line((40, 29), (440, 29), "lt") + line((40, 39), (440, 39), "lt")
    b += poly([(440, 22), (482, 34), (440, 46)], "ln")
    b += poly([(472, 31), (482, 34), (472, 37)], "fillk")
    b += poly([(18, 22), (40, 22), (40, 46), (18, 46)], "ln")
    b += line((26, 22), (26, 46), "lt")
    b += arrow((150, 145), (20, 145), "lt") + arrow((370, 145), (500, 145), "lt")
    b += text(160, 149, "H = hart, hell, spitz", "labs") + text(360, 149, "B = weich, dunkel", "labs", "end")
    return svg(520, 158, b)


# ---------------------------------------------------------------- Linien

def dots_exercise(w, h, n, seed, minlen=60, maxlen=200):
    rnd = random.Random(seed)
    b = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" class="frame"/>'
    for _ in range(n):
        for _try in range(50):
            x1, y1 = rnd.uniform(20, w - 20), rnd.uniform(20, h - 20)
            a = rnd.uniform(0, math.pi * 2)
            L = rnd.uniform(minlen, maxlen)
            x2, y2 = x1 + math.cos(a) * L, y1 + math.sin(a) * L
            if 20 < x2 < w - 20 and 20 < y2 < h - 20:
                break
        k = _ + 1
        b += circ(x1, y1, 2.8, "dot") + circ(x2, y2, 2.8, "dot")
        b += text(x1 + 5, y1 - 4, str(k), "labs") + text(x2 + 5, y2 - 4, str(k), "labs")
    return svg(w, h, b)


def line_demo():
    b = ""
    # Ghosting
    b += circ(30, 60, 3, "dot") + circ(200, 30, 3, "dot")
    for i, off in enumerate([-14, -9, -4]):
        b += line((30, 60 + off), (200, 30 + off), "cn")
    b += line((30, 60), (200, 30), "ln")
    b += text(115, 92, "1. Punkte setzen, 2. Bewegung in der Luft", "labs", "middle")
    b += text(115, 104, "üben (Ghosting), 3. in einem Zug ziehen", "labs", "middle")
    # Ellipsen
    for i in range(5):
        b += ell(330, 55, 70 - i * 0.8, 26 + i * 0.6, "lt", rot=-8 + i)
    b += text(330, 104, "Ellipsen: 2–3 Mal locker umkreisen,", "labs", "middle")
    b += text(330, 116, "dann sauber nachziehen", "labs", "middle")
    # Schulter/Ellbogen/Handgelenk
    b += path("M440,85 Q490,10 540,85", "ln") + text(490, 104, "lange Linie: aus der Schulter", "labs", "middle")
    b += path("M465,60 Q490,40 515,60", "lt")
    return svg(560, 122, b)


# ---------------------------------------------------------------- Tonwerte

def value_scale(filled=True, n=7, w=520):
    cols = ["#ffffff", "#e6e6e6", "#c8c8c8", "#a0a0a0", "#777777", "#4a4a4a", "#141414"]
    bw = (w - 20) / n
    b = ""
    for i in range(n):
        fill = cols[i] if filled else "#ffffff"
        b += f'<rect x="{f(10+i*bw)}" y="8" width="{f(bw)}" height="52" style="fill:{fill}" class="lt"/>'
        b += text(10 + i * bw + bw / 2, 76, str(i + 1), "labs", "middle")
    return svg(w, 82, b)


def hatch_demo():
    b = ""
    s = 92
    labels = ["Parallel", "Kreuz", "Dreifach", "Punkte", "Kritzeln", "Verwischen"]
    rnd = random.Random(4)
    for i, lab in enumerate(labels):
        x, y = 8 + i * (s + 12), 8
        if i == 0:
            b += hatch(x, y, s, s, -45, 6)
        elif i == 1:
            b += hatch(x, y, s, s, -45, 6) + hatch(x, y, s, s, 45, 6)
        elif i == 2:
            b += hatch(x, y, s, s, -45, 5) + hatch(x, y, s, s, 45, 5) + hatch(x, y, s, s, 0, 5)
        elif i == 3:
            for _ in range(420):
                px, py = rnd.uniform(x + 2, x + s - 2), rnd.uniform(y + 2, y + s - 2)
                if rnd.random() < (px - x) / s + 0.1:
                    b += circ(px, py, 1.0, "dot")
        elif i == 4:
            pts = []
            for k in range(160):
                pts.append((x + 8 + rnd.random() * (s - 16), y + 8 + (k / 160) * (s - 16) + rnd.uniform(-6, 6)))
            b += path(smooth(pts, k=0.9), "lt")
        else:
            gid = uid("lg")
            b += (f'<defs><linearGradient id="{gid}"><stop offset="0" stop-color="#fff"/>'
                  f'<stop offset="1" stop-color="#222"/></linearGradient></defs>'
                  f'<rect x="{x}" y="{y}" width="{s}" height="{s}" style="fill:url(#{gid})"/>')
        b += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" class="lt"/>'
        b += text(x + s / 2, y + s + 15, lab, "labb", "middle")
    return svg(6 * (s + 12), s + 28, b)


def sphere_light():
    gid, sid = uid("rg"), uid("rg")
    b = (f'<defs><radialGradient id="{gid}" cx="0.36" cy="0.34" r="0.75">'
         f'<stop offset="0" stop-color="#ffffff"/><stop offset="0.12" stop-color="#f4f4f4"/>'
         f'<stop offset="0.45" stop-color="#bdbdbd"/><stop offset="0.72" stop-color="#4a4a4a"/>'
         f'<stop offset="0.86" stop-color="#3a3a3a"/><stop offset="1" stop-color="#7a7a7a"/>'
         f'</radialGradient>'
         f'<radialGradient id="{sid}" cx="0.4" cy="0.5" r="0.6"><stop offset="0" stop-color="#111"/>'
         f'<stop offset="1" stop-color="#bbb" stop-opacity="0"/></radialGradient></defs>')
    cx, cy, r = 210, 130, 85
    b += ell(cx + 70, cy + r - 4, 110, 22, "none", extra=f'style="fill:url(#{sid})"')
    b += line((40, cy + r + 18), (500, cy + r + 18), "cs")
    b += circ(cx, cy, r, "lt", extra=f'style="fill:url(#{gid})"')
    # Sonne
    b += circ(42, 30, 12, "ln")
    for k in range(8):
        a = k * math.pi / 4
        b += line((42 + math.cos(a) * 16, 30 + math.sin(a) * 16), (42 + math.cos(a) * 22, 30 + math.sin(a) * 22), "lt")
    b += arrow((60, 46), (130, 86), "cn")
    b += text(30, 64, "Licht", "labs")
    lx = 330
    b += leader((cx - 32, cy - 36), (lx, 30), "Glanzlicht (Papier weiß lassen)")
    b += leader((cx - 5, cy - 5), (lx, 58), "Licht / Halbton")
    b += leader((cx + 45, cy + 35), (lx, 100), "Kernschatten (dunkelste Stelle am Körper)")
    b += leader((cx + 76, cy + 30), (lx + 25, 128), "Reflexlicht (etwas heller, Rand)")
    b += leader((cx + 150, cy + r - 2), (lx + 70, 172), "Schlagschatten")
    b += leader((cx + 55, cy + r + 1), (lx + 8, 198), "Kontaktschatten (fast schwarz)")
    return svg(560, 240, b)


# ---------------------------------------------------------------- Grundformen

def basic_shapes():
    b = ""
    # Würfel (2-Punkt, schematisch)
    f0, f1 = (60, 150), (60, 85)
    l0, l1 = (18, 128), (18, 66)
    r0, r1 = (118, 130), (118, 68)
    back = (76, 50)
    b += poly([f0, l0, l1, f1], "ln") + poly([f0, r0, r1, f1], "ln") + poly([f1, l1, back, r1], "ln")
    bb = (76, 110)
    b += line(l0, bb, "hid") + line(r0, bb, "hid") + line(bb, back, "hid")
    b += text(68, 185, "Würfel", "labb", "middle")
    # Zylinder
    cx = 210
    b += ell(cx, 60, 40, 13, "ln") + line((cx - 40, 60), (cx - 40, 145), "ln") + line((cx + 40, 60), (cx + 40, 145), "ln")
    b += path(f"M{cx-40},145 A40,15 0 0 0 {cx+40},145", "ln") + path(f"M{cx-40},145 A40,15 0 0 1 {cx+40},145", "hid")
    b += line((cx, 45), (cx, 165), "cn")
    b += text(cx, 185, "Zylinder", "labb", "middle")
    # Kegel
    cx = 330
    b += path(f"M{cx-42},145 A42,14 0 0 0 {cx+42},145", "ln") + path(f"M{cx-42},145 A42,14 0 0 1 {cx+42},145", "hid")
    b += line((cx - 42, 145), (cx, 45), "ln") + line((cx + 42, 145), (cx, 45), "ln") + line((cx, 45), (cx, 145), "cn")
    b += text(cx, 185, "Kegel", "labb", "middle")
    # Kugel
    cx = 450
    b += circ(cx, 100, 50, "ln") + path(f"M{cx-50},100 A50,15 0 0 0 {cx+50},100", "cs")
    b += path(f"M{cx-50},100 A50,15 0 0 1 {cx+50},100", "cn") + path(f"M{cx},50 A16,50 0 0 0 {cx},150", "cs")
    b += text(cx, 185, "Kugel", "labb", "middle")
    return svg(520, 195, b)


def one_point():
    W, H = 520, 250
    hy, vp = 95, (260, 95)
    b = line((10, hy), (W - 10, hy), "ln") + circ(vp[0], vp[1], 4, "dot")
    b += text(14, hy - 6, "Horizont = Augenhöhe", "labs") + text(vp[0], hy - 10, "FP", "labb", "middle")

    def box(x, y, w, h, s):
        out = ""
        fr = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        bk = [lerp(p, vp, s) for p in fr]
        for p, q in zip(fr, bk):
            out += line(p, vp, "cn") + line(p, q, "ln")
        out += poly(fr, "ln") + poly(bk, "lt")
        return out
    b += box(40, 150, 90, 60, 0.3) + box(350, 140, 110, 70, 0.28) + box(80, 20, 70, 45, 0.3)
    b += box(380, 25, 80, 40, 0.3)
    b += text(260, 240, "unter Augenhöhe: Oberseite sichtbar", "labs", "middle")
    b += text(260, 14, "über Augenhöhe: Unterseite sichtbar", "labs", "middle")
    return svg(W, H, b)


def two_pt_box(vl, vr, base, h, fl, fr):
    P = base
    T = (P[0], P[1] - h)
    L = lerp(P, vl, fl)
    R = lerp(P, vr, fr)
    TL = inter(T, vl, L, (L[0], L[1] - 10))
    TR = inter(T, vr, R, (R[0], R[1] - 10))
    B = inter(L, vr, R, vl)
    TB = inter(TL, vr, TR, vl)
    return dict(P=P, T=T, L=L, R=R, TL=TL, TR=TR, B=B, TB=TB)


def draw_box(k, vl, vr, guides=True, hidden=True):
    o = ""
    if guides:
        for p in ("T", "TL", "L", "P"):
            o += line(k[p], vr, "cn")
        for p in ("T", "TR", "R", "P"):
            o += line(k[p], vl, "cn")
    o += poly([k["P"], k["L"], k["TL"], k["T"]], "ln") + poly([k["P"], k["R"], k["TR"], k["T"]], "ln")
    top_vis = k["T"][1] > k["TB"][1] - 0.01 and k["T"][1] > vl[1]
    if k["P"][1] > vl[1]:
        o += poly([k["T"], k["TL"], k["TB"], k["TR"]], "ln")
    if hidden:
        o += line(k["L"], k["B"], "hid") + line(k["R"], k["B"], "hid") + line(k["B"], k["TB"], "hid")
        if k["P"][1] <= vl[1]:
            o += line(k["TL"], k["TB"], "hid") + line(k["TR"], k["TB"], "hid")
    return o


def two_point():
    W, H = 520, 260
    hy = 80
    vl, vr = (12, hy), (508, hy)
    b = line((0, hy), (W, hy), "ln") + circ(vl[0], hy, 4, "dot") + circ(vr[0], hy, 4, "dot")
    b += text(16, hy - 8, "FP links", "labb") + text(504, hy - 8, "FP rechts", "labb", "end")
    k = two_pt_box(vl, vr, (230, 230), 90, 0.33, 0.30)
    b += draw_box(k, vl, vr)
    k2 = two_pt_box(vl, vr, (420, 60), 35, 0.25, 0.25)
    b += draw_box(k2, vl, vr, guides=False)
    b += text(230, 252, "Senkrechte bleiben senkrecht – alles andere läuft zu einem der Fluchtpunkte", "labs", "middle")
    return svg(W, H, b)


def persp_sheet(kind=2):
    W, H = 560, 760
    hy = 300
    b = f'<rect x="1" y="1" width="{W-2}" height="{H-2}" class="frame"/>'
    b += line((2, hy), (W - 2, hy), "cs")
    if kind == 2:
        b += circ(8, hy, 4, "dot") + circ(W - 8, hy, 4, "dot")
        b += text(14, hy - 7, "FP", "labs") + text(W - 14, hy - 7, "FP", "labs", "end")
    else:
        b += circ(W / 2, hy, 4, "dot") + text(W / 2, hy - 8, "FP", "labs", "middle")
    b += text(10, hy + 14, "Horizont", "labs")
    return svg(W, H, b)


def ellipses_demo():
    b = ""
    cx = 120
    hy = 22
    b += line((20, hy), (230, hy), "ln") + text(232, hy + 3, "Augenhöhe", "labs")
    for i, y in enumerate([40, 85, 135, 190]):
        ry = 3 + i * 8
        b += ell(cx, y, 70, ry, "ln")
        b += line((cx - 74, y), (cx + 74, y), "cn")
    b += line((cx, 30), (cx, 205), "cn")
    b += text(cx, 222, "je weiter weg vom Horizont, desto runder", "labs", "middle")
    # Fehler
    x = 330
    b += path(f"M{x-60},70 Q{x},40 {x+60},70 Q{x},100 {x-60},70", "ln")
    b += text(x, 115, "falsch: spitze Enden", "labb", "middle")
    b += text(x, 128, "(wie ein Auge)", "labs", "middle")
    b += ell(x, 175, 60, 22, "ln")
    b += text(x, 218, "richtig: Enden rund", "labb", "middle")
    # Zylinder
    x2 = 470
    b += ell(x2, 50, 42, 8, "ln") + line((x2 - 42, 50), (x2 - 42, 180), "ln") + line((x2 + 42, 50), (x2 + 42, 180), "ln")
    b += path(f"M{x2-42},180 A42,20 0 0 0 {x2+42},180", "ln") + path(f"M{x2-42},180 A42,20 0 0 1 {x2+42},180", "hid")
    b += ell(x2, 115, 42, 14, "cn")
    b += text(x2, 218, "unten runder als oben", "labs", "middle")
    return svg(540, 230, b)


# ---------------------------------------------------------------- Köpfe

def head_front(cx, cy, r, construct=True, finished=True, labels=False):
    u = 0.7 * r
    hair, brow, nose, chin = cy - u, cy, cy + u, cy + 2 * u
    top = cy - r
    eye = (top + chin) / 2
    b = ""
    if construct:
        b += circ(cx, cy, r, "cs")
        b += line((cx - 0.8 * r, cy - 0.6 * r), (cx - 0.8 * r, cy + 0.6 * r), "cn")
        b += line((cx + 0.8 * r, cy - 0.6 * r), (cx + 0.8 * r, cy + 0.6 * r), "cn")
        b += line((cx, top - 8), (cx, chin + 6), "cn")
        for y in (hair, brow, nose, chin):
            b += line((cx - r - 6, y), (cx + r + 6, y), "cn")
        b += line((cx - r, eye), (cx + r, eye), "cn")
        if not finished:
            b += path(f"M{f(cx-0.8*r)},{f(cy+0.6*r)} C{f(cx-0.8*r)},{f(cy+1.0*r)} {f(cx-0.4*r)},{f(chin)} {f(cx)},{f(chin)}"
                      f" C{f(cx+0.4*r)},{f(chin)} {f(cx+0.8*r)},{f(cy+1.0*r)} {f(cx+0.8*r)},{f(cy+0.6*r)}", "ln")
    if finished:
        A = (cx - 0.8 * r, cy + 0.6 * r)
        B = (cx + 0.8 * r, cy + 0.6 * r)
        b += path(f"M{f(A[0])},{f(A[1])} A{f(r)},{f(r)} 0 1 1 {f(B[0])},{f(B[1])}"
                  f" C{f(cx+0.8*r)},{f(cy+1.0*r)} {f(cx+0.4*r)},{f(chin)} {f(cx)},{f(chin)}"
                  f" C{f(cx-0.4*r)},{f(chin)} {f(cx-0.8*r)},{f(cy+1.0*r)} {f(A[0])},{f(A[1])}", "ln")
        ew, eh = 0.16 * r, 0.075 * r
        for s in (-1, 1):
            ex = cx + s * 0.34 * r
            b += path(f"M{f(ex-ew)},{f(eye)} Q{f(ex)},{f(eye-eh*1.9)} {f(ex+ew)},{f(eye)} "
                      f"Q{f(ex)},{f(eye+eh*1.5)} {f(ex-ew)},{f(eye)}", "ln")
            b += circ(ex, eye, eh * 0.95, "lt") + circ(ex, eye, eh * 0.42, "dot")
            b += path(f"M{f(ex-ew*0.95)},{f(eye-eh*1.6)} Q{f(ex)},{f(eye-eh*2.9)} {f(ex+ew)},{f(eye-eh*1.6)}", "lt")
            b += path(f"M{f(ex-ew*1.2)},{f(brow-0.02*r)} Q{f(ex)},{f(brow-0.13*r)} {f(ex+s*ew*1.3 if s>0 else ex+ew*1.2)},{f(brow-0.04*r)}", "ln")
            # Ohr
            ox = cx + s * 0.8 * r
            b += path(f"M{f(ox)},{f(brow+0.04*r)} C{f(ox+s*0.2*r)},{f(brow-0.04*r)} {f(ox+s*0.2*r)},{f(nose)} "
                      f"{f(ox+s*0.02*r)},{f(nose)}", "ln")
            # Nase
            b += path(f"M{f(cx+s*0.06*r)},{f(nose-0.02*r)} Q{f(cx+s*0.17*r)},{f(nose-0.03*r)} {f(cx+s*0.15*r)},{f(nose-0.12*r)}", "ln")
        b += path(f"M{f(cx-0.06*r)},{f(nose-0.02*r)} Q{f(cx)},{f(nose+0.03*r)} {f(cx+0.06*r)},{f(nose-0.02*r)}", "ln")
        b += line((cx - 0.06 * r, brow + 0.12 * r), (cx - 0.08 * r, nose - 0.18 * r), "lt")
        my = nose + u / 3
        mw = 0.24 * r
        b += path(f"M{f(cx-mw)},{f(my)} Q{f(cx-mw/2)},{f(my-0.04*r)} {f(cx)},{f(my-0.01*r)} "
                  f"Q{f(cx+mw/2)},{f(my-0.04*r)} {f(cx+mw)},{f(my)}", "ln")
        b += path(f"M{f(cx-mw*0.5)},{f(my+0.11*r)} Q{f(cx)},{f(my+0.16*r)} {f(cx+mw*0.5)},{f(my+0.11*r)}", "lt")
        b += path(f"M{f(cx-0.18*r)},{f(my-0.1*r)} Q{f(cx)},{f(my-0.14*r)} {f(cx+0.18*r)},{f(my-0.1*r)}", "none")
        # Hals
        b += line((cx - 0.42 * r, cy + 1.25 * r), (cx - 0.45 * r, chin + 0.55 * r), "ln")
        b += line((cx + 0.42 * r, cy + 1.25 * r), (cx + 0.45 * r, chin + 0.55 * r), "ln")
    if labels:
        lx = cx + r + 14
        b += text(lx, hair + 4, "Haaransatz", "labs") + text(lx, brow + 4, "Brauen", "labs")
        b += text(lx, eye + 4, "Augen (Kopfmitte!)", "labs") + text(lx, nose + 4, "Nasenunterkante", "labs")
        b += text(lx, nose + u / 3 + 4, "Mund (1/3)", "labs") + text(lx, chin + 4, "Kinn", "labs")
        b += text(lx, top + 4, "Schädeldecke", "labs")
    return b


def head_side(cx, cy, r, construct=True, finished=True):
    u = 0.7 * r
    b = ""
    if construct:
        b += circ(cx, cy, r, "cs") + ell(cx + 0.05 * r, cy, 0.55 * r, u, "cn")
        b += line((cx + 0.05 * r, cy - u - 10), (cx + 0.05 * r, cy + 2 * u + 5), "cn")
        b += line((cx + 0.95 * r, cy - u), (cx + 0.98 * r, cy + 2 * u), "cn")
        for y in (cy - u, cy, cy + u, cy + 2 * u):
            b += line((cx - r - 6, y), (cx + 1.3 * r, y), "cn")
        b += line((cx + 0.98 * r, cy + 2 * u), (cx + 0.05 * r, cy + 1.1 * r), "cn")
    if finished:
        pts = [(cx - 0.62 * r, cy + 0.85 * r), (cx - 0.98 * r, cy + 0.2 * r), (cx - 0.9 * r, cy - 0.45 * r),
               (cx - 0.4 * r, cy - 0.93 * r), (cx + 0.25 * r, cy - 0.98 * r), (cx + 0.75 * r, cy - 0.68 * r),
               (cx + 0.93 * r, cy - 0.3 * r), (cx + 0.98 * r, cy - 0.02 * r), (cx + 0.93 * r, cy + 0.14 * r),
               (cx + 1.08 * r, cy + 0.42 * r), (cx + 1.2 * r, cy + 0.64 * r), (cx + 1.08 * r, cy + 0.72 * r),
               (cx + 1.05 * r, cy + 0.8 * r), (cx + 1.08 * r, cy + 0.9 * r), (cx + 1.02 * r, cy + 0.97 * r),
               (cx + 1.06 * r, cy + 1.05 * r), (cx + 0.98 * r, cy + 1.16 * r), (cx + 1.02 * r, cy + 1.32 * r),
               (cx + 0.82 * r, cy + 1.42 * r), (cx + 0.55 * r, cy + 1.38 * r)]
        b += path(smooth(pts, k=0.8), "ln")
        b += path(smooth([(cx + 0.55 * r, cy + 1.38 * r), (cx + 0.2 * r, cy + 1.25 * r), (cx + 0.02 * r, cy + 1.05 * r)], k=0.6), "ln")
        b += line((cx + 0.6 * r, cy + 1.4 * r), (cx + 0.55 * r, cy + 2.1 * r), "ln")
        b += line((cx - 0.55 * r, cy + 0.95 * r), (cx - 0.5 * r, cy + 2.0 * r), "ln")
        # Ohr
        ox = cx - 0.05 * r
        b += path(smooth([(ox + 0.12 * r, cy + 0.02 * r), (ox - 0.05 * r, cy - 0.02 * r), (ox - 0.2 * r, cy + 0.25 * r),
                          (ox - 0.12 * r, cy + 0.6 * r), (ox + 0.06 * r, cy + 0.72 * r), (ox + 0.1 * r, cy + 0.6 * r)], k=0.8), "ln")
        b += path(smooth([(ox + 0.05 * r, cy + 0.15 * r), (ox - 0.08 * r, cy + 0.3 * r), (ox + 0.02 * r, cy + 0.45 * r)]), "lt")
        # Auge
        ex, ey = cx + 0.84 * r, cy + 0.2 * r
        b += path(f"M{f(ex-0.1*r)},{f(ey-0.05*r)} L{f(ex+0.04*r)},{f(ey)} L{f(ex-0.08*r)},{f(ey+0.05*r)}", "ln")
        b += path(f"M{f(ex-0.14*r)},{f(cy+0.02*r)} Q{f(ex)},{f(cy-0.07*r)} {f(ex+0.1*r)},{f(cy+0.01*r)}", "ln")
        b += path(f"M{f(cx+1.0*r)},{f(cy+0.67*r)} Q{f(cx+0.95*r)},{f(cy+0.6*r)} {f(cx+1.03*r)},{f(cy+0.57*r)}", "lt")
        b += line((cx + 1.03 * r, cy + 0.97 * r), (cx + 0.93 * r, cy + 0.98 * r), "lt")
    return b


def heads_construction():
    b = head_front(140, 120, 80, construct=True, finished=False)
    b += text(140, 315, "1. Kugel, Seiten abschneiden,", "labs", "middle")
    b += text(140, 327, "Mittellinie, Kiefer", "labs", "middle")
    b += head_side(390, 120, 80, construct=True, finished=True)
    b += text(400, 297 - 12 + 30, "", "labs") + text(400, 285 + 30, "Seitenansicht: Ohr sitzt", "labs", "middle")
    b += text(400, 327, "hinter der Kopfmitte", "labs", "middle")
    # Drittel-Klammer
    x = 248
    for y0, y1 in ((64, 120), (120, 176), (176, 232)):
        b += path(f"M{x},{y0+2} Q{x+7},{y0+2} {x+7},{(y0+y1)/2} Q{x+7},{y1-2} {x},{y1-2}", "lt")
    b += text(x + 12, 125, "3 gleiche", "labs") + text(x + 12, 137, "Abstände", "labs")
    return svg(540, 335, b)


def head_proportions():
    b = head_front(170, 115, 82, construct=True, finished=True, labels=True)
    # Augenbreite
    return svg(370, 300, b)


def features():
    b = ""
    # Auge (groß)
    x, y = 90, 60
    b += path(f"M{x-60},{y} Q{x-5},{y-42} {x+60},{y+2} Q{x},{y+30} {x-60},{y}", "ln")
    b += path(f"M{x-52},{y-12} Q{x},{y-58} {x+58},{y-8}", "lt")
    cid = uid("clip")
    b += f'<clipPath id="{cid}"><path d="M{x-60},{y} Q{x-5},{y-42} {x+60},{y+2} Q{x},{y+30} {x-60},{y}"/></clipPath>'
    b += f'<g clip-path="url(#{cid})">' + circ(x, y - 2, 21, "ln", 'style="fill:#bdbdbd"') + circ(x, y - 2, 9, "dot") + "</g>"
    b += circ(x + 6, y - 9, 4, "ln", 'style="fill:#fff" stroke="none"')
    b += path(f"M{x-60},{y} q-3,-2 -8,-1", "lt")
    b += text(x, y + 48, "Auge", "labb", "middle")
    b += text(x, y + 61, "Mandelform, Iris oben vom Lid", "labs", "middle")
    b += text(x, y + 73, "verdeckt, Glanzpunkt weiß lassen", "labs", "middle")
    # Nase
    x, y = 280, 40
    b += poly([(x, y - 25), (x - 16, y + 35), (x + 16, y + 35)], "cn")
    b += poly([(x - 16, y + 35), (x - 30, y + 45), (x + 30, y + 45), (x + 16, y + 35)], "cn")
    b += path(f"M{x-12},{y+48} Q{x-32},{y+48} {x-28},{y+34} Q{x-24},{y+24} {x-14},{y+30}", "ln")
    b += path(f"M{x+12},{y+48} Q{x+32},{y+48} {x+28},{y+34} Q{x+24},{y+24} {x+14},{y+30}", "ln")
    b += path(f"M{x-10},{y+44} Q{x},{y+54} {x+10},{y+44}", "ln")
    b += path(f"M{x-6},{y-22} Q{x-8},{y+10} {x-10},{y+22}", "lt")
    b += text(x, y + 68, "Nase", "labb", "middle")
    b += text(x, y + 81, "erst Keil/Block, dann Nasenflügel", "labs", "middle")
    b += text(x, y + 93, "nur andeuten – Schatten statt Linien", "labs", "middle")
    # Mund
    x, y = 470, 55
    b += line((x - 55, y), (x + 55, y), "cn") + line((x, y - 25), (x, y + 30), "cn")
    b += path(f"M{x-50},{y} Q{x-25},{y-6} {x-8},{y-2} L{x},{y+2} L{x+8},{y-2} Q{x+25},{y-6} {x+50},{y}", "ln")
    b += path(f"M{x-44},{y-1} Q{x-25},{y-22} {x-8},{y-18} Q{x},{y-14} {x+8},{y-18} Q{x+25},{y-22} {x+44},{y-1}", "lt")
    b += path(f"M{x-34},{y+4} Q{x},{y+30} {x+34},{y+4}", "lt")
    b += hatch(x - 30, y + 14, 60, 14, -30, 3.2, "hat", f'<path d="M{x-30},{y+20} Q{x},{y+34} {x+30},{y+20} L{x},{y+28}Z"/>')
    b += text(x, y + 53, "Mund", "labb", "middle")
    b += text(x, y + 66, "Mittellinie am dunkelsten,", "labs", "middle")
    b += text(x, y + 78, "Unterlippe nur durch Schatten", "labs", "middle")
    return svg(560, 160, b)


def ear_and_eyes_spacing():
    b = ""
    # Ohr
    x, y = 70, 20
    b += path(smooth([(x + 30, y + 10), (x + 5, y), (x - 20, y + 30), (x - 15, y + 80), (x + 5, y + 110),
                      (x + 20, y + 105), (x + 25, y + 80)], k=0.8), "ln")
    b += path(smooth([(x + 22, y + 25), (x - 2, y + 22), (x - 8, y + 50), (x + 5, y + 70), (x + 15, y + 85)], k=0.8), "lt")
    b += path(smooth([(x + 18, y + 45), (x + 8, y + 55), (x + 18, y + 70)]), "lt")
    b += text(x + 5, y + 135, "Ohr: wie ein Fragezeichen", "labs", "middle")
    # Augen-Abstand
    x0, y0 = 190, 70
    for i in range(5):
        xs = x0 + i * 66
        if i in (1, 3):
            b += path(f"M{xs},{y0} Q{xs+33},{y0-22} {xs+66},{y0} Q{xs+33},{y0+18} {xs},{y0}", "ln")
            b += circ(xs + 33, y0 - 1, 9, "lt") + circ(xs + 33, y0 - 1, 4, "dot")
        else:
            b += path(f"M{xs},{y0} Q{xs+33},{y0-22} {xs+66},{y0} Q{xs+33},{y0+18} {xs},{y0}", "cn")
        b += line((xs, y0 + 28), (xs, y0 + 38), "lt")
    b += line((x0 + 330, y0 + 28), (x0 + 330, y0 + 38), "lt") + line((x0, y0 + 33), (x0 + 330, y0 + 33), "lt")
    b += text(x0 + 165, y0 + 55, "Kopfbreite = 5 Augenbreiten · Abstand zwischen den Augen = 1 Auge", "labs", "middle")
    b += path(f"M{x0+99},{y0+62} L{x0+99},{y0+84} M{x0+231},{y0+62} L{x0+231},{y0+84}", "cn")
    b += text(x0 + 165, y0 + 97, "Mundwinkel ≈ unter den Pupillen", "labs", "middle")
    return svg(560, 175, b)


def head_turns():
    b = ""
    r = 62
    # Front
    b += head_front(100, 90, r, construct=True, finished=False)
    b += text(100, 250, "frontal", "labb", "middle")
    # 3/4
    cx, cy = 290, 90
    u = 0.7 * r
    b += circ(cx, cy, r, "cs")
    b += path(f"M{cx},{cy-r} A{0.62*r},{r} 0 0 1 {cx},{cy+r}", "cn")
    b += ell(cx - 0.52 * r, cy + 0.05 * r, 0.3 * r, 0.62 * r, "cn")
    for y in (cy - u, cy, cy + u):
        b += line((cx - r - 4, y), (cx + r + 10, y), "cn")
    b += line((cx + 0.45 * r, cy + 0.62 * r), (cx + 0.42 * r, cy + 2 * u), "cn")
    jaw = smooth([(cx - 0.6 * r, cy + 0.65 * r), (cx - 0.35 * r, cy + 1.2 * r), (cx + 0.15 * r, cy + 2 * u),
                  (cx + 0.48 * r, cy + 2 * u - 2), (cx + 0.75 * r, cy + 1.0 * r), (cx + 0.9 * r, cy + 0.45 * r)], k=0.6)
    outline = [(cx - 0.45 * r, cy + 0.85 * r), (cx - 0.85 * r, cy + 0.45 * r), (cx - 1.0 * r, cy - 0.1 * r),
               (cx - 0.8 * r, cy - 0.65 * r), (cx - 0.3 * r, cy - 0.98 * r), (cx + 0.3 * r, cy - 0.97 * r),
               (cx + 0.75 * r, cy - 0.65 * r), (cx + 0.93 * r, cy - 0.2 * r), (cx + 0.86 * r, cy + 0.12 * r),
               (cx + 0.9 * r, cy + 0.42 * r), (cx + 0.8 * r, cy + 1.0 * r), (cx + 0.55 * r, cy + 1.36 * r),
               (cx + 0.2 * r, cy + 1.4 * r), (cx - 0.25 * r, cy + 1.15 * r), (cx - 0.48 * r, cy + 0.75 * r)]
    b += path(smooth(outline, k=0.7), "ln")
    b += line((cx - 0.3 * r, cy + 1.2 * r), (cx - 0.35 * r, cy + 1.9 * r), "ln")
    b += line((cx + 0.45 * r, cy + 1.35 * r), (cx + 0.4 * r, cy + 1.9 * r), "ln")
    # Merkmale 3/4
    ey = cy + 0.2 * r
    b += path(f"M{f(cx-0.15*r)},{f(ey)} q{f(0.17*r)},{f(-0.13*r)} {f(0.38*r)},{f(0.01*r)} q{-0.2*r:.1f},{0.09*r:.1f} {-0.38*r:.1f},{-0.01*r:.1f}", "ln")
    b += path(f"M{f(cx+0.55*r)},{f(ey)} q{f(0.1*r)},{f(-0.1*r)} {f(0.24*r)},{f(0.0)} q{-0.12*r:.1f},{0.07*r:.1f} {-0.24*r:.1f},{0.0:.1f}", "ln")
    b += path(f"M{f(cx+0.47*r)},{f(cy+0.1*r)} L{f(cx+0.68*r)},{f(cy+0.66*r)} L{f(cx+0.45*r)},{f(cy+0.7*r)}", "ln")
    b += path(f"M{f(cx+0.15*r)},{f(cy+0.95*r)} Q{f(cx+0.4*r)},{f(cy+0.9*r)} {f(cx+0.65*r)},{f(cy+0.96*r)}", "ln")
    b += path(f"M{f(cx-0.52*r)},{f(cy+0.02*r)} c{-0.14*r:.1f},{0.0:.1f} {-0.16*r:.1f},{0.6*r:.1f} {0.0:.1f},{0.66*r:.1f}", "ln")
    b += text(cx, 250, "3/4-Ansicht", "labb", "middle")
    # Profil
    b += head_side(470, 90, r * 0.95, construct=True, finished=True)
    b += text(480, 250, "Profil", "labb", "middle")
    return svg(580, 262, b)


def head_guides(n=6, cols=3, w=560, h=640):
    """Übungsblatt mit vorgegebenen Kugeln (zum Ausarbeiten)."""
    b = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" class="frame"/>'
    rows = math.ceil(n / cols)
    cw, ch = w / cols, h / rows
    for i in range(n):
        cx = cw * (i % cols) + cw / 2
        cy = ch * (i // cols) + ch * 0.38
        b += circ(cx, cy, min(cw, ch) * 0.22, "cn")
    return svg(w, h, b)


# ---------------------------------------------------------------- Figuren

def dvec(a):
    r = math.radians(a)
    return (math.sin(r), math.cos(r))


def add(p, v, s=1):
    return (p[0] + v[0] * s, p[1] + v[1] * s)


def capsule(a, b, w, out=""):
    return (f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" class="capo" stroke-width="{f(w)}"/>',
            f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" class="capi" stroke-width="{f(w-2.6)}"/>')


def figure(px, py, H, torso=180, neck=180, la=(10, 5), ra=(-10, -5), ll=(4, 0), rl=(-4, 0),
           lfoot=-80, rfoot=80, style="mannequin", rot_sh=0, rot_hip=0):
    """Gliederpuppe. Winkel in Grad, 0 = nach unten, 90 = nach rechts, 180 = nach oben."""
    P = (px, py)
    t = dvec(torso)
    N = add(P, t, 2.5 * H)
    perp_s = dvec(torso - 90 + rot_sh)
    perp_h = dvec(torso - 90 + rot_hip)
    hd = add(N, dvec(neck), 0.62 * H)
    shL = add(add(N, t, -0.15 * H), perp_s, -0.95 * H)
    shR = add(add(N, t, -0.15 * H), perp_s, 0.95 * H)
    hpL = add(add(P, t, -0.1 * H), perp_h, -0.5 * H)
    hpR = add(add(P, t, -0.1 * H), perp_h, 0.5 * H)

    def limb(start, a1, a2, l1, l2):
        j = add(start, dvec(a1), l1 * H)
        e = add(j, dvec(a2), l2 * H)
        return j, e
    elL, waL = limb(shL, la[0], la[1], 1.45, 1.25)
    elR, waR = limb(shR, ra[0], ra[1], 1.45, 1.25)
    knL, anL = limb(hpL, ll[0], ll[1], 2.0, 1.85)
    knR, anR = limb(hpR, rl[0], rl[1], 2.0, 1.85)
    if style == "stick":
        o = ""
        o += line(P, N, "ln") + line(N, hd, "ln") + line(shL, shR, "ln") + line(hpL, hpR, "ln")
        for a, b_ in ((shL, elL), (elL, waL), (shR, elR), (elR, waR), (hpL, knL), (knL, anL), (hpR, knR), (knR, anR)):
            o += line(a, b_, "ln")
        o += ell(hd[0], hd[1], 0.38 * H, 0.5 * H, "ln", rot=-(neck - 180))
        for j in (elL, elR, knL, knR, shL, shR, hpL, hpR):
            o += circ(j[0], j[1], 2.2, "dot")
        return o
    outer, inner = [], []
    w = 0.44 * H

    def seg(a, b_, ww):
        c1, c2 = capsule(a, b_, ww)
        outer.append(c1); inner.append(c2)
    # Hinten nach vorne: Beine, Becken, Rumpf, Arme
    for a, b_, ww in ((hpL, knL, w * 1.25), (knL, anL, w), (hpR, knR, w * 1.25), (knR, anR, w)):
        seg(a, b_, ww)
    o = "".join(outer) + "".join(inner)
    outer, inner = [], []
    for an, fa in ((anL, lfoot), (anR, rfoot)):
        ft = add(an, dvec(fa), 0.75 * H)
        seg(an, ft, w * 0.75)
    o += "".join(outer) + "".join(inner)
    # Rumpf
    ang = -(torso - 180)
    rc = add(N, t, -0.85 * H)
    pc = add(P, t, 0.05 * H)
    o += line(P, N, "cs")
    o += line(N, hd, "capo", ) .replace('class="capo"', f'class="capo" stroke-width="{f(w*0.9)}"')
    o += line(N, hd, "capi").replace('class="capi"', f'class="capi" stroke-width="{f(w*0.9-2.6)}"')
    o += ell(pc[0], pc[1], 0.62 * H, 0.45 * H, "fig", rot=ang)
    o += ell(rc[0], rc[1], 0.78 * H, 0.95 * H, "fig", rot=ang)
    o += line(P, add(P, t, 0.9 * H), "lt")
    o += ell(hd[0], hd[1], 0.38 * H, 0.5 * H, "fig", rot=-(neck - 180))
    outer, inner = [], []
    for a, b_ in ((shL, elL), (elL, waL), (shR, elR), (elR, waR)):
        seg(a, b_, w * 0.95)
    o += "".join(outer) + "".join(inner)
    for j in (elL, elR, knL, knR, shL, shR):
        o += circ(j[0], j[1], w * 0.45, "fig")
    for wa, el in ((waL, elL), (waR, elR)):
        v = (wa[0] - el[0], wa[1] - el[1])
        L = math.hypot(*v) or 1
        hc = (wa[0] + v[0] / L * 0.3 * H, wa[1] + v[1] / L * 0.3 * H)
        o += ell(hc[0], hc[1], 0.18 * H, 0.34 * H, "fig", rot=-math.degrees(math.atan2(v[0], v[1])))
    return o


def proportions_8():
    H = 40
    top = 18
    px = 170
    py = top + 3.75 * H
    b = ""
    for i in range(9):
        y = top + i * H
        b += line((40, y), (330, y), "cn")
        b += text(32, y + 4, str(i), "labs", "end")
    b += figure(px, py, H, la=(8, 4), ra=(-8, -4), ll=(3, 1), rl=(-3, -1), lfoot=-60, rfoot=60)
    notes = [(1, "Kinn"), (2, "Brustwarzen"), (3, "Bauchnabel"), (4, "Schritt (Körpermitte!)"),
             (5, "Fingerspitzen ≈ Mitte Oberschenkel"), (6, "unter dem Knie"), (7, "Mitte Schienbein"), (8, "Fußsohle")]
    for k, s in notes:
        b += text(340, top + k * H + 4, s, "lab")
    b += text(340, top + 1.5 * H + 4, "Schulterbreite ≈ 2 Köpfe", "labs")
    return svg(540, top * 2 + 8 * H + 6, b)


def mannequin_steps():
    H = 26
    b = ""
    y0 = 30 + 3.75 * H
    b += figure(75, y0, H, style="stick", torso=176, neck=184, la=(-12, -4), ra=(35, 75), ll=(-6, -2), rl=(14, 2), lfoot=-80, rfoot=70, rot_sh=-6, rot_hip=6)
    b += path(smooth([(75 - 12, y0 + 3.9 * H), (75, y0), (75 + 4, y0 - 3.2 * H)], k=0.6), "loa")
    b += text(75, 26 + 8.6 * H, "1. Strichmännchen +", "labs", "middle") + text(75, 26 + 8.6 * H + 12, "Bewegungslinie", "labs", "middle")
    b += figure(265, y0, H, torso=176, neck=184, la=(-12, -4), ra=(35, 75), ll=(-6, -2), rl=(14, 2), lfoot=-80, rfoot=70, rot_sh=-6, rot_hip=6)
    b += text(265, 26 + 8.6 * H, "2. Körper als Formen:", "labs", "middle") + text(265, 26 + 8.6 * H + 12, "Brustkorb, Becken, Röhren", "labs", "middle")
    # Schritt 3: Konturen andeuten
    fig = figure(440, y0, H, torso=176, neck=184, la=(-12, -4), ra=(35, 75), ll=(-6, -2), rl=(14, 2), lfoot=-80, rfoot=70, rot_sh=-6, rot_hip=6)
    b += f'<g opacity="0.35">{fig}</g>'
    b += f'<g>{figure(440, y0, H, torso=176, neck=184, la=(-12, -4), ra=(35, 75), ll=(-6, -2), rl=(14, 2), lfoot=-80, rfoot=70, rot_sh=-6, rot_hip=6, style="stick")}</g>'
    b += text(440, 26 + 8.6 * H, "3. Muskeln/Kleidung drüber,", "labs", "middle") + text(440, 26 + 8.6 * H + 12, "Hilfslinien radieren", "labs", "middle")
    return svg(560, 26 + 8.6 * H + 20, b)


def gestures():
    H = 18
    b = ""
    poses = [
        dict(torso=160, neck=150, la=(-140, -150), ra=(150, 140), ll=(40, 10), rl=(-35, -10)),   # Strecken
        dict(torso=205, neck=200, la=(-30, 20), ra=(60, 110), ll=(-45, 30), rl=(30, -10), lfoot=-100, rfoot=100),  # Laufen
        dict(torso=145, neck=135, la=(100, 60), ra=(80, 30), ll=(-60, 10), rl=(40, 0), lfoot=80, rfoot=80),  # Bücken
        dict(torso=190, neck=170, la=(-160, -170), ra=(-150, 160), ll=(10, 0), rl=(-30, 0)),  # Jubeln
        dict(torso=170, neck=180, la=(30, -60), ra=(-30, 60), ll=(70, 0), rl=(-70, 0)),  # breitbeinig
    ]
    loas = [
        [(-8, 4.3), (0, 0), (18, -2.9)],
        [(-10, 4.0), (0, 0), (10, -3)],
        [(10, 3.8), (0, 0), (-60, -1.5)],
        [(-12, 3.7), (0, 0), (-8, -3.3)],
        [(0, 3.9), (0, 0), (5, -3.2)],
    ]
    for i, (p, lo) in enumerate(zip(poses, loas)):
        x = 55 + i * 110
        y = 20 + 4.1 * H
        b += path(smooth([(x + a, y + c * H) for a, c in lo], k=0.6), "loa")
        b += figure(x, y, H, style="stick", **p)
    b += text(270, 20 + 8.9 * H, "graue Linie = Bewegungslinie (Line of Action): immer zuerst zeichnen!", "labs", "middle")
    return svg(560, 20 + 9.3 * H, b)


def hand():
    b = ""
    x0, y0 = 120, 120
    # Handfläche
    b += path(f"M{x0},{y0} L{x0+70},{y0+4} L{x0+64},{y0+78} Q{x0+35},{y0+92} {x0+6},{y0+76} Z", "cn")
    b += path(f"M{x0-4},{y0} Q{x0+35},{y0-14} {x0+72},{y0+6}", "cn")
    fingers = [(x0 + 7, y0 - 3, 56, -8), (x0 + 26, y0 - 8, 64, -2), (x0 + 45, y0 - 7, 59, 4), (x0 + 63, y0 - 1, 45, 11)]
    outer, inner, joints = "", "", ""
    for fx, fy, L, ang in fingers:
        d = dvec(180 + ang)
        a = (fx, fy)
        p1 = add(a, d, L * 0.45)
        p2 = add(p1, d, L * 0.30)
        p3 = add(p2, d, L * 0.25)
        for s, e, w in ((a, p1, 17), (p1, p2, 15.5), (p2, p3, 14)):
            c1, c2 = capsule(s, e, w)
            outer += c1; inner += c2
        for j in (p1, p2):
            joints += line(add(j, (1, 0), -5.5), add(j, (1, 0), 5.5), "lt")
    # Daumen
    th = [(x0 + 10, y0 + 55), (x0 - 18, y0 + 32), (x0 - 36, y0 + 12), (x0 - 48, y0 - 4)]
    for s, e, w in ((th[0], th[1], 22), (th[1], th[2], 17), (th[2], th[3], 15)):
        c1, c2 = capsule(s, e, w)
        outer += c1; inner += c2
    b += outer
    b += path(f"M{x0-2},{y0} L{x0+72},{y0+4} L{x0+66},{y0+76} Q{x0+35},{y0+94} {x0+4},{y0+78} Z", "capo2")
    b += inner
    b += path(f"M{x0},{y0+2} L{x0+70},{y0+6} L{x0+64},{y0+76} Q{x0+35},{y0+92} {x0+6},{y0+76} Z", "capi2")
    b += joints
    b += path(f"M{x0+12},{y0+60} Q{x0+28},{y0+30} {x0+62},{y0+22}", "lt")
    b += path(smooth([(x0 + 4, y0 - 52), (x0 + 30, y0 - 74), (x0 + 50, y0 - 67), (x0 + 72, y0 - 44)], k=0.7), "cn")
    b += text(x0 + 140, y0 - 50, "Fingerspitzen liegen", "labs") + text(x0 + 140, y0 - 38, "auf einem Bogen", "labs")
    b += text(x0 + 140, y0 + 5, "Knöchel ebenfalls Bogen", "labs")
    b += text(x0 + 140, y0 + 50, "Handfläche = Kästchen", "labs")
    b += text(x0 + 140, y0 + 62, "Finger = 3 Glieder", "labs")
    b += text(x0 + 140, y0 + 74, "Mittelfinger ≈ Länge Handfläche", "labs")
    b += text(x0 - 75, y0 + 60, "Daumen setzt", "labs") + text(x0 - 75, y0 + 72, "tief an!", "labs")
    # Fuß seitlich
    fx, fy = 470, 170
    b += poly([(fx, fy - 90), (fx + 22, fy - 90), (fx + 34, fy - 28), (fx + 120, fy - 6), (fx + 124, fy + 8), (fx - 6, fy + 8), (fx - 12, fy - 10)], "cn")
    b += path(smooth([(fx + 2, fy - 90), (fx + 2, fy - 40), (fx - 12, fy - 10), (fx - 8, fy + 6), (fx + 40, fy + 8),
                      (fx + 90, fy + 6), (fx + 124, fy + 4), (fx + 118, fy - 8), (fx + 80, fy - 20), (fx + 38, fy - 40),
                      (fx + 22, fy - 90)], k=0.6), "ln")
    b += circ(fx + 10, fy - 26, 7, "lt")
    b += text(fx + 60, fy + 30, "Fuß: Keil, Knöchel innen höher", "labs", "middle")
    return svg(610, 210, b)


# ---------------------------------------------------------------- Autos

def car_side(step):
    r = 18
    D = 2 * r
    g = 110
    L = 7 * D
    x0 = 60
    hgt = 2 * D
    wf, wr = x0 + 1.4 * D, x0 + 1.4 * D + 4.2 * D
    b = line((20, g), (380, g), "cs")
    if step >= 1:
        cls = "cn" if step > 1 else "ln"
        b += f'<rect x="{x0}" y="{g-hgt}" width="{L}" height="{hgt}" class="{cls}"/>'
        b += circ(wf, g - r, r, "cn" if step > 1 else "ln") + circ(wr, g - r, r, "cn" if step > 1 else "ln")
        if step == 1:
            for i in range(7):
                b += f'<rect x="{x0+i*D}" y="{g-hgt-14}" width="{D}" height="6" class="lt" style="fill:{"#000" if i%2 else "#fff"}"/>'
            b += text(x0 + L / 2, g - hgt - 20, "Länge ≈ 7 Räder · Höhe ≈ 2 Räder · Radstand ≈ 4 Räder", "labs", "middle")
    sill = g - 0.24 * hgt

    def X(t): return x0 + t * L

    def Y(t): return g - t * hgt
    if step >= 2:
        ar = 1.25 * r
        cy = g - r
        dy = cy - sill
        dx = math.sqrt(ar * ar - dy * dy) if ar > abs(dy) else ar
        d = (f"M{f(X(0.0))},{f(sill)} L{f(X(0.0))},{f(Y(0.48))} Q{f(X(0.01))},{f(Y(0.58))} {f(X(0.06))},{f(Y(0.6))} "
             f"L{f(X(0.31))},{f(Y(0.66))} Q{f(X(0.4))},{f(Y(0.97))} {f(X(0.47))},{f(Y(1.0))} "
             f"L{f(X(0.7))},{f(Y(0.99))} Q{f(X(0.8))},{f(Y(0.96))} {f(X(0.88))},{f(Y(0.68))} "
             f"L{f(X(0.98))},{f(Y(0.64))} Q{f(X(1.0))},{f(Y(0.6))} {f(X(1.0))},{f(Y(0.5))} L{f(X(1.0))},{f(sill)} "
             f"L{f(wr+dx)},{f(sill)} A{f(ar)},{f(ar)} 0 0 0 {f(wr-dx)},{f(sill)} "
             f"L{f(wf+dx)},{f(sill)} A{f(ar)},{f(ar)} 0 0 0 {f(wf-dx)},{f(sill)} Z")
        b += path(d, "ln")
        b += circ(wf, g - r, r, "ln") + circ(wr, g - r, r, "ln")
    if step >= 3:
        b += circ(wf, g - r, r * 0.6, "lt") + circ(wr, g - r, r * 0.6, "lt")
        b += circ(wf, g - r, 3, "dot") + circ(wr, g - r, 3, "dot")
        win = (f"M{f(X(0.37))},{f(Y(0.68))} Q{f(X(0.43))},{f(Y(0.92))} {f(X(0.48))},{f(Y(0.93))} L{f(X(0.69))},{f(Y(0.92))} "
               f"Q{f(X(0.77))},{f(Y(0.89))} {f(X(0.83))},{f(Y(0.68))} Z")
        b += path(win, "ln", 'style="fill:#d6d6d6"')
        b += line((X(0.6), Y(0.93)), (X(0.6), Y(0.68)), "ln")
        b += line((X(0.38), Y(0.66)), (X(0.38), sill + 1), "lt") + line((X(0.6), Y(0.68)), (X(0.6), sill + 1), "lt")
        b += line((X(0.82), Y(0.66)), (X(0.84), Y(0.40)), "lt")
        b += line((X(0.03), Y(0.42)), (X(0.97), Y(0.44)), "lt")
        b += path(f"M{f(X(0.005))},{f(Y(0.5))} L{f(X(0.05))},{f(Y(0.55))} L{f(X(0.05))},{f(Y(0.47))} Z", "ln", 'style="fill:#fff"')
        b += f'<rect x="{f(X(0.965))}" y="{f(Y(0.6))}" width="{f(0.03*L)}" height="{f(0.1*hgt)}" class="ln" style="fill:#555"/>'
        b += line((X(0.45), Y(0.55)), (X(0.49), Y(0.55)), "ln") + line((X(0.66), Y(0.55)), (X(0.7), Y(0.55)), "ln")
        b += ell((wf + wr) / 2, g + 2, L * 0.48, 4, "none", extra='style="fill:#000" opacity="0.6"')
    return svg(400, 125, b)


def car_34():
    W, H = 540, 300
    hy = 95
    vl, vr = (-420, hy), (1100, hy)
    b = line((0, hy), (W, hy), "cs") + text(6, hy - 6, "Horizont (Augenhöhe)", "labs")
    k = two_pt_box(vl, vr, (200, 262), 80, 0.14, 0.30)
    for p in ("T", "P", "TR", "R"):
        b += line(k[p], lerp(k[p], vl, 0.3), "cn")
    for p in ("T", "P", "TL", "L"):
        b += line(k[p], lerp(k[p], vr, 0.62), "cn")
    b += draw_box(k, vl, vr, guides=False)
    q = lerp(k["T"], k["TR"], 0.3)
    q = lerp(q, vl, 0.02)
    kc = two_pt_box(vl, vr, q, 48, 0.08, 0.14)
    b += draw_box(kc, vl, vr, guides=False, hidden=True)
    r = 26
    for t in (0.17, 0.80):
        c = lerp(k["P"], k["R"], t)
        c = (c[0], c[1] - r * 0.9)
        ax = math.degrees(math.atan2(vl[1] - c[1], vl[0] - c[0]))
        b += ell(c[0], c[1], r * 0.45, r, "ln", rot=ax)
        b += ell(c[0], c[1], r * 0.45 * 0.55, r * 0.55, "lt", rot=ax)
        b += line(c, lerp(c, vl, 0.06), "cn")
    b += text(270, 292, "Radachsen (kurze Ellipsen-Achse) zeigen zum linken Fluchtpunkt", "labs", "middle")
    b += text(534, 60, "beide Fluchtpunkte liegen weit außerhalb", "labs", "end")
    b += text(534, 72, "des Bildes → wirkt natürlich, nicht verzerrt", "labs", "end")
    return svg(W, H, b)


# ---------------------------------------------------------------- Tiere & Natur

def dog():
    b = ""
    b += circ(150, 110, 40, "cs") + circ(262, 115, 30, "cs") + circ(82, 72, 23, "cs")
    b += poly([(62, 68), (36, 78), (40, 92), (66, 90)], "cn")
    b += line((150, 70), (262, 85), "cn") + line((150, 150), (262, 145), "cn")
    joints = [(142, 140), (148, 172), (146, 202), (160, 210)]
    joints2 = [(270, 135), (290, 165), (266, 186), (272, 210), (286, 211)]
    b += poly(joints, "ln", False) + poly(joints2, "ln", False)
    for p in joints[:-1] + joints2[:-1]:
        b += circ(p[0], p[1], 3, "dot")
    outline = [(104, 62), (125, 72), (175, 74), (240, 84), (282, 96), (290, 118), (288, 140), (278, 160),
               (290, 168), (276, 184), (278, 206), (292, 212), (266, 213), (258, 186), (276, 166), (258, 148),
               (215, 150), (170, 154), (158, 176), (156, 204), (166, 212), (142, 212), (138, 176), (128, 150),
               (112, 132), (100, 100), (90, 95), (72, 96), (44, 93), (36, 80), (58, 64), (70, 50), (90, 48)]
    b += path(smooth(outline, closed=True, k=0.6), "ln")
    b += poly([(70, 52), (78, 34), (90, 50)], "ln")
    b += circ(72, 70, 2.6, "dot") + circ(38, 80, 3.5, "dot")
    b += path(smooth([(288, 104), (306, 86), (316, 62)], k=0.7), "ln")
    b += text(180, 240, "Brustkorb groß, Becken kleiner, Kopf + Schnauze als Kasten.", "labs", "middle")
    b += text(180, 252, "Hinterbein knickt wie ein Z – das Fersengelenk zeigt nach hinten!", "labs", "middle")
    # Vogel
    bx, by = 440, 120
    b += ell(bx, by, 50, 32, "cs", rot=-20) + circ(bx + 46, by - 40, 18, "cs")
    pts = [(bx + 30, by - 50), (bx + 50, by - 58), (bx + 64, by - 44), (bx + 60, by - 26), (bx + 40, by + 10),
           (bx + 10, by + 28), (bx - 30, by + 22), (bx - 60, by + 40), (bx - 70, by + 36), (bx - 48, by + 6),
           (bx - 20, by - 22), (bx + 20, by - 34)]
    b += path(smooth(pts, closed=True, k=0.7), "ln")
    b += poly([(bx + 62, by - 46), (bx + 80, by - 40), (bx + 63, by - 36)], "ln")
    b += circ(bx + 50, by - 44, 2.6, "dot")
    b += path(smooth([(bx - 30, by - 10), (bx + 10, by - 6), (bx + 30, by + 8), (bx - 40, by + 20)], k=0.7), "lt")
    b += poly([(bx, by + 26), (bx - 4, by + 55), (bx + 6, by + 55)], "ln", False)
    b += poly([(bx + 14, by + 24), (bx + 14, by + 55), (bx + 22, by + 55)], "ln", False)
    b += text(bx, 240, "Vogel: Ei + Kreis", "labs", "middle")
    return svg(540, 260, b)


def tree_and_landscape():
    b = ""
    # Baum: Blob-Methode
    circles = [(110, 70, 38), (70, 95, 32), (150, 95, 34), (95, 125, 30), (135, 128, 30), (110, 42, 26), (60, 128, 22), (165, 130, 22)]
    b += line((105, 210), (105, 120), "ln") + line((118, 210), (118, 120), "ln")
    b += path("M106,150 L80,118 M117,145 L145,115", "ln")
    for x, y, r in circles:
        b += circ(x, y, r + 1.3, "none", 'style="fill:#000"')
    for x, y, r in circles:
        b += circ(x, y, r, "none", 'style="fill:#bbb"')
    cid = uid("clip")
    b += f'<clipPath id="{cid}">' + "".join(circ(x, y, r, "none") for x, y, r in circles) + "</clipPath>"
    b += f'<g clip-path="url(#{cid})">'
    for x, y, r in circles:
        b += circ(x - 6, y - 7, r * 0.78, "none", 'style="fill:#fff"')
    b += "</g>"
    b += path("M96,210 Q111,203 128,210", "ln")
    b += text(112, 236, "Baum: erst Laubmassen, dann Licht/Schatten", "labs", "middle")
    b += text(112, 248, "– keine einzelnen Blätter!", "labs", "middle")
    # Landschaft
    x0, y0, w, h = 260, 20, 270, 190
    cid = uid("clip")
    b += f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">'
    b += f'<polygon points="{x0},{y0+110} {x0+50},{y0+60} {x0+90},{y0+85} {x0+150},{y0+40} {x0+210},{y0+90} {x0+w},{y0+70} {x0+w},{y0+h} {x0},{y0+h}" style="fill:#e2e2e2"/>'
    b += f'<path d="M{x0},{y0+130} Q{x0+70},{y0+95} {x0+140},{y0+120} T{x0+w},{y0+115} L{x0+w},{y0+h} L{x0},{y0+h}Z" style="fill:#9a9a9a"/>'
    b += f'<path d="M{x0},{y0+165} Q{x0+100},{y0+140} {x0+w},{y0+170} L{x0+w},{y0+h} L{x0},{y0+h}Z" style="fill:#333"/>'
    b += f'<rect x="{x0+40}" y="{y0+90}" width="5" height="70" style="fill:#222"/>' + circ(x0 + 42, y0 + 90, 24, "none", 'style="fill:#222"')
    b += "</g>" + f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="ln"/>'
    b += text(x0 + w - 4, y0 + 58, "hinten: hell, wenig Kontrast", "labs", "end")
    b += f'<text x="{x0+w-4}" y="{y0+150}" class="labs" text-anchor="end">Mitte: Mittelgrau</text>'
    b += f'<text x="{x0+w-4}" y="{y0+184}" class="labs" text-anchor="end" style="fill:#fff">vorne: dunkel, Details</text>'
    b += text(x0 + w / 2, 236, "Landschaft in 3 Ebenen (Luftperspektive)", "labs", "middle")
    return svg(540, 255, b)


def still_life():
    b = ""
    # Tasse
    cx = 90
    b += ell(cx, 60, 50, 14, "ln") + ell(cx, 60, 44, 11, "lt")
    b += path(f"M{cx-50},60 L{cx-44},160 A44,14 0 0 0 {cx+44},160 L{cx+50},60", "ln")
    b += path(f"M{cx-44},160 A44,14 0 0 1 {cx+44},160", "hid")
    b += line((cx, 40), (cx, 185), "cn")
    b += path(f"M{cx+49},80 C{cx+88},76 {cx+90},140 {cx+45},140", "ln") + path(f"M{cx+48},92 C{cx+74},90 {cx+74},128 {cx+46},127", "ln")
    b += hatch(cx + 10, 60, 44, 110, -70, 4, "hat", f'<path d="M{cx+18},70 L{cx+50},62 L{cx+44},160 L{cx+22},172 Z"/>')
    b += text(cx, 205, "Tasse = Zylinder", "labs", "middle")
    # Flasche
    cx = 260
    right = [(0, 20), (9, 20), (9, 60), (20, 85), (30, 105), (30, 185)]
    left = [(-x, y) for x, y in reversed(right)]
    pts = [(cx + x, y) for x, y in right + left]
    b += line((cx, 10), (cx, 195), "cn")
    for y in (20, 60, 105, 185):
        b += line((cx - 40, y), (cx + 40, y), "cn")
    b += poly(pts, "ln")
    b += ell(cx, 185, 30, 6, "lt") + ell(cx, 20, 9, 3, "ln")
    b += line((cx + 18, 112), (cx + 18, 175), "lt") + line((cx + 22, 112), (cx + 22, 175), "lt")
    b += text(cx, 205, "Flasche: Mittellinie, spiegeln", "labs", "middle")
    # Lampe = zerlegen
    cx = 430
    b += ell(cx, 180, 42, 10, "ln") + line((cx - 42, 180), (cx - 42, 170), "ln") + line((cx + 42, 180), (cx + 42, 170), "ln")
    b += path(f"M{cx-42},170 A42,10 0 0 1 {cx+42},170", "ln")
    b += line((cx - 3, 164), (cx - 3, 80), "ln") + line((cx + 3, 164), (cx + 3, 80), "ln")
    b += path(f"M{cx-60},90 L{cx-28},30 L{cx+28},30 L{cx+60},90", "ln") + ell(cx, 90, 60, 13, "ln") + ell(cx, 30, 28, 6, "ln")
    b += text(cx, 205, "Lampe: Zylinder + Stab + Kegelstumpf", "labs", "middle")
    return svg(540, 215, b)


# ---------------------------------------------------------------- Rotation

def cube3d(cx, cy, s, rx, ry, rz, guides=False):
    V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]

    def rot(p):
        x, y, z = p
        a = math.radians(rx); c, s_ = math.cos(a), math.sin(a)
        y, z = y * c - z * s_, y * s_ + z * c
        a = math.radians(ry); c, s_ = math.cos(a), math.sin(a)
        x, z = x * c + z * s_, -x * s_ + z * c
        a = math.radians(rz); c, s_ = math.cos(a), math.sin(a)
        x, y = x * c - y * s_, x * s_ + y * c
        return x, y, z
    R = [rot(v) for v in V]
    dcam = 6

    def proj(p):
        k = dcam / (dcam - p[2])
        return (cx + p[0] * s * k, cy - p[1] * s * k)
    Pp = [proj(p) for p in R]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    edges_vis = set()
    for fc in faces:
        a, b_, c = (R[i] for i in fc[:3])
        u = [b_[i] - a[i] for i in range(3)]
        v = [c[i] - a[i] for i in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        cen = [sum(R[i][k] for i in fc) / 4 for k in range(3)]
        view = (0 - cen[0], 0 - cen[1], dcam - cen[2])
        if n[0] * view[0] + n[1] * view[1] + n[2] * view[2] > 0:
            for i in range(4):
                e = tuple(sorted((fc[i], fc[(i + 1) % 4])))
                edges_vis.add(e)
    out = ""
    all_edges = set()
    for fc in faces:
        for i in range(4):
            all_edges.add(tuple(sorted((fc[i], fc[(i + 1) % 4]))))
    for e in all_edges:
        out += line(Pp[e[0]], Pp[e[1]], "ln" if e in edges_vis else "hid")
    return out


def cube_rotations():
    b = ""
    rots = [(20, 30, 0), (35, -40, 0), (-25, 20, 0), (60, 45, 10), (10, 70, -20), (-40, -30, 15)]
    for i, (a, c, d) in enumerate(rots):
        b += cube3d(50 + i * 90, 60, 26, a, c, d)
    return svg(560, 115, b)


def frames(n, cols, w=560, h=300, labels=None, guide=None, seed=1):
    b = ""
    rows = math.ceil(n / cols)
    gap = 12
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i in range(n):
        x = (i % cols) * (cw + gap)
        y = (i // cols) * (ch + gap)
        b += f'<rect x="{f(x+1)}" y="{f(y+1)}" width="{f(cw-2)}" height="{f(ch-2)}" class="frame"/>'
        if labels:
            b += text(x + 8, y + 15, labels[i % len(labels)], "labs")
        if guide == "cross":
            b += line((x + cw / 2 - 6, y + ch / 2), (x + cw / 2 + 6, y + ch / 2), "lt")
            b += line((x + cw / 2, y + ch / 2 - 6), (x + cw / 2, y + ch / 2 + 6), "lt")
        elif guide == "circle":
            b += circ(x + cw / 2, y + ch * 0.42, min(cw, ch) * 0.24, "cn")
        elif guide == "horizon":
            b += line((x + 2, y + ch * 0.35), (x + cw - 2, y + ch * 0.35), "cn")
        elif guide == "ground":
            b += line((x + 10, y + ch * 0.8), (x + cw - 10, y + ch * 0.8), "cn")
        elif guide == "cube":
            if i % 2 == 0:
                b += f'<g>{cube3d(x + cw/2, y + ch/2, min(cw, ch)*0.18, 20 + i*8, 30 - i*17, i*3)}</g>'
    return svg(w, h, b)


def cover_art():
    b = ""
    gid = uid("rg")
    b += (f'<defs><radialGradient id="{gid}" cx="0.35" cy="0.33" r="0.75"><stop offset="0" stop-color="#fff"/>'
          f'<stop offset="0.5" stop-color="#bbb"/><stop offset="0.8" stop-color="#333"/><stop offset="1" stop-color="#777"/></radialGradient></defs>')
    b += ell(140, 300, 95, 16, "none", 'style="fill:#000" opacity="0.5"')
    b += circ(110, 245, 58, "lt", f'style="fill:url(#{gid})"')
    vl, vr = (-300, 160), (900, 160)
    k = two_pt_box(vl, vr, (300, 320), 110, 0.17, 0.17)
    b += draw_box(k, vl, vr, guides=False)
    b += hatch(0, 0, 500, 400, -60, 5, "hat", f'<polygon points="{k["P"][0]},{k["P"][1]} {k["R"][0]},{k["R"][1]} {k["TR"][0]},{k["TR"][1]} {k["T"][0]},{k["T"][1]}"/>')
    b += f'<g transform="translate(330 -20) scale(0.9)">{head_front(120, 120, 72, construct=True, finished=True)}</g>'
    return svg(500, 340, b)
