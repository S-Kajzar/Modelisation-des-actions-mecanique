#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercice 1.1 — Projections : les quatre quadrants (niveau 1), entraînement à valeurs aléatoires, page autonome.

    python3 src/construire_exercice_quadrants.py   # écrit src/exercices/quadrants-source.html et la vignette
    python3 src/generer.py                          # publie exercice-quadrants.html

Construction reprise de l'exercice « Déplacer un torseur » du dépôt Statique : séries de 5, 10, 15 ou 20 questions
tirées au hasard parmi les situations choisies (angle mesuré depuis l'axe horizontal ou vertical, quadrants 1 à 4),
page plein écran en trois colonnes (données et figure | réponse | correction pas à pas), note sur 20 en fin de série.

Chaque question donne une force F (intensité, angle α et axe de référence) ; l'élève écrit le vecteur F en colonne,
d'abord en fonction de F et de α (expression littérale, toute écriture équivalente acceptée), puis en newtons.
Une question n'est réussie que si les quatre cases sont justes à la première vérification. L'adresse ?graine=N rend
la suite de tirages reproductible (tests, même série pour toute la classe).
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commun import GABARIT, IMAGES, ROOT  # noqa: E402

SORTIE = ROOT / "src" / "exercices" / "quadrants-source.html"
HOUSE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.3" '
         'stroke-linejoin="round" stroke-linecap="round"><path d="M3 11.5 12 4l9 7.5"/>'
         '<path d="M5.5 9.8V20h4.5v-5.5h4V20h4.5V9.8"/></svg>')


def V(x):
    return f'<span class="vec">{x}</span>'


RAPPEL = ("<p><b>1. L'axe de l'angle α</b> : sur cet axe, la projection est le côté <b>adjacent</b> → F cos α ; sur "
          "l'autre axe, c'est le côté <b>opposé</b> → F sin α.</p>"
          '<div class="formule"><span class="f-main">α depuis l\'axe horizontal : ' + V("F") + " = ( ± F cos α ; ± F sin α )"
          '</span><span class="f-units">α depuis l\'axe vertical : ' + V("F") + " = ( ± F sin α ; ± F cos α )</span></div>"
          "<p><b>2. Le signe</b> se lit sur la flèche : vers la droite F<sub>x</sub> &gt; 0, vers la gauche F<sub>x</sub> "
          "&lt; 0 ; vers le haut F<sub>y</sub> &gt; 0, vers le bas F<sub>y</sub> &lt; 0.</p>"
          '<table class="qd-signes"><tr><th>Quadrant</th><td>1</td><td>2</td><td>3</td><td>4</td></tr>'
          "<tr><th>(F<sub>x</sub> ; F<sub>y</sub>)</th><td>(+ ; +)</td><td>(− ; +)</td><td>(− ; −)</td><td>(+ ; −)</td></tr>"
          "</table><p><b>3. Vérifie</b> : F<sub>x</sub>² + F<sub>y</sub>² = F².</p>")


def chips(nom, vals, type_="checkbox", coche=None):
    return "".join(f'<label class="ta-chip"><input type="{type_}" name="{nom}" value="{v}"'
                   f'{" checked" if (coche is None or v == coche) else ""}><span>{t}</span></label>' for v, t in vals)


BODY = f"""<div class="ta-app" id="qd">
<header class="ta-top">
  <div class="ta-id"><a class="ta-home no-print" href="index.html" title="Retour à l'accueil" aria-label="Retour à l'accueil">{HOUSE}</a>
    <span class="mc-tag">Exercice 1.1</span><span class="pastille">Niveau 1</span>
    <h1>Projections : les quatre quadrants</h1></div>
  <div class="ta-prog" aria-live="polite"><span>Question <b id="qd-k">1</b> / <b id="qd-N">10</b></span>
    <span class="ta-dots" id="qd-dots" aria-hidden="true"></span><span>Réussies <b id="qd-ok">0</b></span></div>
  <div class="ta-menus">
    <details class="ta-pd ta-cfg" id="qd-cfg"><summary>Série : <span id="qd-cfg-sum">10 questions</span></summary><div class="ta-pop">
      <p class="ta-pop-t">Angle α mesuré depuis l'axe</p><div class="ta-chips">{chips("qd-ref", (("h", "horizontal (x ou x')"), ("v", "vertical (y ou y')")))}</div>
      <p class="ta-pop-t">Quadrants <span class="small">(questions tirées au hasard parmi les cases cochées)</span></p>
      <div class="ta-chips">{chips("qd-q", [(str(q), f"Quadrant {q}") for q in range(1, 5)])}</div>
      <p class="ta-pop-t">Nombre de questions</p><div class="ta-chips">{chips("qd-n", [(str(n), str(n)) for n in (5, 10, 15, 20)], "radio", "10")}</div>
      <p class="ta-cfg-msg small" id="qd-cfg-msg"></p>
      <button type="button" class="btn" id="qd-go">Lancer la série</button></div></details>
    <details class="ta-pd"><summary>Rappel</summary><div class="ta-pop">{RAPPEL}</div></details>
  </div>
</header>
<main class="ta-grid" id="qd-grid">
  <section class="ta-col ta-col-don" aria-labelledby="qd-h-don"><h2 id="qd-h-don"><span>1</span> Données <em class="ta-type" id="qd-type"></em></h2>
    <p id="qd-txt"></p>
    <svg class="ta-svg" id="qd-svg" viewBox="0 0 360 320" role="img" aria-label="Repère, force F et angle α"></svg></section>
  <section class="ta-col ta-col-rep" aria-labelledby="qd-h-rep"><h2 id="qd-h-rep"><span>2</span> Ta réponse</h2>
    <p class="ta-conseil"><b>Conseil :</b> repère d'abord l'axe de l'angle α (cos sur cet axe, sin sur l'autre), puis les
    signes d'après le sens de la flèche. Calculatrice en degrés.</p>
    <div class="ta-saisie">
      <div class="ta-bloc"><h3>Le vecteur {V("F")} en fonction de F et de α</h3><div class="ta-vecin qd-lit" id="qd-lit"></div>
        <p class="qd-touches no-print"><span class="small">Insérer :</span> <button type="button" data-ins="α">α</button>
        <button type="button" data-ins="cos ">cos</button><button type="button" data-ins="sin ">sin</button>
        <button type="button" data-ins="−">−</button></p></div>
      <div class="ta-bloc"><h3>Le vecteur {V("F")} en newtons</h3><div class="ta-vecin" id="qd-num"></div></div>
    </div>
    <div class="ta-act"><button type="button" class="btn" id="qd-check" title="Touche Entrée">Vérifier</button>
      <button type="button" class="btn ghost" id="qd-sol" title="La question compte alors comme manquée">Correction</button>
      <button type="button" class="btn ta-next" id="qd-next" disabled>Question suivante ▶</button></div>
    <p class="ta-fb" id="qd-fb" aria-live="polite"></p></section>
  <section class="ta-col ta-col-cor" id="qd-col-cor" aria-labelledby="qd-h-cor"><h2 id="qd-h-cor"><span>3</span> Correction</h2>
    <p class="ta-vide small" id="qd-vide">La correction pas à pas s'affiche ici dès que ta réponse est juste, ou avec le
    bouton « Correction » (la question compte alors comme manquée). Les projections apparaissent aussi sur la figure.</p>
    <div class="ta-corr" id="qd-corr" hidden></div></section>
</main>
<section class="ta-bilan" id="qd-bilan" hidden aria-live="polite"></section>
<footer class="ta-foot small"><p>Saisie : expressions avec F et α (ou <code>a</code>), <code>cos</code>, <code>sin</code>,
le signe − ; le signe × est facultatif (<code>-F sin α</code>, <code>-F*sin(a)</code>…), toute écriture équivalente est acceptée.
Nombres décimaux avec une virgule ou un point, signe compris, arrondis au centième ; tolérance ± 0,1 % (au moins 0,05 N).
<kbd>Tab</kbd> passe à la case suivante, <kbd>Entrée</kbd> vérifie, puis passe à la question suivante. Une question n'est
réussie que si les quatre cases sont justes à la première vérification ; la note sur 20 est donnée en fin de série.</p>
<p class="no-print"><a href="cours-projection.html">Cours 2 — Projection d'une force</a> · <a href="exercice-projections.html">Exercice 1.2</a>
· <a href="index.html">Accueil</a></p></footer>
</div>"""

