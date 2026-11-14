"""Erzeugt skizzenbuch.html (A4, Ringordner-Rand links). PDF: node render.js"""
import os
import svgs as S

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; color: #000; }
body { font-family: 'Inter', 'DejaVu Sans', sans-serif; font-size: 10pt; line-height: 1.42; }
.page { width: 210mm; height: 297mm; padding: 14mm 14mm 16mm 27mm; position: relative;
        overflow: hidden; page-break-after: always; break-after: page; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
.foot { position: absolute; left: 27mm; right: 14mm; bottom: 8mm; display: flex; justify-content: space-between;
        font-size: 7.5pt; color: #555; border-top: 0.3mm solid #000; padding-top: 1.5mm; }
.kicker { font-size: 8pt; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; margin-bottom: 1mm; }
h1 { font-family: 'Inter Display', 'Inter', sans-serif; font-size: 22pt; line-height: 1.1; margin: 0 0 3mm; font-weight: 800; }
h2 { font-size: 12pt; margin: 4mm 0 1.5mm; font-weight: 700; }
p { margin: 0 0 2.2mm; }
.lead { font-size: 10.5pt; }
.ill { width: 100%; height: auto; display: block; margin: 2mm 0; }
.grow { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.grow .ill { flex: 1; height: 100%; min-height: 0; margin: 0; }
.row { display: flex; gap: 5mm; }
.row > * { flex: 1; min-width: 0; }
.box { border: 0.35mm solid #000; padding: 2.5mm 3.5mm; margin: 2mm 0; border-radius: 1.5mm; }
.box b.t { display: block; font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 1mm; }
.mat { background: #f0f0f0; border-color: #f0f0f0; }
.ex { border-width: 0.6mm; }
.err { border-style: dashed; }
ol, ul { margin: 0 0 1mm; padding-left: 5mm; }
li { margin: 0 0 1mm; }
.small { font-size: 8.5pt; }
.timer { font-weight: 700; }
.chk { display: inline-block; width: 3.6mm; height: 3.6mm; border: 0.3mm solid #000; vertical-align: -0.6mm; margin-right: 1.5mm; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; }
td, th { border: 0.3mm solid #000; padding: 1.6mm 2mm; text-align: left; vertical-align: top; }
th { background: #e8e8e8; }
.toc td { border: none; border-bottom: 0.2mm dotted #777; padding: 1.4mm 0; }
.plan td, .plan th { padding: 0.9mm 2mm; }
.toc td:last-child { text-align: right; width: 14mm; }
.section { justify-content: center; }
.section .num { font-family: 'Inter Display', sans-serif; font-size: 90pt; font-weight: 900; line-height: 1; }
.section h1 { font-size: 34pt; }
.blankfoot { position: absolute; left: 27mm; right: 14mm; bottom: 8mm; font-size: 7.5pt; color: #777;
             display: flex; justify-content: space-between; }
/* SVG */
.ln { stroke: #000; stroke-width: 1.6; fill: none; stroke-linecap: round; stroke-linejoin: round; }
.lt { stroke: #000; stroke-width: 0.9; fill: none; stroke-linecap: round; }
.cn { stroke: #8c8c8c; stroke-width: 0.9; fill: none; stroke-dasharray: 4 3; }
.cs { stroke: #9a9a9a; stroke-width: 0.9; fill: none; }
.hid { stroke: #000; stroke-width: 0.9; fill: none; stroke-dasharray: 3 3; }
.hat { stroke: #000; stroke-width: 0.7; }
.lead { stroke: #000; stroke-width: 0.6; }
.loa { stroke: #b5b5b5; stroke-width: 7; fill: none; stroke-linecap: round; }
.frame { stroke: #000; stroke-width: 0.8; fill: none; }
.dot { fill: #000; stroke: none; }
.fillk { fill: #000; stroke: none; }
.none { stroke: none; }
.capo { stroke: #000; stroke-linecap: round; }
.capi { stroke: #fff; stroke-linecap: round; }
.capo2 { stroke: #000; stroke-width: 2.6; fill: #fff; stroke-linejoin: round; }
.capi2 { stroke: none; fill: #fff; }
.fig { stroke: #000; stroke-width: 1.3; fill: #fff; }
.lab { font: 11px 'Inter', sans-serif; fill: #000; }
.labs { font: 9.5px 'Inter', sans-serif; fill: #000; }
.labb { font: 600 10.5px 'Inter', sans-serif; fill: #000; }
"""

pages = []
state = {"n": 0}


def page(body, section="", cls=""):
    state["n"] += 1
    n = state["n"]
    foot = f'<div class="foot"><span>{section}</span><span>{n}</span></div>' if section is not None else ""
    pages.append(f'<section class="page {cls}">{body}{foot}</section>')


def blank(title="Freie Seite"):
    state["n"] += 1
    n = state["n"]
    pages.append(f'<section class="page"><div class="blankfoot"><span>{title} · Datum: ____________ · '
                 f'Motiv: ______________________ · Zeit: ______ min</span><span>{n}</span></div></section>')


def head(kicker, title, lead=""):
    return f'<div class="kicker">{kicker}</div><h1>{title}</h1>' + (f'<p class="lead">{lead}</p>' if lead else "")


def mat(txt):
    return f'<div class="box mat"><b class="t">Material</b>{txt}</div>'


def ex(title, txt):
    return f'<div class="box ex"><b class="t">Übung · {title}</b>{txt}</div>'


def err(txt):
    return f'<div class="box err"><b class="t">Typische Fehler</b>{txt}</div>'


def steps(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def section(num, title, sub, points):
    page(f'<div class="num">{num}</div><h1>{title}</h1><p class="lead">{sub}</p>'
         + '<h2>Du lernst hier</h2><ul>' + "".join(f"<li>{p}</li>" for p in points) + "</ul>",
         section=f"Teil {num}", cls="section")


# =================================================================== Start
page(f"""
<div class="kicker">Arbeitsbuch zum Ausdrucken · A4 · für den Ringordner</div>
<h1 style="font-size:40pt;margin-top:8mm">SKIZZENBUCH</h1>
<p class="lead" style="font-size:15pt;margin-bottom:6mm">Zeichnen lernen – vom Würfel bis zum Gesicht,<br>vom Abzeichnen bis zum Zeichnen aus dem Kopf.</p>
{S.cover_art()}
<div style="margin-top:auto;font-size:11pt;line-height:2.4">
Name: ______________________________________________<br>
Begonnen am: ________________ &nbsp;&nbsp; Fertig am: ________________
</div>""", section=None)

page(head("Vorwort", "So benutzt du dieses Buch",
          "Dieses Buch ist für dich, wenn du schon ein bisschen gezeichnet hast und jetzt systematisch besser werden willst. "
          "Jeder Teil hat drei Arten von Seiten:") + """
<div class="row">
 <div class="box"><b class="t">Lernseiten</b>Erklären eine Technik mit Bildern, Schritten, Material und typischen Fehlern.</div>
 <div class="box ex"><b class="t">Übungsseiten</b>Vorgegebene Felder, Hilfslinien und Zeitangaben. Hier wird gearbeitet!</div>
 <div class="box"><b class="t">Freie Seiten</b>Komplett weiß. Für eigene Motive, Wiederholungen oder Studien.</div>
</div>
<h2>Die 6 Regeln, die am meisten bringen</h2>
<ol>
<li><b>Jeden Tag ein bisschen</b> – 20 Minuten täglich schlagen 3 Stunden am Sonntag.</li>
<li><b>Von groß nach klein:</b> erst die Gesamtform, dann Proportionen, erst ganz zum Schluss Details.</li>
<li><b>Hell anfangen, dunkel aufhören.</b> Hilfslinien mit wenig Druck, damit du sie wegradieren kannst.</li>
<li><b>Konstruieren statt abmalen:</b> Alles besteht aus Kugel, Würfel, Zylinder und Kegel. Wer diese Formen drehen kann, kann alles zeichnen – auch aus dem Kopf.</li>
<li><b>Viele schlechte Zeichnungen sind gut.</b> Menge schlägt Perfektion. Nicht radieren, sondern neu zeichnen.</li>
<li><b>Datieren!</b> Schreib auf jede Seite das Datum. In 3 Monaten wirst du staunen.</li>
</ol>
<h2>Druck-Tipps</h2>
<ul>
<li>Einseitig drucken (Graphit drückt durch). Der linke Rand ist breiter – dort lochen.</li>
<li>Papier: Normales 80 g/m² reicht für Übungen. Für schöne Seiten 120–160 g/m² oder Zeichenpapier (Laserdrucker-geeignet).</li>
<li>Freie Seiten kannst du mehrfach drucken oder direkt leeres Zeichenpapier einheften.</li>
<li>Drucker auf „Tatsächliche Größe / 100 %“ stellen, nicht „An Seite anpassen“.</li>
</ul>
<h2>Wie lange?</h2>
<p>Plane pro Teil etwa 1–2 Wochen. Du musst nicht der Reihe nach vorgehen – aber Teil 1 und 2 sind die Grundlage für alles danach.
Hinten findest du einen <b>30-Tage-Plan</b> und eine <b>Vorher/Nachher-Seite</b>.</p>
""", section="Vorwort")

TOC = [("1", "Material & Grundlagen", "Stifte, Linien, Tonwerte, Schraffur, Licht & Schatten"),
       ("2", "Formen & Perspektive", "Grundkörper, 1- und 2-Punkt-Perspektive, Ellipsen"),
       ("3", "Gesichter & Köpfe", "Loomis-Methode, Proportionen, Augen, Nase, Mund, Drehungen"),
       ("4", "Menschen", "Proportionen, Gliederpuppe, Bewegung, Hände & Füße"),
       ("5", "Autos & Technik", "Seitenansicht, 3/4-Ansicht, Räder als Ellipsen"),
       ("6", "Tiere, Natur & Gegenstände", "Tiere aus Formen, Bäume, Landschaft, Stillleben"),
       ("7", "Aus dem Kopf zeichnen", "Visuelle Bibliothek, Gedächtnis-Training, Drehen, Erfinden"),
       ("", "Trainingsplan", "30 Tage, Vorher/Nachher, freie Seiten")]
page(head("Übersicht", "Inhalt") + '<table class="toc">' + "".join(
    f'<tr><td><b>{("Teil " + a) if a else ""}</b></td><td><b>{b}</b><br><span class="small">{c}</span></td><td></td></tr>'
    for a, b, c in TOC) + '</table>' + """
<h2 style="margin-top:8mm">Legende in den Bildern</h2>
<table><tr><th>Linie</th><th>Bedeutung</th><th>Womit zeichnen?</th></tr>
<tr><td>— durchgezogen, kräftig</td><td>Endgültige Kontur</td><td>2B, mit mehr Druck</td></tr>
<tr><td>- - - grau gestrichelt</td><td>Hilfs-/Konstruktionslinie</td><td>HB oder 2H, ganz leicht</td></tr>
<tr><td>- - - schwarz gestrichelt</td><td>Verdeckte Kante (dahinter)</td><td>leicht, später radieren</td></tr>
<tr><td>breite graue Linie</td><td>Bewegungslinie (Line of Action)</td><td>HB, ein schneller Zug</td></tr>
</table>""", section="Inhalt")

# =================================================================== Teil 1
section(1, "Material & Grundlagen", "Bevor du Gesichter oder Autos zeichnest, brauchst du sichere Linien und ein Gefühl für Hell und Dunkel.",
        ["welche Stifte wofür", "lockere, gerade Linien und Ellipsen", "die Tonwertskala", "Schraffur-Techniken",
         "wie Licht auf Körper fällt"])

page(head("Teil 1 · Grundlagen", "Dein Werkzeug",
          "Du brauchst nicht viel. Teuer ist nicht wichtig – wichtig ist, dass du weißt, welcher Stift welche Aufgabe hat.")
     + S.pencil_scale() + """
<table>
<tr><th style="width:28%">Werkzeug</th><th>Wofür</th></tr>
<tr><td><b>2H oder HB</b></td><td>Hilfslinien, Konstruktion, erste Skizze. Lässt sich gut radieren.</td></tr>
<tr><td><b>2B</b></td><td>Dein Hauptstift: Konturen, mittlere Schatten. Wenn du nur einen Stift kaufst – diesen.</td></tr>
<tr><td><b>4B – 6B</b></td><td>Dunkle Schatten, Kontaktschatten, Akzente. Verschmiert leicht.</td></tr>
<tr><td><b>Druckbleistift 0,5 HB</b></td><td>Feine Details (Augen, Haare, Technik). Immer spitz.</td></tr>
<tr><td><b>Knetradiergummi</b></td><td>Tupft Graphit ab statt zu reiben – zum Aufhellen und für Glanzlichter. Formbar zur Spitze.</td></tr>
<tr><td><b>Radierstift / Kunststoffradierer</b></td><td>Saubere weiße Kanten, Hilfslinien entfernen.</td></tr>
<tr><td><b>Fineliner 0,3 / 0,5 + Brushpen</b></td><td>Für Teil 7 und Skizzen ohne Radieren – zwingt zu sicheren Strichen.</td></tr>
<tr><td><b>Papierwischer (Estompe)</b></td><td>Weiche Übergänge. Sparsam benutzen – nicht mit dem Finger (Hautfett!).</td></tr>
<tr><td><b>Cutter / Spitzer</b></td><td>Mit dem Cutter angespitzte lange Mine = flach für Flächen, spitz für Linien.</td></tr>
</table>
<h2>Stifthaltung</h2>
<div class="row">
<div><b>Schreibhaltung</b> – für Details und kleine Bereiche. Bewegung aus Fingern und Handgelenk.</div>
<div><b>Überhandhaltung</b> – Stift flach unter der Hand, wie ein Messer. Für lockere Skizzen, Flächen und lange Linien. Bewegung aus Ellbogen und Schulter.</div>
</div>
""" + mat("Starter-Set für ca. 15 €: Bleistifte HB, 2B, 4B, 6B · Knetradiergummi · Kunststoffradierer · Spitzer · Fineliner 0,3 + 0,5 · Papierwischer."),
     section="Teil 1 · Grundlagen")

page(head("Teil 1 · Grundlagen", "Sichere Linien",
          "Zittrige, gestrichelte Linien („Haarlinien“) sind der häufigste Anfängerfehler. Eine saubere Linie entsteht durch Tempo und Planung – nicht durch langsames Kriechen.")
     + S.line_demo() + steps([
         "<b>Ghosting:</b> Setze Start- und Endpunkt. Bewege den Stift 2–3 Mal in der Luft über die Strecke.",
         "Dann ziehe die Linie in <b>einem</b> zügigen Strich. Augen aufs Ziel, nicht auf die Mine!",
         "Lange Linien aus der <b>Schulter</b>, mittlere aus dem <b>Ellbogen</b>, kurze aus dem <b>Handgelenk</b>.",
         "Blatt drehen ist erlaubt – zieh in die Richtung, die für dich am leichtesten ist."])
     + mat("HB oder Fineliner (Fineliner = keine Korrektur möglich, ideal zum Üben).")
     + ex("Punkte verbinden", "Verbinde jedes Punktpaar mit einer geraden Linie in einem Zug. <span class='timer'>10 min</span>. Nicht nachbessern!")
     + '<div class="grow">' + S.dots_exercise(560, 330, 16, 3) + "</div>", section="Teil 1 · Grundlagen")

page(head("Teil 1 · Übung", "Linien & Ellipsen – Aufwärmblatt",
          "Mach diese Seite (ausgedruckt oder auf leerem Papier) vor jeder Zeichen-Session für 5–10 Minuten. Sie ist dein Aufwärmen.")
     + '<div class="box ex"><b class="t">Übung · 4 Felder</b><ol>'
       '<li>Oben links: parallele Linien, alle gleicher Abstand.</li>'
       '<li>Oben rechts: Punkte verbinden (setz die Punkte selbst).</li>'
       '<li>Unten links: Ellipsen um das Kreuz – 2× locker umkreisen, dann sauber.</li>'
       '<li>Unten rechts: Kreise freihand, möglichst rund. Kleine, mittlere, große.</li></ol></div>'
     + '<div class="grow">' + S.frames(4, 2, 560, 720, ["parallele Linien", "Punkte verbinden", "Ellipsen", "Kreise"], guide="cross") + "</div>",
     section="Teil 1 · Grundlagen")

page(head("Teil 1 · Grundlagen", "Tonwerte & Schraffur",
          "Tonwert = wie hell oder dunkel etwas ist. Farbe ist egal – im Schwarz-Weiß zählt nur der Tonwert. Gute Zeichnungen haben <b>echtes Weiß und echtes Schwarz</b>.")
     + S.value_scale(True) + steps([
         "Teile eine Fläche in 7 Felder. Feld 1 bleibt <b>papierweiß</b>, Feld 7 ist so dunkel wie möglich (6B, mehrere Schichten).",
         "Fülle die Mitte (4) zuerst, dann 2–3 und 5–6. Die Stufen sollen <b>gleichmäßig</b> wirken.",
         "Dunkel durch <b>Schichten</b>, nicht durch Druck! Viel Druck macht das Papier glänzend und es nimmt nichts mehr an."])
     + S.hatch_demo() + """
<div class="row">
<div><h2>Schraffur-Regeln</h2><ul>
<li>Striche <b>parallel</b> und gleich lang – wie ein Stoff.</li>
<li>Jede neue Schicht in leicht anderem Winkel (Kreuzschraffur).</li>
<li>Striche folgen der <b>Form</b> (um eine Kugel herum gebogen) – das erzeugt Volumen.</li>
<li>Am Strichende Druck wegnehmen → weiche Kanten.</li></ul></div>
<div>""" + mat("HB für helle Töne, 2B für Mitte, 4B–6B für Dunkel. Knetradiergummi zum Aufhellen.")
     + err("Alles nur grau (Angst vor Schwarz) · Kritzel-Schraffur in alle Richtungen · mit dem Finger verwischen.") + "</div></div>",
     section="Teil 1 · Grundlagen")

page(head("Teil 1 · Übung", "Tonwertskalen & Schraffurfelder")
     + ex("Tonwertskala", "Fülle jede Skala von 1 (weiß) bis 7 (schwarz). Skala 1 mit Verwischen, Skala 2 mit Parallelschraffur, Skala 3 mit Kreuzschraffur, Skala 4 mit Punkten (Fineliner). <span class='timer'>je 5 min</span>")
     + S.value_scale(False) + S.value_scale(False) + S.value_scale(False) + S.value_scale(False)
     + ex("Verlauf", "Ein weicher Übergang von weiß nach schwarz ohne sichtbare Stufen – erst mit Bleistift, dann mit Schraffur.")
     + '<div class="grow">' + S.frames(2, 1, 560, 260, ["Verlauf – Bleistift", "Verlauf – Schraffur"]) + "</div>",
     section="Teil 1 · Grundlagen")

page(head("Teil 1 · Grundlagen", "Licht & Schatten",
          "Jeder runde Körper hat die gleichen Zonen. Wenn du sie an der Kugel verstehst, kannst du jedes Gesicht, jeden Arm und jedes Auto schattieren.")
     + S.sphere_light() + steps([
         "<b>Lichtquelle festlegen</b> und mit einem kleinen Pfeil am Rand markieren. Das ist Pflicht!",
         "Kreis leicht zeichnen, Grenze zwischen Licht und Schatten (Schattenlinie) als Bogen andeuten.",
         "Gesamte Schattenseite in einem mittleren Ton anlegen (2B), dann den Schlagschatten auf dem Boden.",
         "Kernschatten dunkler (4B). Am Rand einen schmalen Streifen <b>heller</b> lassen – das Reflexlicht vom Boden.",
         "Halbtöne zum Licht hin weich auslaufen lassen. Glanzlicht frei lassen oder mit Knetgummi heraustupfen.",
         "Zum Schluss den Kontaktschatten direkt unter der Kugel fast schwarz (6B)."])
     + err("Reflexlicht zu hell (die Kugel wirkt flach) · Schlagschatten vergessen (Objekt schwebt) · Schatten mit dunkler Kontur umrandet.")
     + mat("HB, 2B, 4B, 6B, Papierwischer, Knetradiergummi."), section="Teil 1 · Grundlagen")

page(head("Teil 1 · Übung", "Kugel, Würfel, Zylinder schattieren")
     + ex("Grundkörper mit Licht", "Zeichne in jedes Feld den Körper und schattiere ihn. Die Lichtrichtung ist im Feld angegeben. "
          "Achte auf: Lichtseite, Schattenseite, Schlagschatten, Kontaktschatten. <span class='timer'>je 15 min</span>")
     + '<div class="grow">' + S.frames(6, 2, 560, 780, ["Kugel · Licht von links oben", "Kugel · Licht von rechts", "Würfel · Licht links oben",
                                                      "Würfel · Licht von vorne", "Zylinder · Licht links", "Kegel · Licht rechts oben"], guide="ground") + "</div>",
     section="Teil 1 · Grundlagen")

blank()

# =================================================================== Teil 2
section(2, "Formen & Perspektive", "Die wichtigste Fähigkeit, um aus dem Kopf zu zeichnen: einfache Körper glaubhaft im Raum darstellen.",
        ["die vier Grundkörper", "1-Punkt-Perspektive", "2-Punkt-Perspektive", "Ellipsen richtig zeichnen",
         "Gegenstände als Kisten aufbauen"])

page(head("Teil 2 · Perspektive", "Alles ist aus Grundkörpern gebaut",
          "Ein Kopf ist eine Kugel, ein Auto eine Kiste, ein Arm ein Zylinder, eine Nase ein Keil. Zeichne Körper immer „durchsichtig“ – auch die Kanten, die man nicht sieht.")
     + S.basic_shapes() + """
<table><tr><th>Grundkörper</th><th>Steckt in …</th></tr>
<tr><td>Kugel</td><td>Kopf, Augapfel, Schultergelenk, Apfel, Baumkrone</td></tr>
<tr><td>Würfel / Quader</td><td>Auto, Haus, Brustkorb (vereinfacht), Becken, Handfläche, Möbel</td></tr>
<tr><td>Zylinder</td><td>Arme, Beine, Hals, Finger, Tassen, Räder, Flaschen</td></tr>
<tr><td>Kegel</td><td>Nase, Lampenschirm, Tannenbaum, Schnabel, Hut</td></tr></table>
""" + steps(["Zeichne die Körper zuerst mit Hilfslinien (HB, leicht) und mit verdeckten Kanten.",
             "Prüfe: Sind Senkrechte senkrecht? Laufen parallele Kanten zusammen? Sind Ellipsen rund statt spitz?",
             "Dann die sichtbaren Kanten kräftig nachziehen (2B)."])
     + ex("Formen-Wand", "Fülle eine freie Seite komplett mit Würfeln, Zylindern, Kegeln und Kugeln in allen Größen und Lagen – auch gekippt und überlappend. "
          "<span class='timer'>20 min</span>. Diese Übung kannst du jede Woche wiederholen."),
     section="Teil 2 · Formen & Perspektive")

page(head("Teil 2 · Perspektive", "1-Punkt-Perspektive",
          "Du schaust frontal auf eine Fläche. Alle Linien, die von dir weg in die Tiefe gehen, laufen in <b>einem</b> Fluchtpunkt (FP) auf dem Horizont zusammen.")
     + S.one_point() + steps([
         "Horizontlinie ziehen = deine Augenhöhe. Einen Fluchtpunkt darauf setzen.",
         "Vorderseite der Kiste als normales Rechteck zeichnen.",
         "Von jeder Ecke eine Linie zum Fluchtpunkt ziehen (leicht!).",
         "Die Tiefe festlegen: eine waagerechte und eine senkrechte Linie schließen die Rückseite."])
     + """<div class="row"><div>""" + mat("Lineal erlaubt für die ersten Übungen, danach freihand. HB für Fluchtlinien, 2B für Kanten.")
     + "</div><div>" + err("Fluchtlinien zu anderen Punkten · Kiste zu tief (sieht verzerrt aus – lieber kurz halten) · Senkrechte kippen.") + "</div></div>"
     + "<p><b>Typische Motive:</b> Straße/Zugschienen von vorne, Flur, Zimmer, Regal frontal, Buchstaben in 3D.</p>",
     section="Teil 2 · Formen & Perspektive")

page(head("Teil 2 · Perspektive", "2-Punkt-Perspektive",
          "Du schaust auf eine Ecke. Jetzt gibt es zwei Fluchtpunkte – einen links, einen rechts. Das ist die Perspektive für Autos, Häuser und fast alles Alltägliche.")
     + S.two_point() + steps([
         "Horizont ziehen, zwei Fluchtpunkte <b>weit auseinander</b> setzen (gerne sogar außerhalb des Blattes – Klebestreifen-Verlängerung!).",
         "Vorderste senkrechte Kante zeichnen.",
         "Oben und unten von der Kante je eine Linie zu beiden Fluchtpunkten.",
         "Breite links und rechts mit zwei Senkrechten festlegen.",
         "Von diesen Ecken über Kreuz zum jeweils anderen FP – wo sie sich treffen, liegt die hintere Ecke."])
     + "<p>Liegen die Fluchtpunkte zu nah beieinander, wirkt die Kiste <b>verzerrt</b> (wie mit Fischaugen-Objektiv). Faustregel: Abstand der FP mindestens 3× so breit wie dein Objekt.</p>"
     + mat("Lineal, langes Papier oder Klebeband für weit entfernte Fluchtpunkte, HB, 2B."),
     section="Teil 2 · Formen & Perspektive")

page(head("Teil 2 · Übung", "Kisten-Stadt", "")
     + ex("2-Punkt-Kisten", "Zeichne mindestens 10 Kisten: über, unter und auf dem Horizont. Mach daraus dann Häuser, ein Regal, einen Würfelturm. "
          "Verdeckte Kanten gestrichelt einzeichnen! <span class='timer'>30 min</span>")
     + '<div class="grow">' + S.persp_sheet(2) + "</div>", section="Teil 2 · Formen & Perspektive")

page(head("Teil 2 · Perspektive", "Ellipsen & Zylinder",
          "Ein Kreis in Perspektive wird zur Ellipse. Ellipsen findest du überall: Tassen, Räder, Augen, Arme, Flaschen.")
     + S.ellipses_demo() + steps([
         "Erst die <b>Mittelachse</b> (bei einem Zylinder die Senkrechte durch die Mitte) zeichnen.",
         "Die große Achse der Ellipse steht immer <b>im rechten Winkel</b> zur Mittelachse.",
         "Ellipse in einer kreisenden Bewegung aus dem Ellbogen, mehrmals locker umrunden.",
         "Je weiter die Ellipse unter (oder über) deiner Augenhöhe liegt, desto runder ist sie."])
     + err("Spitze Enden wie ein Auge · Ellipse oben runder als unten · Ellipse schief zur Achse.")
     + ex("Ellipsen-Leiter", "Zeichne auf eine freie Seite 5 Zylinder nebeneinander: der erste auf Augenhöhe, jeder nächste tiefer. "
          "Dann: 3 Tassen, 2 Flaschen, 1 Rad. <span class='timer'>20 min</span>"),
     section="Teil 2 · Formen & Perspektive")

blank()

# =================================================================== Teil 3
section(3, "Gesichter & Köpfe", "Gesichter wirken schwer, weil wir sie so gut kennen – jeder kleine Fehler fällt auf. Mit einer Konstruktion triffst du die Proportionen sicher.",
        ["die Loomis-Methode (Kopf aus Kugel)", "Proportionen des Gesichts", "Augen, Nase, Mund, Ohren", "den Kopf drehen und neigen",
         "Gesichter schattieren"])

page(head("Teil 3 · Gesichter", "Der Kopf als Kugel (Loomis-Methode)",
          "Der Illustrator Andrew Loomis hat eine Methode entwickelt, mit der du einen Kopf aus jeder Richtung konstruieren kannst – ohne Vorlage.")
     + S.heads_construction() + steps([
         "<b>Kugel</b> zeichnen (HB, ganz leicht). Das ist der Schädel.",
         "Links und rechts eine <b>Scheibe abschneiden</b> – das sind die Schläfenflächen. Frontal: zwei senkrechte Linien.",
         "<b>Mittellinie</b> senkrecht durch die Kugel und darüber hinaus nach unten verlängern.",
         "<b>Brauenlinie</b> durch die Mitte der Kugel. Die Strecke Haaransatz–Braue nach unten zweimal abtragen: Nasenunterkante und Kinn.",
         "Kiefer von der Seitenfläche zum Kinn. Fertig ist das „Gerüst“ – jetzt kommen die Merkmale drauf."])
     + mat("HB oder 2H für das Gerüst, 2B für Merkmale, Knetradiergummi um das Gerüst am Ende aufzuhellen."),
     section="Teil 3 · Gesichter")

page(head("Teil 3 · Gesichter", "Proportionen des Gesichts",
          "Diese Regeln gelten für einen durchschnittlichen Erwachsenen von vorne. Echte Menschen weichen ab – genau das macht Ähnlichkeit aus. Aber zuerst die Regel kennen!")
     + '<div class="row"><div style="flex:1.25">' + S.head_proportions() + "</div><div>" + """
<h2>Merksätze</h2><ul class="small">
<li>Die <b>Augen</b> sitzen auf halber Kopfhöhe – nicht oben! (Häufigster Fehler.)</li>
<li>Haaransatz → Braue → Nase → Kinn: <b>drei gleiche Abstände</b>.</li>
<li>Zwischen den Augen passt <b>ein Auge</b>.</li>
<li>Nasenflügel ≈ so breit wie der Augenabstand (innere Augenwinkel).</li>
<li>Mund ≈ auf 1/3 zwischen Nase und Kinn.</li>
<li>Ohren zwischen Brauenlinie und Nasenunterkante.</li>
<li>Der Hals ist breiter, als man denkt – fast so breit wie der Kiefer.</li></ul>
</div></div>""" + S.ear_and_eyes_spacing()
     + ex("Proportions-Check", "Zeichne 3 Gesichter frontal nach dem Schema. Kontrolliere jede Regel mit einem Stift als Messlatte. <span class='timer'>3 × 10 min</span>"),
     section="Teil 3 · Gesichter")

page(head("Teil 3 · Gesichter", "Augen, Nase, Mund",
          "Merkmale sind keine Symbole, sondern Formen mit Volumen. Das Auge ist eine Kugel unter Lidern, die Nase ein Keil, der Mund liegt auf einem Zylinder.")
     + S.features() + """
<div class="row">
<div><h2>Auge</h2><ol class="small">
<li>Kugel (Augapfel) andeuten.</li>
<li>Oberlid als Bogen über die Kugel, Unterlid flacher.</li>
<li>Iris rund, oben vom Lid angeschnitten. Pupille dunkel (6B).</li>
<li>Oberlid hat Dicke und wirft Schatten auf den Augapfel.</li>
<li>Wimpern nur als dunkle Kante am Oberlid, nicht einzeln.</li></ol></div>
<div><h2>Nase</h2><ol class="small">
<li>Keil von Brauen bis Nasenspitze.</li>
<li>Unterseite als Fläche: Kugel für Spitze, zwei Flügel.</li>
<li>Nasenlöcher dunkel, aber klein.</li>
<li>Nasenrücken <b>nicht</b> mit Linien, nur mit Schatten auf einer Seite.</li></ol></div>
<div><h2>Mund</h2><ol class="small">
<li>Mittellinie zuerst – sie ist die dunkelste Stelle.</li>
<li>Oberlippe: „M“-Form, meist im Schatten (dunkler).</li>
<li>Unterlippe: voller, im Licht, nur durch den Schatten darunter zeigen.</li>
<li>Mundwinkel leicht vertieft.</li></ol></div>
</div>""" + mat("Druckbleistift HB für Details, 2B / 4B für Pupille und Mundlinie, Knetgummi für Glanzlicht und Lichtreflexe auf den Lippen.")
     + err("Lippen komplett umranden · Augen als Fisch-Form ohne Lid · Nase mit zwei Seitenlinien („Röhre“) · Wimpern wie Zaunpfähle."),
     section="Teil 3 · Gesichter")

page(head("Teil 3 · Gesichter", "Den Kopf drehen",
          "Wenn sich der Kopf dreht, krümmen sich die Hilfslinien um die Kugel. Die Mittellinie wird zur Kurve, die Brauenlinie bleibt (bei Augenhöhe) gerade.")
     + S.head_turns() + steps([
         "<b>Kugel</b> und die <b>Mittellinie als Bogen</b> – je stärker die Drehung, desto weiter wandert sie zum Rand.",
         "Die <b>Seitenfläche</b> (Ellipse) wird auf der abgewandten Seite schmaler, auf der zugewandten breiter.",
         "Brauen-, Nasen- und Kinnlinie wie gewohnt eintragen.",
         "<b>3/4-Ansicht:</b> Das hintere Auge wird schmaler, die Nase verdeckt einen Teil der Wange dahinter.",
         "<b>Nicken:</b> Schaut der Kopf nach oben, biegen sich die waagerechten Linien nach oben (wie ein Lächeln), nach unten wie ein Stirnrunzeln."])
     + err("Bei 3/4 beide Augen gleich groß · Ohr zu weit vorne · Kinn in der 3/4-Ansicht nicht unter der Mittellinie.")
     + ex("Kopf-Karussell", "Zeichne denselben Kopf in 8 Richtungen: frontal, 3/4 links/rechts, Profil links/rechts, von oben, von unten, schräg von unten. "
          "<span class='timer'>40 min</span> – die nächste Seite hat die Kugeln schon vorbereitet."),
     section="Teil 3 · Gesichter")

page(head("Teil 3 · Übung", "Köpfe konstruieren")
     + ex("Gerüst ausbauen", "In jeder Kugel einen Kopf in einer anderen Drehung konstruieren: Mittellinie, Seitenfläche, Brauen/Nase/Kinn – dann Merkmale. "
          "Nicht schattieren, nur Linien. <span class='timer'>je 5–8 min</span>")
     + '<div class="grow">' + S.head_guides(9, 3, 560, 800) + "</div>", section="Teil 3 · Gesichter")

page(head("Teil 3 · Übung", "Merkmale studieren")
     + ex("Studienblatt", "Fotos aus Zeitschriften oder dem Internet (oder dein Spiegelbild) als Vorlage. In jedes Feld eine Studie, schattiert. "
          "Lichtrichtung immer zuerst festlegen. <span class='timer'>je 10 min</span>")
     + '<div class="grow">' + S.frames(9, 3, 560, 800, ["Auge frontal", "Auge 3/4", "Auge Profil", "Nase frontal", "Nase 3/4", "Nase Profil",
                                                      "Mund frontal", "Mund lächelnd", "Ohr"]) + "</div>", section="Teil 3 · Gesichter")

page(head("Teil 3 · Gesichter", "Ein Gesicht schattieren – Ablauf",
          "Jetzt kommt alles zusammen. Nimm ein Foto mit klarem Licht von der Seite (keine Blitz-Fotos – die sind flach).")
     + steps([
         "<b>Gerüst</b> (Loomis) leicht mit HB. Proportionen prüfen, bevor du weitermachst – später kannst du nichts mehr retten.",
         "<b>Merkmale</b> platzieren: Augen, Nase, Mund, Ohren als einfache Formen.",
         "<b>Schattenformen</b> als Flächen einzeichnen: Augenhöhlen, Seite der Nase, unter der Nase, unter der Unterlippe, unter dem Kinn, Schattenseite des Gesichts.",
         "<b>Ein Mittelton</b> (2B) über alle Schattenflächen. Jetzt hast du zwei Töne: Licht und Schatten. Kneif die Augen zusammen und vergleiche mit dem Foto.",
         "<b>Dunkelste Stellen</b> (4B–6B): Pupillen, Nasenlöcher, Mundlinie, Kontaktschatten unter dem Kinn, Haare.",
         "<b>Halbtöne</b> zwischen Licht und Schatten weich verbinden.",
         "<b>Lichter</b> mit Knetgummi: Glanzpunkt im Auge, Nasenspitze, Unterlippe, Stirn.",
         "Haare als <b>Masse</b> mit Licht und Schatten, nur am Rand und in der Lichtzone einzelne Strähnen."])
     + """<div class="row"><div>""" + mat("HB, 2B, 4B, 6B, Papierwischer, Knetradiergummi, Radierstift für feine Lichter.")
     + "</div><div>" + err("Zu früh Details (Wimpern!) · Konturlinie überall gleich dunkel · Schatten zu zaghaft – trau dich!") + "</div></div>"
     + """<h2>Die „Augen zukneifen“-Technik</h2><p>Kneif die Augen fast zu, wenn du dein Motiv anschaust. Details verschwinden, nur große Hell-Dunkel-Formen bleiben.
     Genau die musst du zuerst zeichnen. Mach das alle 5 Minuten – auch mit deiner eigenen Zeichnung.</p>
     <h2>Spiegel-Trick</h2><p>Halte deine Zeichnung vor einen Spiegel (oder fotografiere sie und spiegle das Foto). Fehler in der Symmetrie springen sofort ins Auge.</p>""",
     section="Teil 3 · Gesichter")

blank()
blank()

# =================================================================== Teil 4
section(4, "Menschen", "Der Körper ist schwierig, weil er sich bewegt. Darum zeichnen wir zuerst die Bewegung, dann die Formen, ganz zuletzt die Details.",
        ["Proportionen in Kopfhöhen", "die Gliederpuppe als Gerüst", "Bewegungslinie & Gesture Drawing", "Hände und Füße",
         "Figuren aus dem Kopf in jeder Pose"])

page(head("Teil 4 · Menschen", "Proportionen in Kopfhöhen",
          "Der Kopf ist das Maß. Ein Erwachsener ist ca. 7½ bis 8 Köpfe groß (Comic-Helden 8–9, Kinder 4–6).")
     + S.proportions_8() + '<div class="row small">' + """
<div><h2>So misst du</h2><ol>
<li>Höhe der Figur oben und unten markieren.</li>
<li>In 8 Teile teilen (halbieren, nochmal halbieren, nochmal halbieren).</li>
<li>Oberstes Feld = Kopf. Schritt liegt genau auf der Hälfte.</li></ol></div>
<div><h2>Männlich / weiblich</h2><ul>
<li>Männer: Schultern breiter als Hüfte, kantiger Brustkorb.</li>
<li>Frauen: Hüfte ≈ Schulterbreite oder breiter, Taille schmaler.</li></ul></div>
<div><h2>Merkhilfen</h2><ul>
<li>Ellbogen auf Taillenhöhe.</li>
<li>Handgelenk auf Schritthöhe.</li>
<li>Hand ≈ Gesicht groß.</li>
<li>Fuß ≈ Unterarm lang.</li></ul>
</div></div>""" + ex("Messen", "Zeichne 3 stehende Figuren auf eine freie Seite: 8 Köpfe, 6 Köpfe (Jugendlicher), 4 Köpfe (Kleinkind). <span class='timer'>20 min</span>"),
     section="Teil 4 · Menschen")

page(head("Teil 4 · Menschen", "Die Gliederpuppe",
          "Wie die Holzpuppe aus dem Künstlerbedarf: Brustkorb und Becken als zwei feste Blöcke, Wirbelsäule biegt sich, Arme und Beine sind Röhren mit Gelenken.")
     + S.mannequin_steps() + steps([
         "<b>Bewegungslinie</b> (eine Kurve von Kopf bis Standbein) – 2 Sekunden, ein Strich.",
         "<b>Strichmännchen</b> darüber: Kopf, Schulterlinie, Hüftlinie, Gelenke als Punkte. Schulter- und Hüftlinie sind oft gegeneinander gekippt (Kontrapost).",
         "<b>Brustkorb</b> als Ei, <b>Becken</b> als Schale/Box, verbunden durch die biegsame Wirbelsäule.",
         "<b>Arme und Beine</b> als Zylinder, die sich zur Mitte hin verjüngen. Gelenke als Kugeln.",
         "Erst jetzt: Muskeln, Kleidung, Hände, Gesicht."])
     + """<div class="row"><div>""" + mat("Zuerst Bleistift HB, für Gesture-Übungen lieber Fineliner oder Brushpen (zwingt dich zu klaren Strichen).")
     + "</div><div>" + err("Steife „Zinnsoldaten“ · Becken vergessen · Arme zu kurz · Figur steht nicht (Schwerpunkt prüfen: Kopf über dem Standbein!)") + "</div></div>",
     section="Teil 4 · Menschen")

page(head("Teil 4 · Menschen", "Bewegung zeichnen (Gesture Drawing)",
          "Gesture-Zeichnungen sind schnelle Skizzen von 30 Sekunden bis 2 Minuten. Ziel ist nicht Schönheit, sondern Energie: Was macht die Figur?")
     + S.gestures() + """
<div class="row"><div><h2>Ablauf (1 Minute)</h2><ol>
<li>5 Sek: Pose anschauen. Wo ist die Hauptkurve?</li>
<li>5 Sek: Bewegungslinie ziehen.</li>
<li>20 Sek: Kopf, Brustkorb, Becken.</li>
<li>30 Sek: Arme und Beine als Linien, Hände/Füße als Dreiecke.</li></ol></div>
<div><h2>Gute Vorlagen</h2><ul>
<li>Websites mit Posen-Timern (Suchbegriff: <i>„gesture drawing timer“</i>, z.&nbsp;B. Line of Action, Quickposes).</li>
<li>Sportfotos, Tanz, Kampfsport.</li>
<li>Leute im Café, Bahn, Park – die besten Lehrer!</li>
<li>Videos pausieren.</li></ul></div></div>
""" + mat("Kohle, weicher Bleistift (4B) oder Brushpen. Großes Papier, Überhandhaltung, aus der Schulter zeichnen.")
     + "<p><b>C-Kurve, S-Kurve, gerade Linie:</b> Fast jede Pose lässt sich auf eine dieser drei Formen zurückführen. Gegenüber einer Kurve steht oft eine gerade Seite (z.&nbsp;B. Rücken gebogen, Bauch gestreckt).</p>",
     section="Teil 4 · Menschen")

page(head("Teil 4 · Übung", "Gesture-Session")
     + ex("Gesture mit Timer", "Stelle einen Posen-Timer ein. Erste Reihe 30 Sekunden, zweite Reihe 1 Minute, dritte Reihe 2 Minuten. "
          "Nur Bewegungslinie + Strichmännchen + Grundformen. Nicht radieren! <span class='timer'>gesamt ca. 20 min</span>")
     + '<div class="grow">' + S.frames(12, 4, 560, 800, ["30 s", "30 s", "30 s", "30 s", "1 min", "1 min", "1 min", "1 min", "2 min", "2 min", "2 min", "2 min"]) + "</div>",
     section="Teil 4 · Menschen")

page(head("Teil 4 · Menschen", "Hände & Füße",
          "Hände gelten als das Schwierigste – dabei sind sie nur ein Kästchen mit fünf Röhren. Deine beste Vorlage hast du immer dabei: deine linke Hand.")
     + S.hand() + steps([
         "<b>Handfläche</b> als flaches Kästchen (leicht trapezförmig). Gibt die Richtung vor.",
         "<b>Knöchelbogen</b> und <b>Fingerspitzenbogen</b> einzeichnen – die Finger sind nicht gleich lang.",
         "Finger als <b>Zylinder in drei Gliedern</b> (Längen ca. 3 : 2 : 1,5). Die Gelenke liegen auch auf Bögen.",
         "<b>Daumen</b> setzt weit unten an der Handwurzel an und hat einen dicken Ballen.",
         "Konturen weich verbinden, Falten nur an den Gelenken andeuten."])
     + "<p><b>Füße:</b> Von der Seite ein Keil, von vorne ein Trapez. Der Innenknöchel liegt höher als der Außenknöchel. Zehen zuerst als eine Masse, dann unterteilen.</p>"
     + err("Finger wie Würstchen gleicher Länge · Daumen setzt zu hoch an · Hände zu klein (Hand ≈ Gesicht!).")
     + ex("100 Hände", "Zeichne über die nächsten Wochen 100 Hände (eigene Hand in allen Haltungen, Fotos). Zähle mit: ______ / 100"),
     section="Teil 4 · Menschen")

page(head("Teil 4 · Übung", "Gliederpuppen-Posen")
     + ex("Pose umbauen", "In jedes Feld eine Gliederpuppe: <b>stehen, sitzen, laufen, springen, bücken, liegen, werfen, über die Schulter schauen</b>. "
          "Zuerst nach Foto, dann die gleiche Pose aus einer anderen Richtung <b>erfinden</b>. <span class='timer'>je 5 min</span>")
     + '<div class="grow">' + S.frames(8, 2, 560, 800, ["stehen (Kontrapost)", "sitzen auf Stuhl", "laufen", "springen", "bücken / heben",
                                                      "liegen", "werfen", "über die Schulter schauen"], guide="ground") + "</div>",
     section="Teil 4 · Menschen")

blank()
blank()

# =================================================================== Teil 5
section(5, "Autos & Technik", "Autos sind perfekt zum Lernen: harte Kanten, klare Perspektive, Ellipsen. Wer ein Auto aus einer Kiste bauen kann, kann jedes Gerät zeichnen.",
        ["Proportionen mit dem Rad als Maß", "Seitenansicht in 3 Schritten", "3/4-Ansicht aus Kisten", "Räder als Ellipsen",
         "Spiegelungen auf Lack und Glas"])

page(head("Teil 5 · Autos", "Seitenansicht in drei Schritten",
          "Das Rad ist das Maß aller Dinge. Bestimme zuerst die Radgröße – daraus ergeben sich Länge, Höhe und Radstand.")
     + "<h2>1 · Kiste und Räder</h2>" + S.car_side(1)
     + "<h2>2 · Silhouette (Umriss)</h2>" + S.car_side(2)
     + "<h2>3 · Fenster, Türen, Lichter, Schatten</h2>" + S.car_side(3)
     + steps([
         "Bodenlinie ziehen, zwei Kreise für die Räder. Ein Rad als Maßeinheit: Länge ≈ 6–7 Räder (Kleinwagen 5½, Limousine 7).",
         "Kiste um das Auto. Höhe ≈ 2 Räder (Sportwagen 1½, SUV 2½).",
         "Silhouette: Motorhaube, Windschutzscheibe (schräg!), Dach, Heck. Radhäuser als Bögen etwas größer als das Rad.",
         "Fensterfläche, Türfugen, Lichter, Felgen. Der Schatten unter dem Auto lässt es auf dem Boden stehen."])
     + mat("Lineal und Ellipsen-/Kreisschablone erlaubt (Profis nutzen sie auch). HB, 2B, Fineliner 0,3 für Fugen, 6B für Reifen und Schatten."),
     section="Teil 5 · Autos")

page(head("Teil 5 · Autos", "3/4-Ansicht aus Kisten",
          "Jetzt wird die Kiste in 2-Punkt-Perspektive gestellt. Erst eine Kiste für den Unterbau, eine kleinere für die Kabine, dann wegschneiden und runden.")
     + S.car_34() + steps([
         "Horizont festlegen: über dem Auto (wie im Bild) = du stehst daneben und siehst das Dach. Tief gelegt (unter halber Autohöhe) wirkt das Auto mächtiger. Fluchtpunkte weit außen.",
         "Unterbau-Kiste in 2-Punkt-Perspektive. Die lange Seite zum weiter entfernten Fluchtpunkt.",
         "Kabine als kleinere Kiste obendrauf, nach hinten versetzt.",
         "Radmittelpunkte auf der Seitenfläche markieren. Räder als Ellipsen: die <b>kurze Achse</b> der Ellipse zeigt zum anderen Fluchtpunkt (Richtung Radachse).",
         "Kanten abschrägen: Windschutzscheibe, Motorhaube, Heck. Ecken runden.",
         "Spiegelungen: Auf dem Lack spiegelt sich oben der Himmel (hell), unten der Boden (dunkel), dazwischen ein harter Horizont-Streifen."])
     + err("Räder als Kreise statt Ellipsen · beide Räder gleich groß (das hintere ist kleiner/schmaler) · Auto zu kurz · Fluchtpunkte zu nah.")
     + "<p><b>Tipp:</b> Sammle Fotos von Autos im 3/4-Winkel und zeichne zuerst nur die Kiste darüber (Transparentpapier oder dünnes Papier auf dem Tablet). So lernst du die Proportionen.</p>",
     section="Teil 5 · Autos")

page(head("Teil 5 · Übung", "Autos konstruieren")
     + ex("Vom Rad zum Auto", "Felder 1–3: Seitenansichten (Kleinwagen, Sportwagen, SUV) mit dem Rad als Maß. "
          "Felder 4–6: dieselben Autos in 3/4-Ansicht aus Kisten. Die Bodenlinie ist vorgegeben. <span class='timer'>je 15 min</span>")
     + '<div class="grow">' + S.frames(6, 2, 560, 800, ["Kleinwagen · Seite", "Kleinwagen · 3/4", "Sportwagen · Seite", "Sportwagen · 3/4",
                                                      "SUV · Seite", "SUV · 3/4"], guide="ground") + "</div>",
     section="Teil 5 · Autos")

page(head("Teil 5 · Technik", "Andere Fahrzeuge & Geräte",
          "Mit der gleichen Methode – Kiste, Zylinder, wegschneiden – zeichnest du alles Technische.")
     + """<table>
<tr><th style="width:24%">Motiv</th><th>Grundformen</th><th>Achte auf</th></tr>
<tr><td><b>Fahrrad</b></td><td>2 Kreise, Dreiecke für den Rahmen</td><td>Räder ≈ ein Rad Abstand, Sattel ≈ über Tretlager</td></tr>
<tr><td><b>Motorrad</b></td><td>2 Räder, Tank als Ei, Motor als Kiste</td><td>Neigung in Kurven = ganze Kiste kippen</td></tr>
<tr><td><b>LKW / Bus</b></td><td>2–3 Kisten hintereinander</td><td>sehr lang, Fluchtpunkte besonders weit</td></tr>
<tr><td><b>Flugzeug</b></td><td>Zylinder + flache Kisten (Flügel)</td><td>Flügel symmetrisch zur Mittelachse</td></tr>
<tr><td><b>Handy, Kamera, Kopfhörer</b></td><td>flache Kiste, Zylinder, Torus (Ring)</td><td>Rundungen erst nach der Kiste</td></tr>
<tr><td><b>Haus / Straße</b></td><td>Kisten, 1- oder 2-Punkt</td><td>Fenster laufen zu den gleichen FP</td></tr>
</table>""" + ex("Technik-Woche", "Zeichne jeden Tag einen Gegenstand aus deinem Zimmer als Kiste/Zylinder-Konstruktion – und danach <b>den gleichen</b> aus einem anderen Blickwinkel, ohne hinzuschauen.")
     + '<div class="grow">' + S.frames(4, 2, 560, 420, ["Gegenstand – nach Vorlage", "gleicher Gegenstand – gedreht, aus dem Kopf",
                                                      "Fahrzeug – nach Vorlage", "Fahrzeug – erfunden"]) + "</div>",
     section="Teil 5 · Technik")

blank()

# =================================================================== Teil 6
section(6, "Tiere, Natur & Gegenstände", "Hier wendest du alles an: Formen, Perspektive, Licht. Jedes Motiv wird erst zerlegt, dann aufgebaut.",
        ["Tiere aus Kreisen und Kästen", "Bäume und Pflanzen als Massen", "Landschaft in drei Ebenen", "Stillleben und Alltagsgegenstände"])

page(head("Teil 6 · Tiere", "Tiere aus Grundformen",
          "Fast alle Säugetiere haben das gleiche Grundgerüst: großer Brustkorb, kleineres Becken, Kopf, vier Beine. Nur die Proportionen ändern sich.")
     + S.dog() + steps([
         "<b>Bewegungslinie</b> über den Rücken bis zum Kopf.",
         "<b>Brustkorb</b> (großer Kreis), <b>Becken</b> (kleinerer Kreis), <b>Kopf</b> (Kreis + Schnauzen-Kasten).",
         "Verbinde mit Rücken- und Bauchlinie.",
         "<b>Beine</b> als Linien mit Gelenkpunkten. Tiere stehen auf den Zehen – das „Knie“ hinten ist eigentlich die Ferse.",
         "Fell als Masse mit Licht und Schatten, Fellstriche nur an Rand und Schattengrenze in Wuchsrichtung."])
     + """<div class="row"><div>""" + mat("HB für Gerüst, 2B/4B, für Fell Knetgummi zum Heraustupfen heller Strähnen. Für schnelle Tierskizzen: Fineliner.")
     + "</div><div>" + "<p class='small'><b>Vorlagen:</b> Zoo, Haustiere (schlafende Tiere sind ideal!), Tierdokus pausieren. Katzen: Kreis-Körper, Hunde: lange Brust, Pferde: Brustkorb sehr groß, Beine lang und dünn.</p></div></div>",
     section="Teil 6 · Tiere")

page(head("Teil 6 · Natur", "Bäume, Pflanzen & Landschaft",
          "In der Natur ist die Versuchung groß, jedes Blatt zu zeichnen. Das Geheimnis: Gruppen von Blättern als Masse sehen – wie Wolken mit einer Licht- und einer Schattenseite.")
     + S.tree_and_landscape() + """
<div class="row"><div><h2>Baum</h2><ol class="small">
<li>Stamm verjüngt sich nach oben, Äste teilen sich wie ein Y.</li>
<li>Laub als 3–7 große „Wolken“.</li>
<li>Schattenseite der Wolken dunkel, Lichtseite fast weiß.</li>
<li>Löcher im Laub zeigen den Himmel – nicht vergessen!</li>
<li>Rand ausfransen mit kurzen, unregelmäßigen Strichen.</li></ol></div>
<div><h2>Landschaft</h2><ol class="small">
<li>Kleines Vorschaubild (Thumbnail) 6 × 4 cm: Komposition finden.</li>
<li>Horizont nie genau in der Mitte – oben oder unten im Drittel.</li>
<li>Hintergrund hell, kontrastarm. Vordergrund dunkel, scharf, detailliert.</li>
<li>Wolken und Wasser sparsam: Weiß lassen ist oft besser.</li></ol></div></div>
""" + mat("Bleistift flach geführt (lange Mine) für Flächen, 6B für Vordergrund, Fineliner/Brushpen für schnelle Outdoor-Skizzen.")
     + ex("Draußen zeichnen", "Setz dich 20 Minuten nach draußen und zeichne 4 Thumbnails (Mini-Skizzen) desselben Ortes aus verschiedenen Blickwinkeln auf eine freie Seite. Wähle den besten und mach ihn groß."),
     section="Teil 6 · Natur")

page(head("Teil 6 · Gegenstände", "Stillleben & Alltagsgegenstände",
          "Ein Stillleben bewegt sich nicht und läuft nicht weg – perfekt, um Formen, Licht und Oberflächen (Glas, Metall, Stoff) zu üben.")
     + S.still_life() + steps([
         "Gegenstände auf einen Tisch, <b>eine</b> Lampe von der Seite. Deckenlicht aus.",
         "Jeden Gegenstand in seine Grundform zerlegen: Tasse = Zylinder, Flasche = Zylinder + Kegel, Buch = Quader, Apfel = Kugel.",
         "Bei symmetrischen Dingen <b>Mittellinie</b> zuerst, dann beide Seiten gleich.",
         "Größenverhältnisse mit dem Stift messen (Arm ausstrecken, Daumen auf dem Stift verschieben).",
         "Licht & Schatten wie an der Kugel. Schlagschatten verbinden die Gegenstände miteinander."])
     + """<table><tr><th>Oberfläche</th><th>So zeichnest du sie</th></tr>
<tr><td>Glas</td><td>Fast nur Hintergrund durchscheinen lassen, harte weiße Lichtkanten, dunkle Ränder.</td></tr>
<tr><td>Metall / Chrom</td><td>Extreme Kontraste: Schwarz direkt neben Weiß, Umgebung spiegelt sich verzerrt.</td></tr>
<tr><td>Stoff</td><td>Falten entstehen an Stützpunkten. Röhrenfalten, Zickzack an Knick-Stellen.</td></tr>
<tr><td>Holz</td><td>Erst Licht/Schatten, dann Maserung leicht obendrauf.</td></tr></table>""",
     section="Teil 6 · Gegenstände")

page(head("Teil 6 · Übung", "Studienblatt Natur & Dinge")
     + ex("Gemischtes Studienblatt", "Pro Feld eine Studie nach echter Vorlage. Zuerst die Grundform leicht, dann ausarbeiten. <span class='timer'>je 10–15 min</span>")
     + '<div class="grow">' + S.frames(6, 2, 560, 800, ["Haustier / Tier – schlafend", "Vogel", "Baum", "Pflanze im Topf",
                                                      "Tasse + Löffel (Metall)", "Glas mit Wasser"]) + "</div>",
     section="Teil 6 · Übung")

blank()

# =================================================================== Teil 7
section(7, "Aus dem Kopf zeichnen", "Aus dem Kopf zeichnen ist kein Talent, sondern Training. Du brauchst zwei Dinge: eine „visuelle Bibliothek“ im Gedächtnis und die Fähigkeit, Formen im Raum zu drehen.",
        ["wie das Gedächtnis beim Zeichnen funktioniert", "Gedächtnis-Zeichnen in Stufen", "Objekte im Kopf drehen",
         "eigene Figuren, Autos und Kreaturen erfinden"])

page(head("Teil 7 · Aus dem Kopf", "Warum es nicht klappt – und wie doch",
          "Wenn du versuchst, ein Auto aus dem Kopf zu zeichnen, merkst du: Du weißt, wie es aussieht, aber nicht, wie es <i>gebaut</i> ist. Abzeichnen allein trainiert das Auge – aber nicht das Verständnis.")
     + """
<h2>Die 3 Säulen</h2>
<div class="row">
<div class="box"><b class="t">1 · Konstruktion</b>Du kannst Kugel, Kiste und Zylinder in jeder Lage zeichnen (Teil 2). Damit hast du ein „3D-Programm“ im Kopf.</div>
<div class="box"><b class="t">2 · Bibliothek</b>Du hast Motive bewusst studiert und dir gemerkt, <b>woraus</b> sie bestehen – nicht wie ein Foto aussieht.</div>
<div class="box"><b class="t">3 · Abrufen</b>Du übst regelmäßig, Gelerntes ohne Vorlage zu zeichnen – und vergleichst danach.</div>
</div>
<h2>Die Studien-Schleife</h2>
<ol>
<li><b>Studieren:</b> Zeichne ein Motiv nach Vorlage – aber analysierend: Welche Grundformen? Welche Proportionen? Notiere sie am Rand („Kopf = 1/3 Rumpf“, „Rad = 1/2 Höhe“).</li>
<li><b>Abdecken:</b> Vorlage weg, Zeichnung umdrehen.</li>
<li><b>Aus dem Gedächtnis:</b> Gleiches Motiv nochmal zeichnen.</li>
<li><b>Vergleichen:</b> Vorlage wieder holen. Kreise mit Rotstift (oder einem dicken Strich) ein, was falsch ist oder fehlte.</li>
<li><b>Wiederholen:</b> Nach 1 Tag und nach 1 Woche wieder aus dem Gedächtnis. Erst dann sitzt es.</li>
</ol>
<h2>Schreib Notizen in deine Zeichnungen</h2>
<p>Profis kritzeln ihre Studien voll mit Pfeilen und Notizen: „Licht von oben = Augen im Schatten“, „Pferdeknie zeigt nach vorne“, „Fenster ist 1/3 der Höhe“.
Was du in Worte fassen kannst, kannst du dir merken.</p>
<h2>Was du NICHT tun solltest</h2>
<ul><li>Nur abzeichnen und hoffen, dass es irgendwann von allein im Kopf ist.</li>
<li>Nur aus dem Kopf zeichnen – ohne neue Informationen wiederholst du nur deine Fehler.</li>
<li>Bei Unsicherheit zu Symbolen greifen (Mandelaugen, Strichmund). Lieber Grundformen und Konstruktion.</li></ul>
""" + mat("Fineliner oder Kugelschreiber für Gedächtnis-Übungen – kein Radieren, du siehst ehrlich, was du weißt."),
     section="Teil 7 · Aus dem Kopf")

page(head("Teil 7 · Aus dem Kopf", "Gedächtnis-Training in Stufen",
          "Fang leicht an und steigere dich. Jede Stufe kannst du mit jedem Motiv machen: Gesicht, Hand, Auto, Tier, Baum.")
     + """
<table>
<tr><th style="width:15%">Stufe</th><th style="width:28%">Was</th><th>Ablauf</th></tr>
<tr><td><b>1</b></td><td>Sofort nachzeichnen</td><td>Vorlage 1 Min anschauen, sofort ohne Vorlage zeichnen, vergleichen.</td></tr>
<tr><td><b>2</b></td><td>Kurz merken</td><td>Vorlage 30 Sek anschauen, 5 Min warten (etwas anderes tun), dann zeichnen.</td></tr>
<tr><td><b>3</b></td><td>Am nächsten Tag</td><td>Gestern studiertes Motiv heute aus dem Gedächtnis.</td></tr>
<tr><td><b>4</b></td><td>Drehen</td><td>Motiv von vorne studiert → aus dem Kopf von der Seite / oben zeichnen.</td></tr>
<tr><td><b>5</b></td><td>Verändern</td><td>Gesicht lacht statt ernst, Auto als Cabrio, Hund springt statt steht.</td></tr>
<tr><td><b>6</b></td><td>Erfinden</td><td>Komplett neues Motiv aus gelernten Bausteinen (z.&nbsp;B. ein Fantasie-Tier aus Pferd + Vogel).</td></tr>
</table>
<h2>Alltagsübungen ohne Stift</h2>
<ul>
<li><b>Bewusst schauen:</b> Im Bus ein Gesicht betrachten und überlegen: Wo liegt das Licht? Wie breit ist die Nase im Vergleich zum Augenabstand?</li>
<li><b>Gedanklich zerlegen:</b> Jedes Auto auf der Straße: Wie viele Räder lang? Wo ist die Kabine?</li>
<li><b>Abends rekapitulieren:</b> Ein Ding, das du heute gesehen hast, schnell aus dem Kopf skizzieren (2 Min).</li>
</ul>
<h2>Die 10-Dinge-Liste</h2>
<p>Schreib 10 Dinge auf, die du aus dem Kopf zeichnen können willst (z.&nbsp;B. „mein Lieblingsauto“, „Katze im Sprung“, „Hände, die etwas halten“).
Für jedes machst du die Studien-Schleife, bis du es ohne Vorlage kannst.</p>
<table>""" + "".join(f'<tr><td style="width:8mm">{i}</td><td style="height:8mm"></td><td style="width:22mm"><span class="chk"></span>kann ich</td></tr>' for i in range(1, 11))
     + "</table>", section="Teil 7 · Aus dem Kopf")

page(head("Teil 7 · Übung", "Vorlage ↔ Gedächtnis")
     + ex("Studien-Schleife", "Links: nach Vorlage, analysierend, mit Notizen. Rechts: Vorlage weg, aus dem Gedächtnis. "
          "Danach vergleichen und Fehler markieren. Motive: 1 Gesicht, 1 Auto, 1 Tier. <span class='timer'>je 10 + 10 min</span>")
     + '<div class="grow">' + S.frames(6, 2, 560, 800, ["Gesicht · nach Vorlage", "Gesicht · aus dem Gedächtnis", "Auto · nach Vorlage",
                                                      "Auto · aus dem Gedächtnis", "Tier · nach Vorlage", "Tier · aus dem Gedächtnis"]) + "</div>",
     section="Teil 7 · Aus dem Kopf")

page(head("Teil 7 · Aus dem Kopf", "Formen im Kopf drehen",
          "Die wichtigste Fähigkeit beim Zeichnen ohne Vorlage: dir vorzustellen, wie etwas von einer anderen Seite aussieht. Trainiere sie mit Würfeln – sie sind einfach zu prüfen.")
     + S.cube_rotations() + steps([
         "Zeichne einen Würfel, durchsichtig, mit allen 12 Kanten.",
         "Prüfe: Laufen die 3 Gruppen paralleler Kanten jeweils leicht zusammen (zu einem Fluchtpunkt)?",
         "Zeichne einen Zylinder <b>durch</b> den Würfel (Ellipsen auf zwei gegenüberliegenden Flächen).",
         "Verwandle Würfel in Gegenstände: Würfel → Toaster, Würfel → Kopf (Kugel einpassen), Würfel → Auto-Kabine."])
     + ex("Würfel-Rotation", "Die halb vorgegebenen Würfel im Feld unten weiterführen: Zeichne neben jeden Würfel einen weiteren, der um 30–45° weitergedreht ist. "
          "In die leeren Felder eigene gedrehte Würfel und Zylinder. <span class='timer'>15 min</span>")
     + '<div class="grow">' + S.frames(6, 3, 560, 420, guide="cube") + "</div>",
     section="Teil 7 · Aus dem Kopf")

page(head("Teil 7 · Übung", "Erfinden!",
          "Jetzt ohne jede Vorlage. Nutze nur, was du gelernt hast: Grundformen, Perspektive, Proportionen, Licht.")
     + ex("Erfinder-Blatt", "Feld 1: Ein Fantasie-Tier aus zwei echten Tieren. Feld 2: Dein Traumauto in 3/4-Ansicht. "
          "Feld 3: Eine Person in einer Aktion (kochen, Fahrrad fahren, tanzen). Feld 4: Ein Gesicht mit starkem Gefühl (Wut, Lachen, Angst). "
          "Erst Konstruktion, dann ausarbeiten. Licht von links oben. <span class='timer'>je 20 min</span>")
     + '<div class="grow">' + S.frames(4, 2, 560, 800, ["Fantasie-Tier", "Traumauto 3/4", "Person in Aktion", "Gesicht mit Gefühl"]) + "</div>",
     section="Teil 7 · Aus dem Kopf")

blank()
blank()

# =================================================================== Plan
plan = [
    ("1", "Linien-Aufwärmen + Punkte verbinden", "1"), ("2", "Tonwertskalen, Schraffur", "1"), ("3", "Kugel schattieren", "1"),
    ("4", "Würfel & Zylinder schattieren", "1"), ("5", "Formen-Wand", "2"), ("6", "1-Punkt-Perspektive: Zimmer/Flur", "2"),
    ("7", "2-Punkt: Kisten-Stadt", "2"), ("8", "Ellipsen-Leiter, Tassen", "2"), ("9", "Loomis-Kopf frontal + Profil", "3"),
    ("10", "Proportions-Check: 3 Gesichter", "3"), ("11", "Augen-Studien", "3"), ("12", "Nase & Mund", "3"),
    ("13", "Kopf-Karussell (8 Richtungen)", "3"), ("14", "Gesicht schattieren nach Foto", "3"), ("15", "Proportionen 8 Köpfe", "4"),
    ("16", "Gliederpuppe: 8 Posen", "4"), ("17", "Gesture-Session 20 min", "4"), ("18", "Hände (eigene Hand)", "4"),
    ("19", "Gesture + Leute im Café", "4"), ("20", "Auto Seitenansicht ×3", "5"), ("21", "Auto 3/4 aus Kisten", "5"),
    ("22", "Gegenstände drehen (Technik-Woche)", "5"), ("23", "Tiere aus Formen", "6"), ("24", "Bäume + Landschaft-Thumbnails", "6"),
    ("25", "Stillleben mit Lampe", "6"), ("26", "Studien-Schleife: Gesicht", "7"), ("27", "Studien-Schleife: Auto", "7"),
    ("28", "Würfel-Rotation", "7"), ("29", "Erfinder-Blatt", "7"), ("30", "Vorher/Nachher-Zeichnung", "–"),
]
rows = "".join(f'<tr><td style="width:9mm">{d}</td><td>{t}</td><td style="width:11mm;text-align:center">{p}</td>'
               f'<td style="width:18mm"></td><td style="width:8mm"><span class="chk"></span></td></tr>' for d, t, p in plan)
page(head("Trainingsplan", "30 Tage – je 20 bis 40 Minuten",
          "Vor jeder Session 5 Minuten Aufwärmen (Linien & Ellipsen). Einen Tag verpasst? Einfach weitermachen, nicht nachholen.")
     + f'<table class="small plan"><tr><th>Tag</th><th>Aufgabe</th><th>Teil</th><th>Datum</th><th>✓</th></tr>{rows}</table>'
     + "<p class='small' style='margin-top:2mm'><b>Danach:</b> Wiederhole den Plan, aber tausche jede „nach Vorlage“-Übung gegen die Gedächtnis-Version aus Teil 7.</p>",
     section="Trainingsplan")

page(head("Fortschritt", "Vorher / Nachher",
          "Zeichne <b>heute</b> (Tag 1) die drei Motive aus dem Kopf – ohne Vorlage, ohne Hilfe. Nach 30 Tagen zeichnest du sie noch einmal daneben. Nicht vorher anschauen!")
     + '<div class="grow">' + S.frames(6, 2, 560, 840, ["Tag 1 · Gesicht", "Tag 30 · Gesicht", "Tag 1 · Mensch (ganze Figur)",
                                                      "Tag 30 · Mensch (ganze Figur)", "Tag 1 · Auto", "Tag 30 · Auto"]) + "</div>",
     section="Fortschritt")

page(head("Nachschlagen", "Spickzettel",
          "Die wichtigsten Regeln auf einer Seite – zum Rausnehmen und neben das Blatt legen.") + """
<div class="row"><div>
<h2>Ablauf jeder Zeichnung</h2><ol class="small">
<li>Motiv anschauen, Augen zukneifen: große Formen?</li>
<li>Bewegungs-/Mittellinie.</li>
<li>Grundformen leicht (HB).</li>
<li>Proportionen prüfen – <b>jetzt</b> korrigieren.</li>
<li>Lichtrichtung festlegen, Schattenformen.</li>
<li>Mittelton, dann Dunkel, dann Halbtöne.</li>
<li>Details & Lichter zum Schluss.</li></ol>
<h2>Stifte</h2><ul class="small">
<li>2H/HB: Gerüst</li><li>2B: Kontur, Mittelton</li><li>4B–6B: Dunkel, Kontaktschatten</li><li>Knetgummi: Lichter</li></ul>
<h2>Licht</h2><p class="small">Glanzlicht → Licht → Halbton → Kernschatten → Reflexlicht · Schlagschatten · Kontaktschatten</p>
</div><div>
<h2>Gesicht</h2><ul class="small">
<li>Augen auf halber Kopfhöhe</li><li>Haaransatz–Braue–Nase–Kinn: 3 gleiche Teile</li>
<li>Kopf = 5 Augen breit</li><li>Ohren zwischen Braue und Nase</li><li>Mund auf 1/3 Nase–Kinn</li></ul>
<h2>Körper</h2><ul class="small">
<li>8 Köpfe groß, Schritt = Mitte</li><li>Schultern ≈ 2 Köpfe</li><li>Ellbogen = Taille, Handgelenk = Schritt</li>
<li>Hand ≈ Gesicht</li></ul>
<h2>Auto</h2><ul class="small">
<li>Länge ≈ 6–7 Räder, Höhe ≈ 2 Räder</li><li>Radstand ≈ 4 Räder</li><li>kurze Ellipsen-Achse = Radachse</li></ul>
<h2>Perspektive</h2><ul class="small">
<li>Horizont = Augenhöhe</li><li>Senkrechte bleiben senkrecht</li><li>Fluchtpunkte weit auseinander</li>
<li>Ellipsen: runde Enden, weiter vom Horizont = runder</li></ul>
</div></div>""", section="Nachschlagen")

for _ in range(6):
    blank()

html = (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Skizzenbuch</title>'
        f'<style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
with open(os.path.join(HERE, "skizzenbuch.html"), "w", encoding="utf-8") as fh:
    fh.write(html)
print(f"{state['n']} Seiten geschrieben")
