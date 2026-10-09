/* ===================== COURS INTERACTIFS : comportements communs et simulateurs =====================
   Chaque bloc s'initialise seulement s'il est présent dans la page (data-widget="…"). Aucune dépendance externe. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var RAD = Math.PI / 180;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  // nombre au format français, sans « −0 »
  function fr(x, d) {
    if (d == null) d = 2;
    if (Math.abs(x) < 0.5 * Math.pow(10, -d)) x = 0;
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace("-", "−");
  }
  // nombre « naturel » : au plus d décimales, zéros inutiles retirés
  function frn(x, d) {
    if (d == null) d = 3;
    if (Math.abs(x) < 0.5 * Math.pow(10, -d)) x = 0;
    return x.toLocaleString("fr-FR", { maximumFractionDigits: d }).replace("-", "−");
  }
  function par(x, d) { var s = frn(x, d); return x < 0 && Math.abs(x) >= 0.5 * Math.pow(10, -(d == null ? 3 : d)) ? "(" + s + ")" : s; }
  function lireNombre(s) {
    s = String(s).replace(/[−–]/g, "-").replace(/\s/g, "").replace(",", ".");
    var m = s.match(/-?\d+(?:\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }
  function el(tag, attrs, parent, txt) {
    var e = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (txt != null) e.textContent = txt;
    if (parent) parent.appendChild(e);
    return e;
  }
  function attr(e, a) { Object.keys(a).forEach(function (k) { e.setAttribute(k, a[k]); }); return e; }
  function fleche(svg, id, couleur) {
    var defs = $("defs", svg) || el("defs", {}, svg);
    var m = el("marker", { id: id, viewBox: "0 0 10 10", refX: "8.5", refY: "5", markerWidth: "7", markerHeight: "7",
      orient: "auto-start-reverse", markerUnits: "userSpaceOnUse" }, defs);
    attr(m, { markerWidth: "14", markerHeight: "14" });
    el("path", { d: "M0 0 10 5 0 10z", fill: couleur }, m);
    return "url(#" + id + ")";
  }
  function pointSvg(svg, evt) {
    var p = svg.createSVGPoint();
    p.x = evt.clientX; p.y = evt.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }
  // point déplaçable à la souris, au doigt ou au clavier (flèches)
  function deplacable(svg, g, onMove, onKey) {
    var actif = false;
    g.addEventListener("pointerdown", function (e) { actif = true; g.setPointerCapture(e.pointerId); e.preventDefault(); });
    g.addEventListener("pointermove", function (e) { if (actif) onMove(pointSvg(svg, e)); });
    g.addEventListener("pointerup", function () { actif = false; });
    g.addEventListener("pointercancel", function () { actif = false; });
    g.addEventListener("keydown", function (e) {
      var d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
      if (d && onKey) { e.preventDefault(); onKey(d[0], d[1]); }
    });
  }
  function poignee(svg, label, couleur, r) {
    var g = el("g", { "class": "g-pt", tabindex: "0", role: "slider", "aria-label": label }, svg);
    el("circle", { "class": "h", r: 18 }, g);
    el("circle", { "class": "v", r: r || 7, fill: couleur || "#fff" }, g);
    return g;
  }
  function placer(g, x, y) { g.setAttribute("transform", "translate(" + x + " " + y + ")"); }
  function arc(cx, cy, r, a0, a1) {           // angles en degrés, sens trigonométrique, repère SVG (y vers le bas)
    var x0 = cx + r * Math.cos(a0 * RAD), y0 = cy - r * Math.sin(a0 * RAD);
    var x1 = cx + r * Math.cos(a1 * RAD), y1 = cy - r * Math.sin(a1 * RAD);
    var large = Math.abs(a1 - a0) > 180 ? 1 : 0, sweep = a1 > a0 ? 0 : 1;
    return "M" + x0.toFixed(1) + " " + y0.toFixed(1) + " A" + r + " " + r + " 0 " + large + " " + sweep + " " + x1.toFixed(1) + " " + y1.toFixed(1);
  }

  // ===================== barre de lecture et navigation =====================
  var barre = $(".lecture");
  if (barre) {
    var maj = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      barre.style.width = (h > 0 ? clamp(scrollY / h, 0, 1) * 100 : 0) + "%";
    };
    addEventListener("scroll", maj, { passive: true }); maj();
  }
  var liens = $$(".cours-nav a");
  if (liens.length && "IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        liens.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    liens.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) obs.observe(s); });
  }

  // ===================== quiz =====================
  $$(".quiz-bloc").forEach(function (root) {
    var qs = $$(".quiz-q", root);
    function score() {
      var n = qs.filter(function (f) { return f.classList.contains("is-ok"); }).length;
      var fait = qs.filter(function (f) { return f.classList.contains("done"); }).length;
      $(".qz-score", root).textContent = n + " / " + qs.length;
      var et = n === qs.length ? 3 : n >= qs.length - 2 ? 2 : n >= qs.length / 2 ? 1 : 0;
      $(".qz-stars", root).textContent = fait === qs.length ? "★★★".slice(0, et) + "☆☆☆".slice(0, 3 - et) : "";
      $(".qz-msg", root).textContent = fait < qs.length ? (qs.length - fait) + " question(s) restante(s)" :
        (et === 3 ? "Parfait : tu maîtrises ce cours." : et === 2 ? "Très bien : relis la correction des erreurs."
          : "Relis les parties du cours concernées, puis recommence.");
    }
    qs.forEach(function (fs) {
      fs.addEventListener("change", function (e) {
        if (fs.classList.contains("done")) return;
        var ok = e.target.value === fs.getAttribute("data-ok");
        fs.classList.add("done", ok ? "is-ok" : "is-ko");
        $(".quiz-fb", fs).textContent = ok ? "✔ Bonne réponse !" : "✘ Pas tout à fait.";
        $(".quiz-why", fs).hidden = false;
        $$("input", fs).forEach(function (i) {
          i.disabled = true;
          if (i.value === fs.getAttribute("data-ok")) i.parentNode.classList.add("good");
        });
        score();
      });
    });
    $(".qz-reset", root).addEventListener("click", function () {
      qs.forEach(function (fs) {
        fs.classList.remove("done", "is-ok", "is-ko");
        $(".quiz-fb", fs).textContent = "";
        $(".quiz-why", fs).hidden = true;
        $$("input", fs).forEach(function (i) { i.disabled = false; i.checked = false; i.parentNode.classList.remove("good"); });
      });
      score();
    });
    score();
  });

  // ===================== textes à trous =====================
  $$(".trous").forEach(function (root) {
    var sels = $$("select", root), out = $(".trous-s", root);
    function verifier() {
      var n = 0;
      sels.forEach(function (s) {
        var ok = s.value === s.getAttribute("data-ok");
        s.classList.toggle("ok", ok); s.classList.toggle("ko", !ok && s.value !== "");
        if (ok) n++;
      });
      out.textContent = n === sels.length ? "✔ Tout est juste !" : n + " / " + sels.length + " juste(s) : corrige les cases en rouge.";
    }
    $(".trous-ok", root).addEventListener("click", verifier);
    $(".trous-sol", root).addEventListener("click", function () {
      sels.forEach(function (s) { s.value = s.getAttribute("data-ok"); });
      verifier();
    });
    sels.forEach(function (s) { s.addEventListener("change", function () { s.classList.remove("ok", "ko"); out.textContent = ""; }); });
  });

  // ===================== cartes à retourner =====================
  $$(".carte").forEach(function (b) {
    b.addEventListener("click", function () { b.setAttribute("aria-expanded", b.getAttribute("aria-expanded") === "true" ? "false" : "true"); });
  });

  // ===================== vérifications rapides =====================
  $$(".check").forEach(function (root) {
    var inp = $("input", root), fb = $(".check-fb", root), essais = 0;
    var ans = parseFloat(root.getAttribute("data-ans")), tol = parseFloat(root.getAttribute("data-tol") || "0.01");
    function test() {
      var v = lireNombre(inp.value);
      if (v === null) { fb.textContent = "Saisis un nombre."; return; }
      essais++;
      var ok = Math.abs(v - ans) <= tol + 1e-9;
      root.classList.toggle("is-ok", ok); root.classList.toggle("is-ko", !ok);
      fb.innerHTML = ok ? "✔ " + root.getAttribute("data-why") :
        (essais >= 2 ? "✘ La réponse : " + root.getAttribute("data-why") : "✘ Pas encore : vérifie ton calcul et réessaie.");
    }
    $("button", root).addEventListener("click", test);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); test(); } });
  });

  // ===================== exemples pas à pas =====================
  $$(".stepper").forEach(function (root) {
    var items = $$("ol>li", root), n = 1;
    function show() {
      items.forEach(function (li, i) { li.hidden = i >= n; });
      $(".st-next", root).disabled = n >= items.length;
    }
    $(".st-next", root).addEventListener("click", function () { n = Math.min(items.length, n + 1); show(); });
    $(".st-all", root).addEventListener("click", function () { n = items.length; show(); });
    $(".st-reset", root).addEventListener("click", function () { n = 1; show(); });
    show();
  });

  // ===================== impression : réponses « À toi » visibles =====================
  var ouverts = [];
  addEventListener("beforeprint", function () {
    ouverts = $$("details.a-toi").map(function (d) { var o = d.open; d.open = true; return o; });
  });
  addEventListener("afterprint", function () { $$("details.a-toi").forEach(function (d, i) { d.open = !!ouverts[i]; }); });
  $$(".cours-print").forEach(function (b) { b.addEventListener("click", function () { window.print(); }); });

  // ===================== carte des disciplines de la mécanique =====================
  $$('[data-widget="disciplines"]').forEach(function (root) {
    var svg = $("svg", root);
    $$(".carte-btn", root).forEach(function (b) {
      b.addEventListener("click", function () {
        var d = b.getAttribute("data-d");
        svg.classList.add("choix");
        $$(".carte-btn", root).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        $$(".lien", svg).forEach(function (l) { l.classList.toggle("on", (" " + l.getAttribute("data-d") + " ").indexOf(" " + d + " ") >= 0); });
        $$(".noeud", svg).forEach(function (n) { n.classList.toggle("on", (" " + n.getAttribute("data-d") + " ").indexOf(" " + d + " ") >= 0); });
        $$(".disc", svg).forEach(function (t) { t.classList.toggle("on", t.getAttribute("data-d") === d); });
        $$(".carte-txt p", root).forEach(function (p) { p.hidden = p.getAttribute("data-d") !== d; });
      });
    });
  });

  // ===================== vecteur AB dans un repère =====================
  $$('[data-widget="repere"]').forEach(function (root) {
    var svg = $("svg", root), U = 30, OX = 50, OY = 290, XM = 12, YM = 8;
    var P = { A: { x: 1, y: 1 }, B: { x: 6, y: 5 } }, defiFait = false;
    function X(x) { return OX + U * x; }
    function Y(y) { return OY - U * y; }
    var mk = fleche(svg, "fl-rep", "#1C2530"), mkV = fleche(svg, "fl-rep-v", "#1F5FA8"),
        mkR = fleche(svg, "fl-rep-r", "#B42318"), mkB = fleche(svg, "fl-rep-b", "#1B7A43");
    var gr = el("g", { "class": "g-grille" }, svg), i;
    for (i = 0; i <= XM; i++) el("line", { x1: X(i), y1: Y(0), x2: X(i), y2: Y(YM) }, gr);
    for (i = 0; i <= YM; i++) el("line", { x1: X(0), y1: Y(i), x2: X(XM), y2: Y(i) }, gr);
    el("line", { x1: X(0) - 14, y1: OY, x2: X(XM) + 14, y2: OY, "class": "g-axe", "marker-end": mk }, svg);
    el("line", { x1: OX, y1: Y(0) + 14, x2: OX, y2: Y(YM) - 14, "class": "g-axe", "marker-end": mk }, svg);
    el("text", { x: X(XM) + 6, y: OY + 20, "class": "g-lab" }, svg, "x");
    el("text", { x: OX + 8, y: Y(YM) - 4, "class": "g-lab" }, svg, "y");
    el("text", { x: OX - 16, y: OY + 18, "class": "g-lab" }, svg, "O");
    el("line", { x1: OX, y1: OY, x2: X(1), y2: OY, stroke: "#B42318", "stroke-width": 3, "marker-end": mkR }, svg);
    el("line", { x1: OX, y1: OY, x2: OX, y2: Y(1), stroke: "#1B7A43", "stroke-width": 3, "marker-end": mkB }, svg);
    el("text", { x: X(0.45), y: OY + 18, "class": "g-lab-s", fill: "#B42318" }, svg, "i");
    el("text", { x: OX - 14, y: Y(0.55), "class": "g-lab-s" }, svg, "j");
    for (i = 1; i <= XM; i++) el("text", { x: X(i), y: OY + 16, "class": "g-lab-s", "text-anchor": "middle" }, svg, i % 2 ? "" : String(i));
    for (i = 2; i <= YM; i += 2) el("text", { x: OX - 8, y: Y(i) + 4, "class": "g-lab-s", "text-anchor": "end" }, svg, String(i));
    var cH = el("line", { stroke: "#B42318", "stroke-width": 2.5, "stroke-dasharray": "6 4" }, svg);
    var cV = el("line", { stroke: "#1B7A43", "stroke-width": 2.5, "stroke-dasharray": "6 4" }, svg);
    var tH = el("text", { "class": "g-lab-s", fill: "#B42318", "text-anchor": "middle" }, svg);
    var tV = el("text", { "class": "g-lab-s", fill: "#1B7A43" }, svg);
    var vec = el("line", { stroke: "#1F5FA8", "stroke-width": 4, "marker-end": mkV }, svg);
    var hA = poignee(svg, "Point A", "#fff"), hB = poignee(svg, "Point B", "#F2B705");
    var lA = el("text", { "class": "g-lab" }, svg, "A"), lB = el("text", { "class": "g-lab" }, svg, "B");
    function rendu() {
      var a = P.A, b = P.B, dx = b.x - a.x, dy = b.y - a.y, n = Math.sqrt(dx * dx + dy * dy);
      placer(hA, X(a.x), Y(a.y)); placer(hB, X(b.x), Y(b.y));
      attr(lA, { x: X(a.x) - 18, y: Y(a.y) + 18 }); attr(lB, { x: X(b.x) + 10, y: Y(b.y) - 10 });
      attr(cH, { x1: X(a.x), y1: Y(a.y), x2: X(b.x), y2: Y(a.y) });
      attr(cV, { x1: X(b.x), y1: Y(a.y), x2: X(b.x), y2: Y(b.y) });
      attr(tH, { x: (X(a.x) + X(b.x)) / 2, y: Y(a.y) + (dy >= 0 ? 18 : -8) }); tH.textContent = dx ? frn(dx) + " i" : "";
      attr(tV, { x: X(b.x) + 8, y: (Y(a.y) + Y(b.y)) / 2 + 4 }); tV.textContent = dy ? frn(dy) + " j" : "";
      if (n > 0.01) {
        var k = (n * U - 9) / (n * U);
        attr(vec, { x1: X(a.x), y1: Y(a.y), x2: X(a.x) + (X(b.x) - X(a.x)) * k, y2: Y(a.y) + (Y(b.y) - Y(a.y)) * k, visibility: "visible" });
      } else vec.setAttribute("visibility", "hidden");
      $('[data-o="A"]', root).textContent = "(" + a.x + " ; " + a.y + ")";
      $('[data-o="B"]', root).textContent = "(" + b.x + " ; " + b.y + ")";
      $('[data-o="AB"]', root).innerHTML = "(" + b.x + " − " + par(a.x) + " ; " + b.y + " − " + par(a.y) + ") = (" + frn(dx) + " ; " + frn(dy) + ")";
      $('[data-o="dec"]', root).innerHTML = "<span class=\"vec\">AB</span> = " + frn(dx) + " <span class=\"vec\">i</span> " +
        (dy < 0 ? "− " + frn(-dy) : "+ " + frn(dy)) + " <span class=\"vec\">j</span>";
      $('[data-o="n"]', root).innerHTML = "√(" + par(dx) + "² + " + par(dy) + "²) = √" + frn(dx * dx + dy * dy) + " ≈ " + fr(n, 2);
      if (!defiFait && dx && dy && Math.abs(n - 5) < 1e-9) {
        defiFait = true;
        $(".defi-ok", root).textContent = "✔ Bravo : " + Math.abs(dx) + "² + " + Math.abs(dy) + "² = 25 = 5². C'est le triangle « 3-4-5 » des charpentiers.";
      }
    }
    function bouger(k) {
      return function (pt) {
        P[k] = { x: clamp(Math.round((pt.x - OX) / U), 0, XM), y: clamp(Math.round((OY - pt.y) / U), 0, YM) };
        rendu();
      };
    }
    function cle(k) { return function (dx, dy) { P[k] = { x: clamp(P[k].x + dx, 0, XM), y: clamp(P[k].y + dy, 0, YM) }; rendu(); }; }
    deplacable(svg, hA, bouger("A"), cle("A"));
    deplacable(svg, hB, bouger("B"), cle("B"));
    rendu();
  });

  // ===================== triangle rectangle et rapports trigonométriques =====================
  $$('[data-widget="trigo"]').forEach(function (root) {
    var svg = $("svg", root), K = 25, AX = 60, BY = 268;
    var sA = $('[data-in="a"]', root), sH = $('[data-in="h"]', root), defis = {};
    var cAdj = "#C2185B", cOpp = "#0E8BA8", cHyp = "#7E57C2";
    var adj = el("line", { stroke: cAdj, "stroke-width": 5 }, svg), opp = el("line", { stroke: cOpp, "stroke-width": 5 }, svg);
    var hyp = el("line", { stroke: cHyp, "stroke-width": 5 }, svg);
    var ang = el("path", { fill: "none", stroke: "#1C2530", "stroke-width": 2 }, svg), dr = el("path", { fill: "none", stroke: "#1C2530", "stroke-width": 1.5 }, svg);
    var tA = el("text", { "class": "g-lab" }, svg, "A"), tB = el("text", { "class": "g-lab" }, svg, "B"), tC = el("text", { "class": "g-lab" }, svg, "C");
    var tAdj = el("text", { "class": "g-lab-s", fill: cAdj, "text-anchor": "middle" }, svg), tOpp = el("text", { "class": "g-lab-s", fill: cOpp }, svg);
    var tHyp = el("text", { "class": "g-lab-s", fill: cHyp, "text-anchor": "end" }, svg), tAng = el("text", { "class": "g-lab-s" }, svg);
    function rendu() {
      var a = +sA.value, h = +sH.value, ca = Math.cos(a * RAD), sa = Math.sin(a * RAD);
      var la = h * ca, lo = h * sa, Cx = AX + la * K, By = BY - lo * K;
      attr(adj, { x1: AX, y1: BY, x2: Cx, y2: BY }); attr(opp, { x1: Cx, y1: BY, x2: Cx, y2: By }); attr(hyp, { x1: AX, y1: BY, x2: Cx, y2: By });
      attr(ang, { d: arc(AX, BY, 34, 0, a) });
      attr(dr, { d: "M" + (Cx - 12) + " " + BY + " v-12 h12" });
      attr(tA, { x: AX - 20, y: BY + 6 }); attr(tC, { x: Cx + 8, y: BY + 18 }); attr(tB, { x: Cx + 8, y: By - 4 });
      attr(tAdj, { x: (AX + Cx) / 2, y: BY + 20 }); tAdj.textContent = "adjacent : " + fr(la, 1);
      attr(tOpp, { x: Cx + 10, y: (BY + By) / 2 + 4 }); tOpp.textContent = "opposé : " + fr(lo, 1);
      attr(tHyp, { x: (AX + Cx) / 2 - 8, y: (BY + By) / 2 - 8 }); tHyp.textContent = "hypoténuse : " + fr(h, 1);
      attr(tAng, { x: AX + 40, y: BY - 10 }); tAng.textContent = a + "°";
      $('[data-o="a"]', root).textContent = a + "°"; $('[data-o="h"]', root).textContent = fr(h, 1);
      $('[data-o="cos"]', root).textContent = fr(la, 2) + " / " + fr(h, 1) + " = " + fr(ca, 3);
      $('[data-o="sin"]', root).textContent = fr(lo, 2) + " / " + fr(h, 1) + " = " + fr(sa, 3);
      $('[data-o="tan"]', root).textContent = fr(lo, 2) + " / " + fr(la, 2) + " = " + fr(sa / ca, 3);
      if (a === 45 && !defis.d45) { defis.d45 = 1; $('[data-defi="45"]', root).textContent = "✔ À 45°, côté opposé = côté adjacent : tan 45° = 1."; }
      if (a === 30 && !defis.d30) { defis.d30 = 1; $('[data-defi="30"]', root).textContent = "✔ sin 30° = 0,5 : le côté opposé vaut la moitié de l'hypoténuse."; }
    }
    sA.addEventListener("input", rendu); sH.addEventListener("input", rendu);
    rendu();
  });

  // ===================== projection d'une force =====================
  $$('[data-widget="projection"]').forEach(function (root) {
    var svg = $("svg", root), OX = 230, OY = 200, S = 0.16;
    var sF = $('[data-in="F"]', root), sAng = $('[data-in="ang"]', root), mode = "alpha", defis = {};
    var mk = fleche(svg, "fl-pr", "#1C2530"), mkF = fleche(svg, "fl-pr-f", "#1B7A43"),
        mkX = fleche(svg, "fl-pr-x", "#B42318"), mkY = fleche(svg, "fl-pr-y", "#1F5FA8");
    el("line", { x1: 20, y1: OY, x2: 444, y2: OY, "class": "g-axe", "marker-end": mk }, svg);
    el("line", { x1: OX, y1: 368, x2: OX, y2: 18, "class": "g-axe", "marker-end": mk }, svg);
    el("text", { x: 446, y: OY + 22, "class": "g-lab" }, svg, "x"); el("text", { x: 8, y: OY - 8, "class": "g-lab" }, svg, "x'");
    el("text", { x: OX + 10, y: 26, "class": "g-lab" }, svg, "y"); el("text", { x: OX + 10, y: 372, "class": "g-lab" }, svg, "y'");
    el("text", { x: OX - 18, y: OY + 20, "class": "g-lab" }, svg, "O");
    var pX = el("line", { stroke: "#7A848C", "stroke-width": 1.5, "stroke-dasharray": "5 4" }, svg);
    var pY = el("line", { stroke: "#7A848C", "stroke-width": 1.5, "stroke-dasharray": "5 4" }, svg);
    var vX = el("line", { stroke: "#B42318", "stroke-width": 5, "marker-end": mkX }, svg);
    var vY = el("line", { stroke: "#1F5FA8", "stroke-width": 5, "marker-end": mkY }, svg);
    var vF = el("line", { stroke: "#1B7A43", "stroke-width": 4, "marker-end": mkF }, svg);
    var aP = el("path", { fill: "none", stroke: "#1C2530", "stroke-width": 1.8 }, svg), aT = el("text", { "class": "g-lab" }, svg);
    var tF = el("text", { "class": "g-lab", fill: "#1B7A43" }, svg, "F"), tX = el("text", { "class": "g-lab", fill: "#B42318" }, svg, "Fx");
    var tY = el("text", { "class": "g-lab", fill: "#1F5FA8" }, svg, "Fy");
    var hT = poignee(svg, "Extrémité de la force F", "#F2B705");
    function theta() { return mode === "alpha" ? +sAng.value : 90 + +sAng.value; }
    function rendu() {
      var F = +sF.value, t = theta(), fx = F * Math.cos(t * RAD), fy = F * Math.sin(t * RAD);
      var tx = OX + S * fx, ty = OY - S * fy, L = Math.sqrt(fx * fx + fy * fy) * S;
      attr(pX, { x1: tx, y1: ty, x2: tx, y2: OY }); attr(pY, { x1: tx, y1: ty, x2: OX, y2: ty });
      function vecteur(e, x2, y2) {
        var l = Math.hypot(x2 - OX, y2 - OY);
        if (l < 10) { e.setAttribute("visibility", "hidden"); return; }
        var k = (l - 7) / l;
        attr(e, { x1: OX, y1: OY, x2: OX + (x2 - OX) * k, y2: OY + (y2 - OY) * k, visibility: "visible" });
      }
      vecteur(vX, tx, OY); vecteur(vY, OX, ty); vecteur(vF, tx, ty);
      attr(tF, { x: tx + (fx >= 0 ? 8 : -20), y: ty + (fy >= 0 ? -6 : 18) });
      attr(tX, { x: tx + (fx >= 0 ? -24 : 0), y: OY + (fy >= 0 ? 22 : -10) });
      attr(tY, { x: OX + (fx >= 0 ? -30 : 8), y: ty + 5 });
      var a0 = mode === "alpha" ? 0 : 90;
      attr(aP, { d: L > 30 && Math.abs(t - a0) > 1 ? arc(OX, OY, Math.min(52, L - 10), a0, t) : "" });
      var am = (a0 + t) / 2;
      attr(aT, { x: OX + 64 * Math.cos(am * RAD) - 6, y: OY - 64 * Math.sin(am * RAD) + 5 });
      aT.textContent = mode === "alpha" ? "α" : "β";
      placer(hT, tx, ty);
      var a = +sAng.value, nom = mode === "alpha" ? "α" : "β";
      $('[data-o="F"]', root).textContent = fr(F, 0) + " N";
      $('[data-o="ang"]', root).textContent = nom + " = " + a + "°";
      $('[data-o="nom"]', root).textContent = mode === "alpha" ? "Angle α (depuis l'axe x)" : "Angle β (depuis l'axe y, vers x')";
      var lx, ly;
      if (mode === "alpha") {
        lx = "F<sub>x</sub> = F × cos α = " + fr(F, 0) + " × cos(" + a + "°) = <b>" + fr(fx, 2) + " N</b>";
        ly = "F<sub>y</sub> = F × sin α = " + fr(F, 0) + " × sin(" + a + "°) = <b>" + fr(fy, 2) + " N</b>";
      } else {
        lx = "F<sub>x</sub> = −F × sin β = −" + fr(F, 0) + " × sin(" + a + "°) = <b>" + fr(fx, 2) + " N</b>";
        ly = "F<sub>y</sub> = F × cos β = " + fr(F, 0) + " × cos(" + a + "°) = <b>" + fr(fy, 2) + " N</b>";
      }
      $('[data-o="fx"]', root).innerHTML = lx; $('[data-o="fy"]', root).innerHTML = ly;
      $('[data-o="signe"]', root).textContent = F ? "F" + "x " + (fx > 0.005 ? "> 0 : la projection pointe vers les x positifs" : fx < -0.005 ?
        "< 0 : la projection pointe vers les x négatifs (x')" : "= 0 : F est perpendiculaire à l'axe x") + " ; Fy " + (fy > 0.005 ? "> 0." : fy < -0.005 ? "< 0." : "= 0.") : "";
      $('[data-o="verif"]', root).textContent = "√(Fx² + Fy²) = " + fr(Math.sqrt(fx * fx + fy * fy), 2) + " N = F";
      if (F >= 50 && Math.abs(fx - fy) < 0.01 && !defis.egal) { defis.egal = 1; $('[data-defi="egal"]', root).textContent = "✔ Trouvé : à 45° (ou −135°), cos α = sin α."; }
      if (F >= 50 && fx < -1 && fy > 1 && !defis.signe) { defis.signe = 1; $('[data-defi="signe"]', root).textContent = "✔ Trouvé : F pointe vers le haut et vers la gauche."; }
    }
    function choisir(m) {
      mode = m;
      $$(".simu-choix button", root).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-mode") === m ? "true" : "false"); });
      if (m === "alpha") { sAng.min = -180; sAng.max = 180; sAng.value = 30; } else { sAng.min = 0; sAng.max = 180; sAng.value = 30; }
      rendu();
    }
    $$(".simu-choix button", root).forEach(function (b) { b.addEventListener("click", function () { choisir(b.getAttribute("data-mode")); }); });
    sF.addEventListener("input", rendu); sAng.addEventListener("input", rendu);
    deplacable(svg, hT, function (pt) {
      var dx = (pt.x - OX) / S, dy = (OY - pt.y) / S;
      sF.value = clamp(Math.round(Math.hypot(dx, dy) / 10) * 10, 0, 1000);
      var t = Math.round(Math.atan2(dy, dx) / RAD), b = t - 90;                // β : angle depuis l'axe y, vers x'
      if (b <= -180) b += 360;
      sAng.value = mode === "alpha" ? t : clamp(b, 0, 180);
      rendu();
    }, function (dx) { sAng.value = clamp(+sAng.value + dx, +sAng.min, +sAng.max); rendu(); });
    rendu();
  });

  // ===================== clé de serrage : couple =====================
  $$('[data-widget="cle"]').forEach(function (root) {
    var svg = $("svg", root), OX = 70, OY = 120, K = 0.95, KF = 0.6;
    var sF = $('[data-in="F"]', root), sL = $('[data-in="L"]', root), sA = $('[data-in="a"]', root), meilleur = null;
    var mkF = fleche(svg, "fl-cle-f", "#1C2530"), mkM = fleche(svg, "fl-cle-m", "#B42318");
    var manche = el("line", { stroke: "#1C2530", "stroke-width": 30, "stroke-linecap": "round" }, svg);
    var mancheIn = el("line", { stroke: "#D7DDE2", "stroke-width": 25, "stroke-linecap": "round" }, svg);
    el("circle", { cx: OX, cy: OY, r: 34, fill: "#D7DDE2", stroke: "#1C2530", "stroke-width": 2.5 }, svg);
    var hex = [], i;
    for (i = 0; i < 6; i++) hex.push((OX + 20 * Math.cos((i * 60 + 30) * RAD)).toFixed(1) + "," + (OY + 20 * Math.sin((i * 60 + 30) * RAD)).toFixed(1));
    el("polygon", { points: hex.join(" "), fill: "#fff", stroke: "#1C2530", "stroke-width": 2 }, svg);
    el("circle", { cx: OX, cy: OY, r: 3, fill: "#1C2530" }, svg);
    el("text", { x: OX - 52, y: OY + 6, "class": "g-lab" }, svg, "O");
    var ligne = el("line", { stroke: "#7A848C", "stroke-width": 1.5, "stroke-dasharray": "7 5" }, svg);
    var bras = el("line", { stroke: "#F2B705", "stroke-width": 5 }, svg), equ = el("path", { fill: "none", stroke: "#1C2530", "stroke-width": 1.5 }, svg);
    var tD = el("text", { "class": "g-lab", fill: "#9A6A00" }, svg, "d"), tH = el("text", { "class": "g-lab-s" }, svg, "H");
    var force = el("line", { stroke: "#1C2530", "stroke-width": 4, "marker-end": mkF }, svg), tF = el("text", { "class": "g-lab" }, svg, "F");
    var pA = el("circle", { r: 4, fill: "#1C2530" }, svg), tA = el("text", { "class": "g-lab" }, svg, "A");
    var arcA = el("path", { fill: "none", stroke: "#1C2530", "stroke-width": 1.5 }, svg), tAl = el("text", { "class": "g-lab-s" }, svg, "α");
    var rot = el("path", { fill: "none", stroke: "#B42318", "marker-end": mkM }, svg);
    var jauge = $(".jauge-bar", root), cible = $(".jauge-cible", root), MAX = 80, CIBLE = 30;
    cible.style.left = (CIBLE / MAX * 100) + "%";
    function rendu() {
      var F = +sF.value, L = +sL.value, a = +sA.value;
      var Ax = OX + L * K, Ay = OY, t = 180 + a, ux = Math.cos(t * RAD), uy = -Math.sin(t * RAD);
      attr(manche, { x1: OX, y1: OY, x2: Ax + 8, y2: OY }); attr(mancheIn, { x1: OX, y1: OY, x2: Ax + 8, y2: OY });
      attr(pA, { cx: Ax, cy: Ay }); attr(tA, { x: Ax + 10, y: Ay - 18 });
      attr(ligne, { x1: Ax - 700 * ux, y1: Ay - 700 * uy, x2: Ax + 700 * ux, y2: Ay + 700 * uy });
      var lf = Math.max(F * KF, 1);
      attr(force, { x1: Ax, y1: Ay, x2: Ax + lf * ux, y2: Ay + lf * uy, visibility: F > 0 ? "visible" : "hidden" });
      attr(tF, { x: Ax + lf * ux + (ux < 0 ? -18 : 8), y: Ay + lf * uy + 16 });
      var tt = (OX - Ax) * ux + (OY - Ay) * uy, Hx = Ax + tt * ux, Hy = Ay + tt * uy, d = L * Math.sin(a * RAD);
      attr(bras, { x1: OX, y1: OY, x2: Hx, y2: Hy, visibility: d > 2 ? "visible" : "hidden" });
      var nx = (OX - Hx), ny = (OY - Hy), nl = Math.hypot(nx, ny) || 1;
      nx /= nl; ny /= nl;
      attr(equ, { d: d > 12 ? "M" + (Hx + 10 * nx) + " " + (Hy + 10 * ny) + " l" + (10 * ux) + " " + (10 * uy) + " l" + (-10 * nx) + " " + (-10 * ny) : "" });
      attr(tD, { x: (OX + Hx) / 2 + 10, y: (OY + Hy) / 2 + 4, visibility: d > 12 ? "visible" : "hidden" });
      attr(tH, { x: Hx + 6, y: Hy + 14, visibility: d > 2 ? "visible" : "hidden" });
      attr(arcA, { d: a > 2 && a < 178 ? arc(Ax, Ay, 30, 180, 180 + a) : "" });
      attr(tAl, { x: Ax + 40 * Math.cos((180 + a / 2) * RAD) - 4, y: Ay - 40 * Math.sin((180 + a / 2) * RAD) + 4 });
      var M = -F * (L / 1000) * Math.sin(a * RAD), aM = Math.abs(M);
      attr(rot, { d: aM > 0.05 ? arc(OX, OY, 52, 100, -40) : "", "stroke-width": (2 + Math.min(7, aM / 10)).toFixed(1) });
      $('[data-o="F"]', root).textContent = F + " N"; $('[data-o="L"]', root).textContent = L + " mm"; $('[data-o="a"]', root).textContent = a + "°";
      $('[data-o="d"]', root).innerHTML = "d = OA × sin α = " + L + " × sin(" + a + "°) = <b>" + fr(d, 2) + " mm</b>";
      $('[data-o="M"]', root).innerHTML = "‖M<sub>O</sub>‖ = F × d = " + F + " × " + fr(d / 1000, 4) + " = <b>" + fr(aM, 2) + " N·m</b>";
      $('[data-o="sens"]', root).textContent = aM < 0.005 ? "Couple nul : la droite d'action de F passe par O (α = 0° ou 180°) ou F = 0."
        : "Sens horaire (vu de dessus) : le couple est négatif, M = " + fr(M, 2) + " N·m.";
      jauge.style.width = Math.min(100, aM / MAX * 100) + "%";
      var atteint = Math.abs(aM - CIBLE) <= 0.5;
      jauge.classList.toggle("ok", atteint);
      var msg = $('[data-o="defi"]', root);
      if (atteint) {
        if (meilleur === null || F < meilleur) meilleur = F;
        msg.textContent = F <= 75 ? "✔ Imbattable : 30 N·m avec 75 N seulement (OA = 400 mm, α = 90°). Bras de levier maximal, force minimale."
          : "✔ 30 N·m atteints avec F = " + F + " N. Peux-tu y arriver avec une force plus faible ?";
        msg.className = "defi-ok";
      } else if (meilleur !== null) { msg.textContent = "Ton meilleur essai : " + meilleur + " N."; msg.className = ""; }
    }
    [sF, sL, sA].forEach(function (s) { s.addEventListener("input", rendu); });
    rendu();
  });

  // ===================== produit vectoriel pas à pas =====================
  $$('[data-widget="pvect"]').forEach(function (root) {
    var ins = {}, comp = "x";
    $$("input[data-v]", root).forEach(function (i) { ins[i.getAttribute("data-v")] = i; });
    var REG = { x: ["y", "z", "z", "y"], y: ["z", "x", "x", "z"], z: ["x", "y", "y", "x"] };   // u·v' − u''·v'''
    function val(k) { var v = lireNombre(ins[k].value); return v === null ? 0 : v; }
    function calc(c) {
      var r = REG[c];
      return val("a" + r[0]) * val("b" + r[1]) - val("a" + r[2]) * val("b" + r[3]);
    }
    function rendu() {
      ["x", "y", "z"].forEach(function (c) { $('[data-r="' + c + '"]', root).textContent = frn(calc(c)); });
      $$("td", root).forEach(function (td) { td.classList.remove("plus", "moins"); });
      $$(".res", root).forEach(function (td) { td.classList.toggle("on", td.getAttribute("data-r") === comp); });
      var r = REG[comp];
      ins["a" + r[0]].parentNode.classList.add("plus"); ins["b" + r[1]].parentNode.classList.add("plus");
      ins["a" + r[2]].parentNode.classList.add("moins"); ins["b" + r[3]].parentNode.classList.add("moins");
      $$("[data-c]", root).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-c") === comp ? "true" : "false"); });
      $('[data-o="detail"]', root).innerHTML = "Composante sur " + comp + " : " +
        "<span style=\"background:#D9F0E1\">" + r[0] + "<sub>OA</sub> × " + r[1] + "<sub>F</sub></span> − " +
        "<span style=\"background:#F9D9D5\">" + r[2] + "<sub>OA</sub> × " + r[3] + "<sub>F</sub></span> = " +
        par(val("a" + r[0])) + " × " + par(val("b" + r[1])) + " − " + par(val("a" + r[2])) + " × " + par(val("b" + r[3])) +
        " = <b>" + frn(calc(comp)) + "</b>";
      var plan = Math.abs(val("az")) < 1e-12 && Math.abs(val("bz")) < 1e-12;
      $('[data-o="plan"]', root).textContent = plan ? "OA et F sont dans le plan (x, y) : seule la composante sur z peut être non nulle, le moment est perpendiculaire au plan." : "";
    }
    $$("[data-c]", root).forEach(function (b) { b.addEventListener("click", function () { comp = b.getAttribute("data-c"); rendu(); }); });
    $$("[data-preset]", root).forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-preset").split(" ");
        ["ax", "ay", "az", "bx", "by", "bz"].forEach(function (k, i) { ins[k].value = v[i].replace(".", ","); });
        rendu();
      });
    });
    Object.keys(ins).forEach(function (k) { ins[k].addEventListener("input", rendu); });
    rendu();
  });

  // ===================== torseur : changer de point de réduction =====================
  $$('[data-widget="transport"]').forEach(function (root) {
    var svg = $("svg", root), U = 40, OX = 40, OY = 300, XM = 11, YM = 7, KF = 200;   // 1 m = 40 px ; 1 m de flèche = 200 N
    var A = { x: 3, y: 2 }, T = { x: 6, y: 4 }, B = { x: 1, y: 5 }, nuls = {};
    function X(x) { return OX + U * x; }
    function Y(y) { return OY - U * y; }
    var mk = fleche(svg, "fl-tr", "#1C2530"), mkF = fleche(svg, "fl-tr-f", "#1B7A43");
    var mkP = fleche(svg, "fl-tr-p", "#1F5FA8"), mkN = fleche(svg, "fl-tr-n", "#B42318");
    var gr = el("g", { "class": "g-grille" }, svg), i;
    for (i = 0; i <= XM; i++) el("line", { x1: X(i), y1: Y(0), x2: X(i), y2: Y(YM) }, gr);
    for (i = 0; i <= YM; i++) el("line", { x1: X(0), y1: Y(i), x2: X(XM), y2: Y(i) }, gr);
    el("line", { x1: X(0) - 10, y1: OY, x2: X(XM) + 14, y2: OY, "class": "g-axe", "marker-end": mk }, svg);
    el("line", { x1: OX, y1: Y(0) + 10, x2: OX, y2: Y(YM) - 14, "class": "g-axe", "marker-end": mk }, svg);
    el("text", { x: X(XM) + 4, y: OY + 22, "class": "g-lab" }, svg, "x"); el("text", { x: OX - 22, y: Y(YM) - 2, "class": "g-lab" }, svg, "y");
    el("text", { x: OX - 18, y: OY + 18, "class": "g-lab" }, svg, "O");
    for (i = 1; i <= XM; i++) el("text", { x: X(i), y: OY + 16, "class": "g-lab-s", "text-anchor": "middle" }, svg, String(i));
    for (i = 1; i <= YM; i++) el("text", { x: OX - 8, y: Y(i) + 4, "class": "g-lab-s", "text-anchor": "end" }, svg, String(i));
    var ligne = el("line", { stroke: "#1B7A43", "stroke-width": 1.5, "stroke-dasharray": "7 5" }, svg);
    var perp = el("line", { stroke: "#F2B705", "stroke-width": 4 }, svg), ba = el("line", { stroke: "#7A848C", "stroke-width": 1.5, "stroke-dasharray": "3 4" }, svg);
    var vF = el("line", { stroke: "#1B7A43", "stroke-width": 4, "marker-end": mkF }, svg);
    var rot = el("path", { fill: "none", "stroke-width": 3 }, svg);
    var hA = poignee(svg, "Point d'application A", "#fff"), hT = poignee(svg, "Extrémité de la force F", "#1B7A43", 6),
        hB = poignee(svg, "Point de réduction B", "#F2B705");
    var lA = el("text", { "class": "g-lab" }, svg, "A"), lB = el("text", { "class": "g-lab" }, svg, "B"), lF = el("text", { "class": "g-lab", fill: "#1B7A43" }, svg, "F");
    function tors(cells, pt) {
      return "<span class=\"tm\"><span class=\"tm-b\" aria-hidden=\"true\">{</span><span class=\"tm-g\">" +
        cells.map(function (c) { return "<span class=\"tm-c\">" + c + "</span>"; }).join("") +
        "</span><span class=\"tm-b\" aria-hidden=\"true\">}</span><sub class=\"tm-p\">" + pt + "</sub></span>";
    }
    function rendu() {
      var Fx = (T.x - A.x) * KF, Fy = (T.y - A.y) * KF, Fn = Math.hypot(Fx, Fy);
      var N = (A.x - B.x) * Fy - (A.y - B.y) * Fx;
      placer(hA, X(A.x), Y(A.y)); placer(hT, X(T.x), Y(T.y)); placer(hB, X(B.x), Y(B.y));
      attr(lA, { x: X(A.x) - 20, y: Y(A.y) + 20 }); attr(lB, { x: X(B.x) + 10, y: Y(B.y) - 10 }); attr(lF, { x: X(T.x) + 8, y: Y(T.y) - 8 });
      if (Fn > 0) {
        var ux = Fx / Fn, uy = Fy / Fn, l = Math.hypot(X(T.x) - X(A.x), Y(T.y) - Y(A.y)), k = (l - 7) / l;
        attr(vF, { x1: X(A.x), y1: Y(A.y), x2: X(A.x) + (X(T.x) - X(A.x)) * k, y2: Y(A.y) + (Y(T.y) - Y(A.y)) * k, visibility: "visible" });
        attr(ligne, { x1: X(A.x - 20 * ux), y1: Y(A.y - 20 * uy), x2: X(A.x + 20 * ux), y2: Y(A.y + 20 * uy), visibility: "visible" });
        var t = (B.x - A.x) * ux + (B.y - A.y) * uy, Hx = A.x + t * ux, Hy = A.y + t * uy;
        attr(perp, { x1: X(B.x), y1: Y(B.y), x2: X(Hx), y2: Y(Hy), visibility: Math.abs(N) > 1e-6 ? "visible" : "hidden" });
      } else { vF.setAttribute("visibility", "hidden"); ligne.setAttribute("visibility", "hidden"); perp.setAttribute("visibility", "hidden"); }
      attr(ba, { x1: X(B.x), y1: Y(B.y), x2: X(A.x), y2: Y(A.y) });
      attr(rot, { d: Math.abs(N) > 1e-6 ? (N > 0 ? arc(X(B.x), Y(B.y), 24, -60, 200) : arc(X(B.x), Y(B.y), 24, 200, -60)) : "",
        stroke: N > 0 ? "#1F5FA8" : "#B42318", "marker-end": N > 0 ? mkP : mkN });
      $('[data-o="A"]', root).textContent = "A (" + frn(A.x) + " ; " + frn(A.y) + ") m";
      $('[data-o="B"]', root).textContent = "B (" + frn(B.x) + " ; " + frn(B.y) + ") m";
      $('[data-o="F"]', root).textContent = "F = (" + frn(Fx) + " ; " + frn(Fy) + " ; 0) N";
      $('[data-o="tA"]', root).innerHTML = "{<i>T</i>}<sub>A</sub> = " + tors([frn(Fx), "0", frn(Fy), "0", "0", "0"], "A");
      $('[data-o="tB"]', root).innerHTML = "{<i>T</i>}<sub>B</sub> = " + tors([frn(Fx), "0", frn(Fy), "0", "0", "<b>" + frn(N) + "</b>"], "B");
      $('[data-o="N"]', root).innerHTML = "N = (x<sub>A</sub> − x<sub>B</sub>) F<sub>y</sub> − (y<sub>A</sub> − y<sub>B</sub>) F<sub>x</sub> = " +
        par(A.x - B.x) + " × " + par(Fy) + " − " + par(A.y - B.y) + " × " + par(Fx) + " = <b>" + frn(N) + " N·m</b>";
      var v = $('[data-o="verdict"]', root);
      if (A.x === B.x && A.y === B.y) { v.textContent = "B = A : au point d'application, le moment est nul."; v.className = "simu-verdict ok"; }
      else if (Math.abs(N) < 1e-6 && Fn > 0) {
        v.textContent = "B est sur la droite d'action de F : le moment en B est nul."; v.className = "simu-verdict ok";
        nuls[B.x + ";" + B.y] = 1;
      } else {
        v.textContent = N > 0 ? "Moment positif : autour de B, F tourne dans le sens trigonométrique." : "Moment négatif : autour de B, F tourne dans le sens horaire.";
        v.className = "simu-verdict";
      }
      var n = Object.keys(nuls).length, dd = $('[data-o="defi"]', root);
      dd.textContent = n >= 3 ? "✔ " + n + " points trouvés : ils sont tous alignés sur la droite d'action de F." : n + " / 3 point(s) trouvé(s).";
      dd.className = n >= 3 ? "defi-ok" : "";
    }
    function grille(pt, pas) {
      return { x: clamp(Math.round((pt.x - OX) / U / pas) * pas, 0, XM), y: clamp(Math.round((OY - pt.y) / U / pas) * pas, 0, YM) };
    }
    deplacable(svg, hA, function (pt) { var p = grille(pt, 0.5), dx = T.x - A.x, dy = T.y - A.y; A = p; T = { x: p.x + dx, y: p.y + dy }; rendu(); },
      function (dx, dy) { A = { x: clamp(A.x + dx, 0, XM), y: clamp(A.y + dy, 0, YM) }; T = { x: T.x + dx, y: T.y + dy }; rendu(); });
    deplacable(svg, hT, function (pt) { T = grille(pt, 0.5); rendu(); },
      function (dx, dy) { T = { x: clamp(T.x + dx * 0.5, 0, XM), y: clamp(T.y + dy * 0.5, 0, YM) }; rendu(); });
    deplacable(svg, hB, function (pt) { B = grille(pt, 0.5); rendu(); },
      function (dx, dy) { B = { x: clamp(B.x + dx * 0.5, 0, XM), y: clamp(B.y + dy * 0.5, 0, YM) }; rendu(); });
    rendu();
  });

  // ===================== torseur : à quoi correspond chaque lettre ? =====================
  $$('[data-widget="lettres"]').forEach(function (root) {
    var info = $(".tm-info", root);
    $$(".tm-c.clic", root).forEach(function (c) {
      function voir() {
        $$(".tm-c.clic", root).forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        info.innerHTML = c.getAttribute("data-info");
      }
      c.addEventListener("click", voir);
      c.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); voir(); } });
    });
  });
})();