CSS = """<style>
/* ---------- plein écran : barre d'en-tête, puis données | réponse | correction ; la taille du texte suit l'écran ---------- */
body.ta-page{margin:0; background:var(--fond, #E3E5E0)}
.ta-page .home-back{display:none}
#qd{display:flex; flex-direction:column; min-height:calc(100dvh - 20px); padding:8px clamp(6px, 1vw, 16px) 12px;
  font-size:clamp(14.5px, .3vw + .85vh + 5px, 22px); box-sizing:border-box}
.ta-top{display:flex; flex-wrap:wrap; align-items:center; gap:6px 16px; background:var(--encre); color:#fff; padding:7px 12px; position:relative}
.ta-id{display:flex; align-items:center; gap:8px; flex-wrap:wrap}
#qd .ta-id h1{margin:0; font:800 1.2em/1.2 var(--f-titre); color:#fff}
.ta-home{display:inline-flex; color:var(--jaune)} .ta-home svg{width:22px; height:22px}
.mc-tag{display:inline-block; font:700 .72em var(--f-titre); background:var(--jaune); color:var(--encre); padding:2px 8px}
.pastille{display:inline-block; font:700 .72em var(--f-titre); background:var(--vert); color:#fff; padding:2px 8px}
.ta-prog{display:flex; align-items:center; flex-wrap:wrap; gap:4px 12px; font-size:.88em}
.ta-prog b{color:var(--jaune); font-family:var(--f-titre)}
.ta-dots{display:flex; flex-wrap:wrap; gap:3px; max-width:min(46vw, 420px)}
.ta-dots i{width:.8em; height:.8em; border-radius:50%; background:rgba(255,255,255,.22); display:inline-block}
.ta-dots i.ok{background:#3FBF6F} .ta-dots i.ko{background:#E5534B} .ta-dots i.on{outline:2px solid var(--jaune); outline-offset:1px}
.ta-menus{display:flex; gap:6px; margin-left:auto}
.ta-pd summary{cursor:pointer; list-style:none; border:1.5px solid #fff; padding:4px 10px; font:700 .86em var(--f-titre); white-space:nowrap}
.ta-pd summary::-webkit-details-marker{display:none}
.ta-pd[open] summary{background:#fff; color:var(--encre)}
.ta-cfg summary{border-color:var(--jaune)}
.ta-pop{position:absolute; right:12px; top:100%; z-index:20; width:min(600px, calc(100vw - 24px)); background:#fff; color:var(--encre);
  border:2px solid var(--encre); box-shadow:0 8px 24px rgba(0,0,0,.25); padding:8px 14px 12px; font-size:.92em}
.ta-pop p{margin:6px 0}
.ta-pop-t{font:700 .95em var(--f-titre); margin:8px 0 4px}
.ta-chips{display:flex; flex-wrap:wrap; gap:6px}
.ta-chip input{position:absolute; opacity:0; pointer-events:none}
.ta-chip span{display:inline-block; border:1.5px solid var(--encre); padding:5px 12px; font:700 .9em var(--f-titre); cursor:pointer; background:#fff}
.ta-chip input:checked+span{background:var(--encre); color:var(--jaune)}
.ta-chip input:focus-visible+span{outline:2px solid var(--bleu); outline-offset:2px}
.ta-cfg-msg{color:var(--rouge); min-height:1.2em}
.formule{display:flex; flex-wrap:wrap; gap:4px 20px; align-items:center; border:2px solid var(--rouge); background:#fff; padding:6px 12px; margin:6px 0}
.formule .f-main{font:700 1.02em var(--f-titre); line-height:1.8} .formule .f-units{font-size:.9em; color:var(--encre-2)}
.qd-signes{border-collapse:collapse; margin:4px 0} .qd-signes th,.qd-signes td{border:1px solid var(--trait-fin); padding:3px 10px; text-align:center}
.qd-signes th{font:700 .9em var(--f-titre); background:#F4F5F2}
.ta-grid{flex:1; display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.05fr) minmax(0,1fr); gap:clamp(6px, .8vw, 14px); margin-top:8px; align-items:stretch}
@media (max-width:1100px){ .ta-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr); grid-template-areas:"don rep" "cor rep"; align-items:start}
  .ta-col-don{grid-area:don} .ta-col-rep{grid-area:rep} .ta-col-cor{grid-area:cor} }
@media (max-width:700px){ .ta-grid{grid-template-columns:1fr; grid-template-areas:"don" "rep" "cor"} .ta-menus{margin-left:0} #qd{min-height:0} }
.ta-col{background:#fff; border:1px solid var(--trait-fin); padding:.5em .8em .7em; min-width:0}
.ta-col h2{display:flex; align-items:center; flex-wrap:wrap; gap:8px; font:800 1.05em var(--f-titre); margin:0 0 .4em}
.ta-col h2 span{display:inline-grid; place-items:center; width:1.4em; height:1.4em; background:var(--encre); color:var(--jaune); font-size:.85em}
.ta-type{font:700 .78em var(--f-titre); color:var(--bleu); border:1.5px solid var(--bleu); padding:1px 8px; margin-left:auto; font-style:normal}
.ta-col h3{font:700 .92em var(--f-titre); margin:.5em 0 .3em}
.ta-col p{margin:0 0 .4em}
#qd .vec{line-height:1}
.ta-svg{display:block; width:100%; height:auto; max-height:56vh; background:#fff; border:1px solid var(--trait-fin)}
.ta-svg text{font:700 14px var(--f-texte); paint-order:stroke; stroke:#fff; stroke-width:4px; stroke-linejoin:round}
.ta-svg text.qd-fond{font:800 40px var(--f-titre); stroke:none}
.ta-conseil{background:var(--jaune-pale); border-left:4px solid var(--jaune); padding:.35em .7em; font-size:.88em}
.ta-saisie{display:flex; flex-wrap:wrap; gap:.4em 1.6em; align-items:flex-start}
/* vecteur en colonne, entre parenthèses */
.vcol{display:inline-flex; align-items:center; gap:.3em; vertical-align:middle}
.vcol-b{display:inline-block; border-left:2px solid currentColor; border-right:2px solid currentColor; border-radius:1.1em / 50%; padding:.15em .55em}
.vcol-b table{border-collapse:collapse} .vcol-b td{padding:.05em .2em; text-align:center}
.vcol-b td.vl{font:600 .75em var(--f-texte); color:var(--encre-2); padding-right:.4em; text-align:right}
.ta-vecin .vcol-b{padding:.25em .6em}
.ta-f{position:relative; display:inline-flex; flex-direction:column; align-items:center; gap:2px; line-height:1.25; font-size:.8em;
  color:var(--encre-2); padding-bottom:1.15em}
.ta-f input{width:6.4em; border:1.5px dashed var(--encre-2); padding:.25em .3em; background:#fff; font:600 1.15em var(--f-texte); text-align:center}
.qd-lit .ta-f input{width:8.6em}
.ta-f input:focus{outline:2px solid var(--jaune); outline-offset:1px; border-style:solid}
.ta-f.ok input{border:2px solid var(--vert); background:var(--vert-pale)}
.ta-f.ko input{border:2px solid var(--rouge); background:var(--rouge-pale)}
.ta-att{position:absolute; bottom:0; left:0; right:0; text-align:center; font:700 .9em var(--f-texte); color:var(--vert); white-space:nowrap}
.qd-touches{margin:.2em 0 0} .qd-touches button{font:700 .85em var(--f-texte); border:1.5px solid var(--encre-2); background:#fff; padding:.1em .6em; cursor:pointer}
.qd-touches button:hover{background:var(--jaune-pale)}
.ta-act{display:flex; flex-wrap:wrap; gap:6px; margin-top:.3em}
.ta-act .btn{padding:.4em .8em; font-size:.92em}
.ta-next:not(:disabled){background:var(--vert); border-color:var(--vert)}
kbd{font:600 .72rem var(--f-texte); border:1px solid currentColor; border-radius:3px; padding:0 4px; opacity:.8}
.ta-fb{min-height:1.5em; margin:.4em 0 0; font-weight:700}
.ta-fb.ok{color:var(--vert)} .ta-fb.ko{color:var(--rouge)}
.ta-corr{border-left:4px solid var(--vert); padding:0 10px; font-size:.92em}
.ta-corr p{margin:3px 0}
.ta-corr .eq{line-height:1.8; margin:2px 0 6px}
.ta-vide{color:var(--encre-2)}
.ta-grid[hidden],.ta-bilan[hidden]{display:none}
.ta-bilan{flex:1; background:#fff; border:1px solid var(--trait-fin); margin-top:8px; padding:1em 1.4em}
.ta-bilan h2{font:800 1.4em var(--f-titre); margin:0 0 .3em}
.ta-note{font:800 2.6em var(--f-titre); color:var(--bleu); margin:.1em 0}
.ta-note small{font-size:.45em; color:var(--encre-2)} .ta-et{font-size:.55em; color:var(--jaune)}
.ta-bil-l{display:grid; grid-template-columns:repeat(auto-fill, minmax(13em, 1fr)); gap:4px 14px; padding:0; list-style:none; margin:.6em 0 1em}
.ta-bil-l li{border-left:4px solid var(--trait-fin); padding:2px 8px}
.ta-bil-l li.ok{border-color:var(--vert)} .ta-bil-l li.ko{border-color:var(--rouge)}
.ta-foot{margin-top:10px; color:var(--encre-2)}
.ta-foot p{margin:4px 0}
@media (max-width:700px){ #qd .ta-id h1{font-size:1.05em} .ta-dots{max-width:100%} .ta-menus{flex-wrap:wrap} .ta-pd summary{white-space:normal} .ta-f input{width:5.6em} .qd-lit .ta-f input{width:7.4em} }
@media print{ .ta-top{background:#fff; color:var(--encre); border:2px solid var(--encre)} #qd .ta-id h1{color:var(--encre)} .ta-menus,.ta-act{display:none} }
</style>"""

