#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercice 1.3 — Projections : les quatre quadrants (niveau 1), entraînement à valeurs tirées au hasard.

    python3 src/construire_exercice_quadrants.py   # écrit src/exercices/quadrants-source.html et les illustrations
    python3 src/generer.py                          # publie exercice-quadrants.html

Quatre parties, une par quadrant ; dans chacune, deux forces : l'angle α est mesuré depuis l'axe horizontal (x ou x')
pour l'une, depuis l'axe vertical (y ou y') pour l'autre. Les huit situations couvrent toutes les combinaisons de
signes et de fonctions trigonométriques. Pour chaque force : F_x et F_y littérales, puis numériques.

Les intensités (100 à 990 N) et les angles (10° à 80°, jamais 45°) sont tirés à chaque chargement par le script de
configuration, qui réécrit window.__QCFG__ et remplit figures, réponses attendues et démarches avant le démarrage des
moteurs. Un tirage se rejoue avec l'adresse ?graine=N (numéro affiché sur la copie) : même sujet pour toute la classe.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commun import IMAGES, Q, ROOT, UNITE, U_N, construire_exercice, expr, num  # noqa: E402

SORTIE = ROOT / "src" / "exercices" / "quadrants-source.html"
QUADRANTS = [(1, "en haut à droite"), (2, "en haut à gauche"), (3, "en bas à gauche"), (4, "en bas à droite")]
H_LIT = ("Expression littérale avec F et α (écris F, α ou alpha), <code>*</code> pour multiplier, <code>sin(…)</code> "
         "ou <code>cos(…)</code>. Le signe compte.")
H_NUM = "Arrondir au centième. " + UNITE


def figure_vide(k):
    return (f'<figure class="q-fig quad-fig" style="max-width:340px" data-vec="{k}"><svg viewBox="0 0 320 300" role="img" '
            'style="display:block;width:100%;height:auto;background:#fff;border:1px solid #D3D8D5"></svg>'
            '<figcaption></figcaption></figure>')


def bloc(k):
    """Une force F_k : figure (remplie au chargement), puis quatre questions."""
    f = f"F<sub>{k}</sub>"
    lit = expr("f", {"f": [1, 2, 3]}, {"f": "f"})       # correcteurs provisoires : réécrits par le tirage
    return Q(sub=f"Force {f}", html=figure_vide(k), questions=[
        Q(s=f"Exprime F<sub>{k}x</sub> en fonction de {f} et de α.", h=H_LIT, g=lit, att="…", e="…"),
        Q(s=f"Exprime F<sub>{k}y</sub> en fonction de {f} et de α.", h=H_LIT, g=lit, att="…", e="…"),
        Q(s=f"Calcule F<sub>{k}x</sub>.", h=H_NUM, g=num(0, 0.01, U_N), att="…", e="…"),
        Q(s=f"Calcule F<sub>{k}y</sub>.", h=H_NUM, g=num(0, 0.01, U_N), att="…", e="…"),
    ])


PARTIES = [Q(titre=f"Quadrant {q} — {ou}", minutes=10,
             intro=f"Les deux forces de cette partie pointent <b>{ou}</b> du repère (x, y). Pour chacune, la figure donne "
                   f"son intensité et l'angle α qu'elle fait avec l'un des axes : repère bien lequel.",
             blocs=[bloc(2 * q - 1), bloc(2 * q)]) for q, ou in QUADRANTS]

METHODE = """<h3>Projeter une force dans les quatre quadrants</h3>
<ol>
<li><b>Repère l'axe de l'angle</b> α : horizontal (x ou x') ou vertical (y ou y') ?</li>
<li><b>Choisis la fonction</b> : sur l'axe de l'angle, la projection est le côté <b>adjacent</b> → F × cos α ; sur l'autre axe, c'est le côté <b>opposé</b> → F × sin α.</li>
<li><b>Choisis le signe</b> d'après le sens de la flèche : vers la droite F<sub>x</sub> &gt; 0, vers la gauche F<sub>x</sub> &lt; 0 ; vers le haut F<sub>y</sub> &gt; 0, vers le bas F<sub>y</sub> &lt; 0.</li>
<li><b>Signes par quadrant</b> (F<sub>x</sub> ; F<sub>y</sub>) : quadrant 1 (+ ; +), quadrant 2 (− ; +), quadrant 3 (− ; −), quadrant 4 (+ ; −).</li>
<li><b>Vérifie</b> : F<sub>x</sub>² + F<sub>y</sub>² = F², et la plus grande coordonnée est sur l'axe dont la force est la plus proche.</li>
</ol>"""

# ---------------------------------------------------------------- tirage, figures et corrections (navigateur)
TIRAGE_JS = r"""(function () {
  "use strict";
  // ---- tirage reproductible : ?graine=N rejoue le même sujet
  var m = /[?&]graine=(\d+)/.exec(location.search);
  var graine = m ? +m[1] : 10000 + Math.floor(Math.random() * 90000);
  var s = graine >>> 0;
  function hasard() {                                     // mulberry32
    s = (s + 0x6D2B79F5) | 0;
    var t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  function entier(a, b) { return a + Math.floor(hasard() * (b - a + 1)); }
  function fr(x, d) {
    if (Math.abs(x) < 0.5 * Math.pow(10, -d)) x = 0;
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace("-", "−");
  }
  // ---- huit situations : quadrant, axe de l'angle et son orientation (en degrés, sens trigonométrique)
  // h : angle mesuré depuis l'axe horizontal ; dir : sens de rotation de l'axe de référence vers F
  var AXES = { x: 0, y: 90, "x'": 180, "y'": 270 };
  var SITU = [[1, "x", 1], [1, "y", -1], [2, "x'", -1], [2, "y", 1], [3, "x'", 1], [3, "y'", -1], [4, "x", -1], [4, "y'", 1]];
  var forces = [];
  for (var q = 0; q < 4; q++) {
    var paire = [SITU[2 * q], SITU[2 * q + 1]];
    if (hasard() < 0.5) paire.reverse();                  // l'axe horizontal n'est pas toujours le premier
    var a1 = 0, a2 = 0;
    while (a1 === 45 || a1 === 0) a1 = entier(10, 80);
    while (a2 === 45 || a2 === 0 || Math.abs(a2 - a1) < 8) a2 = entier(10, 80);
    [a1, a2].forEach(function (a, i) {
      var sit = paire[i], ref = sit[1], th = AXES[ref] + sit[2] * a;
      forces.push({ q: sit[0], ref: ref, h: ref.charAt(0) === "x", a: a, F: 10 * entier(10, 99), th: th });
    });
  }
  // ---- figures
  var NS = "http://www.w3.org/2000/svg";
  function el(tag, at, par, txt) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) e.setAttribute(k, at[k]);
    if (txt != null) e.textContent = txt;
    par.appendChild(e);
    return e;
  }
  var R = Math.PI / 180;
  function dessiner(svg, f, k) {
    var ox = 160, oy = 150, L = 112, id = "flq" + k;
    var defs = el("defs", {}, svg), mk = el("marker", { id: id, viewBox: "0 0 10 10", refX: "8.5", refY: "5",
      markerWidth: "11", markerHeight: "11", markerUnits: "userSpaceOnUse", orient: "auto" }, defs);
    el("path", { d: "M0 0 10 5 0 10z", fill: "#1C2530" }, mk);
    var mkF = el("marker", { id: id + "f", viewBox: "0 0 10 10", refX: "8.5", refY: "5", markerWidth: "15",
      markerHeight: "15", markerUnits: "userSpaceOnUse", orient: "auto" }, defs);
    el("path", { d: "M0 0 10 5 0 10z", fill: "#1B7A43" }, mkF);
    var pos = { 1: [250, 40], 2: [70, 40], 3: [70, 268], 4: [250, 268] };
    el("text", { x: pos[f.q][0], y: pos[f.q][1], "font-size": "13", fill: "#9AA2A8", "text-anchor": "middle",
      "font-family": "system-ui, sans-serif" }, svg, "quadrant " + f.q);
    var ax = { stroke: "#1C2530", "stroke-width": "2", "marker-end": "url(#" + id + ")" };
    el("line", Object.assign({ x1: ox, y1: oy, x2: 300, y2: oy }, ax), svg);
    el("line", Object.assign({ x1: ox, y1: oy, x2: 20, y2: oy }, ax), svg);
    el("line", Object.assign({ x1: ox, y1: oy, x2: ox, y2: 16 }, ax), svg);
    el("line", Object.assign({ x1: ox, y1: oy, x2: ox, y2: 284 }, ax), svg);
    var lab = { "font-size": "16", "font-weight": "700", fill: "#1C2530", "font-family": "system-ui, sans-serif" };
    el("text", Object.assign({ x: 300, y: oy + 22 }, lab), svg, "x");
    el("text", Object.assign({ x: 10, y: oy + 22 }, lab), svg, "x'");
    el("text", Object.assign({ x: ox + 10, y: 22 }, lab), svg, "y");
    el("text", Object.assign({ x: ox + 10, y: 292 }, lab), svg, "y'");
    el("text", Object.assign({ x: ox - 18, y: oy + 20 }, lab), svg, "O");
    var tx = ox + L * Math.cos(f.th * R), ty = oy - L * Math.sin(f.th * R);
    el("line", { x1: ox, y1: oy, x2: tx, y2: ty, stroke: "#1B7A43", "stroke-width": "4", "marker-end": "url(#" + id + "f)" }, svg);
    var a0 = AXES[f.ref], r = 46, x0 = ox + r * Math.cos(a0 * R), y0 = oy - r * Math.sin(a0 * R);
    var x1 = ox + r * Math.cos(f.th * R), y1 = oy - r * Math.sin(f.th * R), sweep = f.th > a0 ? 0 : 1;
    el("path", { d: "M" + x0 + " " + y0 + " A" + r + " " + r + " 0 0 " + sweep + " " + x1 + " " + y1,
      fill: "none", stroke: "#B26A00", "stroke-width": "2.5" }, svg);
    var am = (a0 + f.th) / 2, lx = ox + 72 * Math.cos(am * R), ly = oy - 72 * Math.sin(am * R);
    el("text", Object.assign({ x: lx, y: ly + 5, "text-anchor": "middle", fill: "#B26A00" }, lab), svg, "α = " + f.a + "°");
    var fx = ox + (L + 26) * Math.cos(f.th * R), fy = oy - (L + 26) * Math.sin(f.th * R);
    el("text", Object.assign({ x: fx, y: fy + 5, "text-anchor": "middle", fill: "#1B7A43" }, lab), svg, "F" + k);
    svg.setAttribute("aria-label", "Force F" + k + " de " + f.F + " N dans le quadrant " + f.q + ", à " + f.a +
      "° de l'axe " + f.ref);
  }
  // ---- corrections et correcteurs
  var NOMS = { f: "f", "α": "alpha", alpha: "alpha", a: "alpha" };
  function essais(f) { var t = [17, 58, 71].filter(function (x) { return x !== f.a; }).slice(0, 2); return [f.a].concat(t); }
  forces.forEach(function (f, i) {
    var k = i + 1, p = Math.floor(i / 2) + 1, n0 = (i % 2) * 4;
    var Fx = f.F * Math.cos(f.th * R), Fy = f.F * Math.sin(f.th * R);
    var sx = Fx > 0 ? 1 : -1, sy = Fy > 0 ? 1 : -1;
    var trigX = f.h ? "cos" : "sin", trigY = f.h ? "sin" : "cos";
    var fig = document.querySelector('figure[data-vec="' + k + '"]');
    dessiner(fig.querySelector("svg"), f, k);
    fig.querySelector("figcaption").innerHTML = "F<sub>" + k + "</sub> = " + f.F + " N ; α = " + f.a + "°, mesuré depuis l'axe " +
      (f.h ? "horizontal " : "vertical ") + f.ref + ".";
    var Fk = "F<sub>" + k + "</sub>", nomX = "F<sub>" + k + "x</sub>", nomY = "F<sub>" + k + "y</sub>";
    var axe = "L'angle α = " + f.a + "° est mesuré depuis l'axe " + (f.h ? "horizontal " : "vertical ") + f.ref +
      " : sur cet axe, la projection est le côté adjacent (cos α) ; sur l'autre axe, c'est le côté opposé (sin α). ";
    var signes = "F" + k + " pointe vers la " + (sx > 0 ? "droite" : "gauche") + " et vers le " + (sy > 0 ? "haut" : "bas") +
      " (quadrant " + f.q + ") : " + nomX + (sx > 0 ? " &gt; 0" : " &lt; 0") + " et " + nomY + (sy > 0 ? " &gt; 0. " : " &lt; 0. ");
    function litt(sg, trig) { return (sg < 0 ? "−" : "") + Fk + " × " + trig + " α"; }
    var vx = Math.round(Fx * 100) / 100, vy = Math.round(Fy * 100) / 100;
    var Q = [
      { g: { type: "expr", expected: (sx < 0 ? "-" : "") + "f*" + trigX + "(alpha)", vars: { f: [f.F, 650, 1300], alpha: essais(f) }, names: NOMS },
        att: nomX + " = " + litt(sx, trigX), e: axe + signes + "D'où <b>" + nomX + " = " + litt(sx, trigX) + "</b>." },
      { g: { type: "expr", expected: (sy < 0 ? "-" : "") + "f*" + trigY + "(alpha)", vars: { f: [f.F, 650, 1300], alpha: essais(f) }, names: NOMS },
        att: nomY + " = " + litt(sy, trigY), e: axe + signes + "D'où <b>" + nomY + " = " + litt(sy, trigY) + "</b>." },
      { g: { type: "num", value: vx, absTol: 0.01, unit: { label: "N", accept: ["n", "newton", "newtons"] } },
        att: nomX + " ≈ " + fr(vx, 2) + " N",
        e: nomX + " = " + (sx < 0 ? "−" : "") + f.F + " × " + trigX + "(" + f.a + "°) ≈ <b>" + fr(vx, 2) + " N</b>." },
      { g: { type: "num", value: vy, absTol: 0.01, unit: { label: "N", accept: ["n", "newton", "newtons"] } },
        att: nomY + " ≈ " + fr(vy, 2) + " N",
        e: nomY + " = " + (sy < 0 ? "−" : "") + f.F + " × " + trigY + "(" + f.a + "°) ≈ <b>" + fr(vy, 2) + " N</b>. " +
           "Vérification : √(" + fr(vx, 2) + "² + " + fr(vy, 2) + "²) ≈ " + fr(Math.hypot(vx, vy), 2) + " N ≈ " + Fk + "." }
    ];
    Q.forEach(function (x, j) {
      var id = "q" + p + "_" + (n0 + j + 1), root = document.getElementById(id);
      window.__QCFG__[id].grader = x.g;
      root.querySelector(".q-expected").innerHTML = "<span>Réponse attendue :</span> " + x.att;
      root.querySelector(".q-why").innerHTML = "<p>" + x.e + "</p>";
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-graine]"), function (e) { e.textContent = graine; });
  Array.prototype.forEach.call(document.querySelectorAll("a.lien-graine"), function (a) { a.href = "?graine=" + graine; });
  window.__tirage__ = { graine: graine, forces: forces };
})();"""


# ---------------------------------------------------------------- illustrations (accueil et carte)
def svg_quadrants(w, h, legende=True):
    """Repère et quatre forces, une par quadrant, angles de référence alternés."""
    ox, oy = w / 2, h / 2 + (8 if legende else 0)
    L = min(w, h) * 0.36
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<rect width="{w}" height="{h}" fill="#fff"/>',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="12" markerHeight="12" '
           'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 10 5 0 10z" fill="#1C2530"/></marker>']
    couleurs = ["#1B7A43", "#1F5FA8", "#B42318", "#B26A00"]
    for i, c in enumerate(couleurs):
        out.append(f'<marker id="f{i}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="18" markerHeight="18" '
                   f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 10 5 0 10z" fill="{c}"/></marker>')
    out.append("</defs>")
    ax = 'stroke="#1C2530" stroke-width="2.5" marker-end="url(#a)"'
    out += [f'<line x1="{ox}" y1="{oy}" x2="{w - 18}" y2="{oy}" {ax}/>', f'<line x1="{ox}" y1="{oy}" x2="18" y2="{oy}" {ax}/>',
            f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="14" {ax}/>', f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{h - 14}" {ax}/>']
    t = 'font-family="Arial, sans-serif" font-weight="700"'
    out += [f'<text x="{w - 30}" y="{oy + 24}" font-size="20" {t}>x</text>', f'<text x="14" y="{oy + 24}" font-size="20" {t}>x\'</text>',
            f'<text x="{ox + 10}" y="28" font-size="20" {t}>y</text>', f'<text x="{ox + 10}" y="{h - 16}" font-size="20" {t}>y\'</text>']
    for i, (th, ref) in enumerate([(35, 0), (180 - 55, 180), (180 + 30, 180), (270 + 40, 270)]):
        x2, y2 = ox + L * math.cos(math.radians(th)), oy - L * math.sin(math.radians(th))
        out.append(f'<line x1="{ox}" y1="{oy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{couleurs[i]}" stroke-width="5" '
                   f'marker-end="url(#f{i})"/>')
        r = L * 0.36
        xa, ya = ox + r * math.cos(math.radians(ref)), oy - r * math.sin(math.radians(ref))
        xb, yb = ox + r * math.cos(math.radians(th)), oy - r * math.sin(math.radians(th))
        sw = 0 if th > ref else 1
        out.append(f'<path d="M{xa:.1f} {ya:.1f} A{r:.1f} {r:.1f} 0 0 {sw} {xb:.1f} {yb:.1f}" fill="none" '
                   f'stroke="{couleurs[i]}" stroke-width="2.5"/>')
        # projections en pointillés
        out.append(f'<path d="M{x2:.1f} {y2:.1f} L{x2:.1f} {oy} M{x2:.1f} {y2:.1f} L{ox} {y2:.1f}" stroke="{couleurs[i]}" '
                   f'stroke-width="1.5" stroke-dasharray="5 4" fill="none" opacity=".7"/>')
    for q, (x, y) in zip("1234", [(0.78, 0.2), (0.22, 0.2), (0.22, 0.86), (0.78, 0.86)]):
        out.append(f'<text x="{w * x:.0f}" y="{h * y:.0f}" font-size="{h * 0.07:.0f}" fill="#C5CBC8" text-anchor="middle" '
                   f'{t}>Q{q}</text>')
    out.append("</svg>")
    return "\n".join(out)


def construire():
    (IMAGES / "carte-exercice-quadrants.svg").write_text(svg_quadrants(480, 270), encoding="utf-8")
    (IMAGES / "sequence" / "quadrants.svg").write_text(svg_quadrants(900, 480), encoding="utf-8")
    consigne = ("<p><strong>Valeurs tirées au hasard</strong> : intensités et angles changent à chaque chargement. "
                "Tirage n° <b data-graine></b> ; pour refaire exactement le même sujet, garde le lien "
                "<a class=\"lien-graine\" href=\"?\">de ce tirage</a>. Pour un nouveau sujet : <a href=\"?\">nouveau "
                "tirage</a>.</p>"
                "<p><strong>Les unités sont notées</strong> : la valeur vaut la moitié des points, l'unité l'autre moitié. "
                "<strong>Les expressions littérales</strong> s'écrivent avec F et α, par exemple <code>-F*sin(α)</code> ; "
                "toute écriture équivalente est acceptée.</p>")
    construire_exercice(
        titre="Projections : les quatre quadrants", script="construire_exercice_quadrants.py", sortie=SORTIE,
        parties=PARTIES, nq_attendu=32, config_js=TIRAGE_JS, consignes=(consigne,),
        description="Entraînement à la projection d'une force sur les axes x et y : huit forces réparties dans les quatre "
                    "quadrants, angle mesuré depuis l'axe horizontal ou vertical, nouvelles valeurs à chaque tirage.",
        sous_titre="S'entraîner à projeter une force sur x et y dans les quatre quadrants : huit forces, l'angle mesuré "
                   "tantôt depuis l'axe horizontal, tantôt depuis l'axe vertical. Intensités et angles changent à chaque "
                   "chargement : recommence autant de fois que tu veux.",
        cartouche="32 questions notées sur 8 forces (2 par quadrant), réparties en 4 parties. Tirage n° "
                  "<b data-graine></b>.",
        methode_titre="projeter dans les quatre quadrants", methode=METHODE,
        hero=Q(f="sequence/quadrants.svg", alt="Repère x, y avec une force dans chacun des quatre quadrants et ses projections",
               cap="Une force par quadrant : chaque quadrant a ses signes, chaque axe de référence sa fonction."),
        facts=[("4 quadrants", "8 forces, 32 questions"), ("40 min", "durée conseillée, qui fixe la pondération"),
               ("1 document", "méthode, en mode entraînement"), ("∞ tirages", "nouvelles valeurs à chaque chargement")])


if __name__ == "__main__":
    construire()