JS = r"""<script>
(function () {
  "use strict";
  var root = document.getElementById("qd"), NS = "http://www.w3.org/2000/svg", RAD = Math.PI / 180;
  function q(s) { return root.querySelector(s); }
  function qa(s) { return Array.prototype.slice.call(root.querySelectorAll(s)); }
  // ---------- tirages : suite reproductible si l'adresse porte ?graine=N (ou ?seed=N)
  var m = /[?&](?:graine|seed)=(\d+)/.exec(location.search), graine = m ? +m[1] : null;
  var rnd = Math.random;
  if (graine !== null) {
    var s = graine >>> 0;
    rnd = function () {   // mulberry32
      s = (s + 0x6D2B79F5) | 0;
      var t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function ent(a, b) { return a + Math.floor(rnd() * (b - a + 1)); }
  function fr(x, d) {
    if (Math.abs(x) < 1e-9) x = 0;
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d || 0, maximumFractionDigits: d === undefined ? 3 : d }).replace("-", "−");
  }
  function par(x, d) { return x < 0 ? "(" + fr(x, d) + ")" : fr(x, d); }

  var REF = { h: "horizontal", v: "vertical" };
  var cur = null, essai = 0, interagi = false, reussi = false;
  var serie = { refs: ["h", "v"], quads: [1, 2, 3, 4], N: 10, liste: [], k: 0, res: [] };

  function melange(t) { for (var i = t.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), x = t[i]; t[i] = t[j]; t[j] = x; } return t; }
  function lancer(refs, quads, N) {
    var combis = [];
    quads.forEach(function (qd) { refs.forEach(function (r) { combis.push([qd, r]); }); });
    serie = { refs: refs.slice(), quads: quads.slice(), N: N, liste: [], k: 0, res: [] };
    melange(combis);
    for (var i = 0; i < N; i++) serie.liste.push(combis[i % combis.length]);   // répartition équilibrée, puis ordre au hasard
    melange(serie.liste);
    q("#qd-N").textContent = N;
    q("#qd-cfg-sum").textContent = N + " questions · " + (refs.length === 2 ? "α depuis x ou y" : "α depuis " + (refs[0] === "h" ? "x" : "y")) +
      " · " + (quads.length === 4 ? "4 quadrants" : "Q" + quads.join(", Q"));
    q("#qd-bilan").hidden = true; q("#qd-grid").hidden = false;
    poser();
  }

  // ---------- une situation : quadrant, axe de l'angle, angle et intensité tirés au hasard
  function tirage(qd, ref) {
    var a; do { a = ent(10, 80); } while (a === 45);
    var F = 10 * ent(10, 99), th;
    if (ref === "h") th = { 1: a, 2: 180 - a, 3: 180 + a, 4: 360 - a }[qd];
    else th = { 1: 90 - a, 2: 90 + a, 3: 270 - a, 4: 270 + a }[qd];
    var sx = qd === 1 || qd === 4 ? 1 : -1, sy = qd <= 2 ? 1 : -1;
    var tx = ref === "h" ? "cos" : "sin", ty = ref === "h" ? "sin" : "cos";
    var axe = ref === "h" ? (sx > 0 ? "x" : "x'") : (sy > 0 ? "y" : "y'");
    var Fx = Math.round(sx * F * (tx === "cos" ? Math.cos(a * RAD) : Math.sin(a * RAD)) * 100) / 100;
    var Fy = Math.round(sy * F * (ty === "cos" ? Math.cos(a * RAD) : Math.sin(a * RAD)) * 100) / 100;
    return { q: qd, ref: ref, axe: axe, a: a, F: F, th: th, sx: sx, sy: sy, tx: tx, ty: ty, Fx: Fx, Fy: Fy };
  }

  // ---------- expressions littérales : analyse (F, α, cos, sin, tan, nombres, + − × / ^, parenthèses, produit implicite)
  function analyser(txt) {
    var s = String(txt).toLowerCase().replace(/[\s  ]/g, "").replace(/[−–]/g, "-").replace(/[×·]/g, "*")
      .replace(/,/g, ".").replace(/°/g, "");
    if (!s) return null;
    var t = [], i = 0, NOMS = ["alpha", "cos", "sin", "tan", "α", "f", "a"];
    while (i < s.length) {
      var c = s.charAt(i), mm = /^(\d+\.?\d*|\.\d+)/.exec(s.slice(i));
      if (mm) { t.push({ k: "n", v: parseFloat(mm[1]) }); i += mm[1].length; continue; }
      if ("+-*/^()".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
      var nom = null;
      for (var j = 0; j < NOMS.length; j++) if (s.substr(i, NOMS[j].length) === NOMS[j]) { nom = NOMS[j]; break; }
      if (!nom) return null;
      t.push(/^(cos|sin|tan)$/.test(nom) ? { k: "fn", v: nom } : { k: "v", v: nom === "f" ? "F" : "a" });
      i += nom.length;
    }
    var p = 0;
    function pk() { return t[p]; }
    function atomeSuit() { var x = t[p]; return x && (x.k === "n" || x.k === "v" || x.k === "fn" || x.k === "("); }
    function somme() {
      var f = produit();
      while (pk() && (pk().k === "+" || pk().k === "-")) {
        var op = t[p++].k, a = f, b = produit();
        f = op === "+" ? function (e) { return a(e) + b(e); } : function (e) { return a(e) - b(e); };
      }
      return f;
    }
    function produit() {
      var f = facteur();
      while (pk() && (pk().k === "*" || pk().k === "/" || atomeSuit())) {
        var op = pk().k === "/" ? "/" : "*";
        if (pk().k === "*" || pk().k === "/") p++;
        var a = f, b = facteur();
        f = op === "*" ? function (e) { return a(e) * b(e); } : function (e) { return a(e) / b(e); };
      }
      return f;
    }
    function facteur() {
      if (pk() && pk().k === "-") { p++; var g = facteur(); return function (e) { return -g(e); }; }
      if (pk() && pk().k === "+") { p++; return facteur(); }
      var b = atome();
      if (pk() && pk().k === "^") { p++; var ex = facteur(), bb = b; return function (e) { return Math.pow(bb(e), ex(e)); }; }
      return b;
    }
    function atome() {
      var x = t[p++];
      if (!x) throw 0;
      if (x.k === "n") return function () { return x.v; };
      if (x.k === "v") return function (e) { return e[x.v]; };
      if (x.k === "(") { var f = somme(); if (!pk() || pk().k !== ")") throw 0; p++; return f; }
      if (x.k === "fn") {
        var arg = pk() && pk().k === "-" ? facteur() : atome(), fn = Math[x.v];
        return function (e) { return fn(arg(e) * RAD); };
      }
      throw 0;
    }
    try { var f = somme(); if (p !== t.length) return null; return f; } catch (e) { return null; }
  }
  function litOk(txt, attendu) {    // attendu : fonction (F, a) ; juste si égal pour trois jeux de valeurs
    var f = analyser(txt);
    if (!f) return false;
    var jeux = [{ F: cur.F, a: cur.a }, { F: 650, a: 17 }, { F: 1300, a: 58 }];
    return jeux.every(function (e) {
      var v = f(e), w = attendu(e);
      return isFinite(v) && Math.abs(v - w) <= 1e-6 * Math.max(1, Math.abs(w));
    });
  }
  function trig(n, a) { return n === "cos" ? Math.cos(a * RAD) : Math.sin(a * RAD); }
  function litX(e) { return cur.sx * e.F * trig(cur.tx, e.a); }
  function litY(e) { return cur.sy * e.F * trig(cur.ty, e.a); }
  function litTxt(sg, fn) { return (sg < 0 ? "−" : "") + "F " + fn + " α"; }

  // ---------- affichage
  function col(vals, labels) {     // vecteur en colonne, entre parenthèses
    return '<span class="vcol"><span class="vcol-b"><table>' + vals.map(function (v, i) {
      return "<tr>" + (labels ? '<td class="vl">' + labels[i] + "</td>" : "") + "<td>" + v + "</td></tr>"; }).join("") + "</table></span></span>";
  }
  function champ(id, lab, lit) {
    return '<label class="ta-f" data-k="' + id + '"><input type="text" ' + (lit ? 'autocapitalize="off" spellcheck="false"' : 'inputmode="decimal"') +
      ' autocomplete="off" aria-label="' + lab + '"></label>';
  }
  function points() {
    q("#qd-dots").innerHTML = serie.liste.map(function (c, i) {
      var r = serie.res[i];
      return '<i class="' + (r === true ? "ok" : r === false ? "ko" : "") + (i === serie.k ? " on" : "") + '" title="Question ' + (i + 1) +
        " : quadrant " + c[0] + ", α depuis l'axe " + REF[c[1]] + '"></i>';
    }).join("");
    q("#qd-ok").textContent = serie.res.filter(function (r) { return r === true; }).length;
  }
  function poser() {
    var c = serie.liste[serie.k];
    cur = tirage(c[0], c[1]); essai = 0; reussi = false;
    q("#qd-type").textContent = "Quadrant " + cur.q + " · α depuis l'axe " + REF[cur.ref];
    q("#qd-next").disabled = true;
    q("#qd-next").textContent = serie.k === serie.N - 1 ? "Voir ma note ▶" : "Question suivante ▶";
    q("#qd-txt").innerHTML = "La force <span class=\"vec\">F</span>, d'intensité <b>F = " + fr(cur.F) + " N</b>, pointe dans le <b>quadrant " +
      cur.q + "</b>. Elle fait l'angle <b>α = " + cur.a + "°</b> avec l'axe <b>" + cur.axe + "</b> (" + REF[cur.ref] +
      "). Écris le vecteur <span class=\"vec\">F</span> dans le repère (O, x, y) : d'abord en fonction de F et de α, puis en newtons.";
    q("#qd-lit").innerHTML = '<span class="vec">F</span> = ' + col([champ("lx", "F, composante x, expression", true), champ("ly", "F, composante y, expression", true)]);
    q("#qd-num").innerHTML = '<span class="vec">F</span> = ' + col([champ("nx", "F, composante x, en newtons"), champ("ny", "F, composante y, en newtons")]) + " N";
    q("#qd-corr").hidden = true; q("#qd-vide").hidden = false; q("#qd-fb").textContent = ""; q("#qd-fb").className = "ta-fb";
    figure(false);
    q("#qd-k").textContent = serie.k + 1;
    points();
    var grid = q(".ta-grid");
    if (interagi && grid.getBoundingClientRect().top < 0) grid.scrollIntoView({ block: "start", behavior: "smooth" });
    var first = q(".ta-f input");
    if (first && (interagi || matchMedia("(min-width: 701px)").matches)) first.focus({ preventScroll: true });
  }
  function el(tag, at, par, txt) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) e.setAttribute(k, at[k]);
    if (txt != null) e.textContent = txt;
    par.appendChild(e);
    return e;
  }
  function figure(proj) {
    var svg = q("#qd-svg"), ox = 180, oy = 160, L = 118;
    svg.innerHTML = "";
    var defs = el("defs", {}, svg);
    [["k", "#1C2530", 11], ["f", "#1B7A43", 15], ["x", "#B42318", 13], ["y", "#1F5FA8", 13]].forEach(function (d) {
      var mk = el("marker", { id: "qd-m" + d[0], viewBox: "0 0 10 10", refX: "8.5", refY: "5", markerWidth: d[2], markerHeight: d[2],
        markerUnits: "userSpaceOnUse", orient: "auto" }, defs);
      el("path", { d: "M0 0 10 5 0 10z", fill: d[1] }, mk);
    });
    var coin = { 1: [300, 56], 2: [60, 56], 3: [60, 290], 4: [300, 290] }[cur.q];
    el("text", { x: coin[0], y: coin[1], fill: "#E4E7E5", "text-anchor": "middle", "class": "qd-fond" }, svg, "Q" + cur.q);
    var ax = { stroke: "#1C2530", "stroke-width": 2, "marker-end": "url(#qd-mk)" };
    [[344, oy], [16, oy], [ox, 14], [ox, 306]].forEach(function (p) { el("line", Object.assign({ x1: ox, y1: oy, x2: p[0], y2: p[1] }, ax), svg); });
    el("text", { x: 340, y: oy + 22 }, svg, "x"); el("text", { x: 12, y: oy + 22 }, svg, "x'");
    el("text", { x: ox + 10, y: 22 }, svg, "y"); el("text", { x: ox + 10, y: 312 }, svg, "y'");
    el("text", { x: ox - 18, y: oy + 20 }, svg, "O");
    var tx = ox + L * Math.cos(cur.th * RAD), ty = oy - L * Math.sin(cur.th * RAD);
    if (proj) {
      el("line", { x1: tx, y1: ty, x2: tx, y2: oy, stroke: "#7A848C", "stroke-width": 1.4, "stroke-dasharray": "5 4" }, svg);
      el("line", { x1: tx, y1: ty, x2: ox, y2: ty, stroke: "#7A848C", "stroke-width": 1.4, "stroke-dasharray": "5 4" }, svg);
      el("line", { x1: ox, y1: oy, x2: tx, y2: oy, stroke: "#B42318", "stroke-width": 5, "marker-end": "url(#qd-mx)" }, svg);
      el("line", { x1: ox, y1: oy, x2: ox, y2: ty, stroke: "#1F5FA8", "stroke-width": 5, "marker-end": "url(#qd-my)" }, svg);
      el("text", { x: (ox + tx) / 2, y: oy + (cur.sy > 0 ? 22 : -10), fill: "#B42318", "text-anchor": "middle" }, svg, "Fx");
      el("text", { x: ox + (cur.sx > 0 ? -12 : 12), y: (oy + ty) / 2 + 5, fill: "#1F5FA8", "text-anchor": cur.sx > 0 ? "end" : "start" }, svg, "Fy");
    }
    el("line", { x1: ox, y1: oy, x2: tx, y2: ty, stroke: "#1B7A43", "stroke-width": 4, "marker-end": "url(#qd-mf)" }, svg);
    var a0 = { x: 0, "x'": 180, y: 90, "y'": 270 }[cur.axe], r = 46;
    var d1 = cur.th - a0; if (d1 > 180) d1 -= 360; if (d1 < -180) d1 += 360;
    var x0 = ox + r * Math.cos(a0 * RAD), y0 = oy - r * Math.sin(a0 * RAD), x1 = ox + r * Math.cos(cur.th * RAD), y1 = oy - r * Math.sin(cur.th * RAD);
    el("path", { d: "M" + x0 + " " + y0 + " A" + r + " " + r + " 0 0 " + (d1 > 0 ? 0 : 1) + " " + x1 + " " + y1, fill: "none", stroke: "#B26A00", "stroke-width": 2.5 }, svg);
    var am = (a0 + d1 / 2) * RAD, lr = 64 + 14 * Math.abs(Math.sin(2 * am)), lx = ox + lr * Math.cos(am), ly = oy - lr * Math.sin(am);
    el("text", { x: lx, y: ly + 5, fill: "#B26A00", "text-anchor": "middle" }, svg, "α = " + cur.a + "°");
    var fx = Math.max(30, Math.min(330, ox + (L + 30) * Math.cos(cur.th * RAD))), fy = Math.max(18, Math.min(308, oy - (L + 24) * Math.sin(cur.th * RAD)));
    el("text", { x: fx, y: fy + 5, fill: "#1B7A43", "text-anchor": "middle" }, svg, "F = " + fr(cur.F) + " N");
    svg.setAttribute("aria-label", "Force F de " + cur.F + " N dans le quadrant " + cur.q + ", à " + cur.a + "° de l'axe " + cur.axe);
  }

  // ---------- correction
  function lire(inp) {
    var s = String(inp.value).replace(/[\s  ]/g, "").replace(/[−–]/g, "-").replace(",", ".").replace(/n$/i, "");
    if (!/^[+-]?(\d+\.?\d*|\.\d+)$/.test(s)) return null;
    return parseFloat(s);
  }
  function juste(k, inp) {
    if (k === "lx") return litOk(inp.value, litX);
    if (k === "ly") return litOk(inp.value, litY);
    var v = lire(inp), a = k === "nx" ? cur.Fx : cur.Fy;
    return v !== null && Math.abs(v - a) <= Math.max(0.05, Math.abs(a) * 0.001) + 1e-9;
  }
  function attendu(k) {
    return { lx: litTxt(cur.sx, cur.tx), ly: litTxt(cur.sy, cur.ty), nx: fr(cur.Fx, 2), ny: fr(cur.Fy, 2) }[k];
  }
  function verifier() {
    var bons = 0, tous = qa(".ta-f");
    tous.forEach(function (f) {
      var ok = juste(f.getAttribute("data-k"), f.querySelector("input"));
      f.classList.toggle("ok", ok); f.classList.toggle("ko", !ok); if (ok) bons++;
    });
    essai++;
    var fb = q("#qd-fb"), tout = bons === tous.length;
    fb.className = "ta-fb " + (tout ? "ok" : "ko");
    fb.textContent = tout ? "✔ Tout est juste ! Entrée : " + (serie.k === serie.N - 1 ? "voir ta note." : "question suivante.") :
      "✘ " + (tous.length - bons) + " case" + (tous.length - bons > 1 ? "s" : "") + " à revoir (en rouge) : corrige et vérifie à nouveau, ou demande la correction.";
    reussi = tout;
    if (!tout) { var ko = q(".ta-f.ko input"); if (ko) ko.focus({ preventScroll: true }); }
    if (essai === 1) compter(tout);
    if (tout) corriger();
  }
  function compter(ok) { serie.res[serie.k] = ok; q("#qd-next").disabled = false; points(); }
  function suivante() {
    if (q("#qd-next").disabled) return;
    if (serie.k < serie.N - 1) { serie.k++; poser(); } else bilan();
  }
  function bilan() {
    var ok = serie.res.filter(function (r) { return r === true; }).length, N = serie.N;
    var note = Math.round(ok / N * 40) / 2, et = note >= 18 ? "★★★" : note >= 14 ? "★★☆" : note >= 10 ? "★☆☆" : "☆☆☆";
    function compte(test) {
      var idx = serie.liste.map(function (c, i) { return test(c) ? i : -1; }).filter(function (i) { return i >= 0; });
      return idx.filter(function (i) { return serie.res[i]; }).length + " / " + idx.length;
    }
    var detail = serie.quads.map(function (qd) { return "quadrant " + qd + " : " + compte(function (c) { return c[0] === qd; }); })
      .concat(serie.refs.map(function (r) { return "α depuis l'axe " + REF[r] + " : " + compte(function (c) { return c[1] === r; }); })).join(" · ");
    q("#qd-bilan").innerHTML = "<h2>Série terminée</h2>" +
      '<p class="ta-note" id="qd-note">' + fr(note, 1) + " <small>/ 20</small> <span class=\"ta-et\">" + et + "</span></p>" +
      "<p>" + ok + " question" + (ok > 1 ? "s" : "") + " réussie" + (ok > 1 ? "s" : "") + " du premier coup sur " + N + ". " + detail + ".</p>" +
      '<ol class="ta-bil-l">' + serie.liste.map(function (c, i) {
        return '<li class="' + (serie.res[i] ? "ok" : "ko") + '">' + (serie.res[i] ? "✔ " : "✘ ") + "Q" + (i + 1) + " · quadrant " + c[0] +
          ", α / " + (c[1] === "h" ? "horizontale" : "verticale") + "</li>"; }).join("") + "</ol>" +
      '<div class="ta-act"><button type="button" class="btn" id="qd-encore">Nouvelle série (mêmes réglages)</button>' +
      '<button type="button" class="btn ghost" id="qd-regl">Changer les réglages</button></div>';
    q("#qd-grid").hidden = true; q("#qd-bilan").hidden = false;
    q("#qd-encore").addEventListener("click", function () { lancer(serie.refs, serie.quads, serie.N); });
    q("#qd-regl").addEventListener("click", function (e) { e.stopPropagation(); q("#qd-cfg").open = true; });
    q("#qd-encore").focus({ preventScroll: true });
    q("#qd-bilan").scrollIntoView({ block: "nearest" });
  }
  function corriger() {
    var c = cur, hz = c.ref === "h";
    var h = "<p><b>1. Les signes</b> : F pointe vers la " + (c.sx > 0 ? "droite" : "gauche") + " et vers le " + (c.sy > 0 ? "haut" : "bas") +
      " (quadrant " + c.q + ") : F<sub>x</sub> " + (c.sx > 0 ? "&gt;" : "&lt;") + " 0 et F<sub>y</sub> " + (c.sy > 0 ? "&gt;" : "&lt;") + " 0.</p>";
    h += "<p><b>2. Les fonctions</b> : α = " + c.a + "° est mesuré depuis l'axe " + c.axe + " (" + REF[c.ref] + "). Sur cet axe, la projection " +
      "est le côté adjacent (cos α) ; sur l'autre axe, le côté opposé (sin α) : F<sub>x</sub> s'écrit avec <b>" + c.tx + "</b>, F<sub>y</sub> avec <b>" +
      c.ty + "</b>.</p>";
    h += '<p><b>3. En fonction de F et de α</b> :</p><div class="eq"><span class="vec">F</span> = <b>' + col([litTxt(c.sx, c.tx), litTxt(c.sy, c.ty)]) + "</b></div>";
    h += '<p><b>4. En newtons</b> :</p><div class="eq"><span class="vec">F</span> = ' +
      col([(c.sx < 0 ? "−" : "") + fr(c.F) + " × " + c.tx + " " + c.a + "°", (c.sy < 0 ? "−" : "") + fr(c.F) + " × " + c.ty + " " + c.a + "°"]) +
      " = <b>" + col([fr(c.Fx, 2), fr(c.Fy, 2)]) + "</b> N</div>";
    h += "<p><b>5. Vérification</b> : √(" + par(c.Fx, 2) + "² + " + par(c.Fy, 2) + "²) ≈ " + fr(Math.hypot(c.Fx, c.Fy), 1) + " N = F. ✔</p>";
    if (!hz) h += '<p class="small">Angle mesuré depuis un axe vertical : sinus et cosinus s\'échangent par rapport au cas habituel.</p>';
    q("#qd-corr").innerHTML = h; q("#qd-corr").hidden = false; q("#qd-vide").hidden = true;
    figure(true);
    qa(".ta-f").forEach(function (f) {      // valeur attendue sous chaque case fausse ou vide
      if (f.classList.contains("ok")) return;
      if (!f.classList.contains("ko")) f.classList.add("ko");
      var att = f.querySelector(".ta-att") || f.appendChild(document.createElement("span"));
      att.className = "ta-att"; att.textContent = "→ " + attendu(f.getAttribute("data-k"));
    });
    var cc = q("#qd-col-cor"), r = cc.getBoundingClientRect();
    if (interagi && r.top > innerHeight - 80) cc.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  // ---------- événements
  var dernier = null;
  root.addEventListener("focusin", function (e) { if (e.target.closest(".qd-lit .ta-f")) dernier = e.target; });
  qa("[data-ins]").forEach(function (b) {
    b.addEventListener("mousedown", function (e) { e.preventDefault(); });
    b.addEventListener("click", function () {
      var inp = dernier || q(".qd-lit input"); if (!inp || inp.disabled) return;
      var a = inp.selectionStart == null ? inp.value.length : inp.selectionStart, z = inp.selectionEnd == null ? a : inp.selectionEnd;
      var ins = b.getAttribute("data-ins");
      inp.value = inp.value.slice(0, a) + ins + inp.value.slice(z);
      inp.focus(); inp.setSelectionRange(a + ins.length, a + ins.length);
    });
  });
  q("#qd-check").addEventListener("click", verifier);
  q("#qd-sol").addEventListener("click", function () { if (essai === 0) { essai = 1; compter(false); } corriger(); q("#qd-next").focus({ preventScroll: true }); });
  q("#qd-next").addEventListener("click", suivante);
  root.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" || !e.target.closest(".ta-f")) return;
    e.preventDefault();
    if (reussi) suivante(); else verifier();
  });
  function choix() {
    var refs = qa("[name=qd-ref]:checked").map(function (x) { return x.value; });
    var quads = qa("[name=qd-q]:checked").map(function (x) { return +x.value; });
    var N = +(q("[name=qd-n]:checked") || { value: 10 }).value;
    q("#qd-cfg-msg").textContent = !refs.length ? "Coche au moins un axe de référence." : !quads.length ? "Coche au moins un quadrant." : "";
    q("#qd-go").disabled = !refs.length || !quads.length;
    return { refs: refs, quads: quads, N: N };
  }
  qa("[name=qd-ref], [name=qd-q], [name=qd-n]").forEach(function (x) { x.addEventListener("change", choix); });
  q("#qd-go").addEventListener("click", function () { var c = choix(); if (q("#qd-go").disabled) return; q("#qd-cfg").open = false; lancer(c.refs, c.quads, c.N); });
  root.addEventListener("pointerdown", function () { interagi = true; });
  root.addEventListener("keydown", function () { interagi = true; }, true);
  document.addEventListener("click", function (e) {      // fermer les menus en cliquant ailleurs
    qa(".ta-pd").forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  qa(".ta-pd").forEach(function (d) {                      // un seul menu ouvert à la fois
    d.addEventListener("toggle", function () { if (d.open) qa(".ta-pd").forEach(function (x) { if (x !== d) x.open = false; }); });
  });
  window.__qd__ = {
    courant: function () { return cur; }, serie: function () { return serie; }, graine: graine,
    lancer: function (refs, quads, N) { lancer(refs, quads, N); },
    reponses: function () { return { lx: (cur.sx < 0 ? "-" : "") + "F*" + cur.tx + "(α)", ly: (cur.sy < 0 ? "-" : "") + "F " + cur.ty + " a",
      nx: String(cur.Fx).replace(".", ","), ny: String(cur.Fy) }; },
    analyser: function (txt, F, a) { var f = analyser(txt); return f ? f({ F: F, a: a }) : null; }
  };
  lancer(["h", "v"], [1, 2, 3, 4], 10);
})();
</script>"""


# ---------------------------------------------------------------- illustration (carte de l'accueil)
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
        out.append(f'<path d="M{x2:.1f} {y2:.1f} L{x2:.1f} {oy} M{x2:.1f} {y2:.1f} L{ox} {y2:.1f}" stroke="{couleurs[i]}" '
                   f'stroke-width="1.5" stroke-dasharray="5 4" fill="none" opacity=".7"/>')
    for q, (x, y) in zip("1234", [(0.78, 0.2), (0.22, 0.2), (0.22, 0.86), (0.78, 0.86)]):
        out.append(f'<text x="{w * x:.0f}" y="{h * y:.0f}" font-size="{h * 0.07:.0f}" fill="#C5CBC8" text-anchor="middle" '
                   f'{t}>Q{q}</text>')
    out.append("</svg>")
    return "\n".join(out)


def construire():
    (IMAGES / "carte-exercice-quadrants.svg").write_text(svg_quadrants(480, 270), encoding="utf-8")
    g = GABARIT.read_text(encoding="utf-8")
    s0 = g.index("<style>:root{")
    styles = g[s0:g.index("</head>")]
    page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page construite par src/construire_exercice_quadrants.py : ne pas modifier à la main. -->
<title>Projections : les quatre quadrants — entraînement</title>
<meta name="description" content="Entraînement à valeurs aléatoires (niveau 1) : séries de 5 à 20 questions pour projeter une force sur les axes x et y dans les quatre quadrants, vecteur écrit en colonne, correction pas à pas et note sur 20.">
{styles}{CSS}
</head>
<body class="ta-page">
{BODY}
{JS}
</body>
</html>
"""
    SORTIE.write_text(page, encoding="utf-8")
    print(f"{SORTIE.relative_to(ROOT)} : {len(page.encode('utf-8')) / 1024:.0f} Kio")


if __name__ == "__main__":
    construire()
