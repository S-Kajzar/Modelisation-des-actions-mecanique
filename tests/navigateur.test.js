// Parcours navigateur (Playwright, Chromium) : accueil, cours interactifs, exercices en entraînement et en examen.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const path = require("path");
const { chromium } = require("playwright");
const { reponseJuste } = require("./reponses.js");

const URL = (p) => "file://" + path.join(__dirname, "..", p);
// pages construites sur le gabarit (modes entraînement et examen) ; l'exercice des quadrants est une page autonome
const EXERCICES = ["exercice-projections.html", "force-moment.html", "exercice-couples-moments.html", "exercice-torseurs.html"];
const AUTONOMES = ["exercice-quadrants.html"];
const COURS = ["cours-modelisation.html", "cours-projection.html", "cours-couple-moment.html", "cours-torseur.html"];
let navigateur;

test.before(async () => { navigateur = await chromium.launch(); });
test.after(async () => { await navigateur.close(); });

async function ouvrir(page, requete) {
  const p = await navigateur.newPage({ viewport: { width: 1280, height: 900 } });
  const erreurs = [];
  p.on("pageerror", (e) => erreurs.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") erreurs.push(m.text()); });
  await p.goto(URL(page) + (requete || ""));
  return { p, erreurs };
}

// remplit toutes les réponses justes ; valide chaque question si demandé (mode entraînement)
async function toutRemplir(p, valider) {
  const cfg = await p.evaluate(() => window.__QCFG__);
  for (const id of Object.keys(cfg)) {
    if (!(await p.$("#in-" + id))) continue;
    await p.fill("#in-" + id, reponseJuste(cfg[id].grader));
    if (valider) await p.click("#" + id + " .btn-validate");
  }
  for (const bloc of await p.$$(".fast-q")) {
    for (const i of await bloc.$$(".sol input")) await i.fill(reponseJuste(cfg[await i.getAttribute("data-q")].grader));
    if (valider) await (await bloc.$(".btn-fast")).click();
  }
}

test("accueil : toutes les cartes mènent à une page existante", async () => {
  const { p, erreurs } = await ouvrir("index.html");
  const liens = await p.$$eval("a.btn", (a) => a.map((x) => x.getAttribute("href")));
  assert.deepStrictEqual(liens.sort(), COURS.concat(EXERCICES, AUTONOMES).sort());
  assert.deepStrictEqual(erreurs, []);
  await p.close();
});

for (const page of EXERCICES) {
  test(page + " : entraînement entièrement juste = 20/20, méthode accessible", async () => {
    const { p, erreurs } = await ouvrir(page);
    await p.click("[data-mode=training]");
    assert.ok(await p.isVisible(".rail .tab.meth"), "onglet Méthode visible");
    await toutRemplir(p, true);
    assert.strictEqual((await p.$$(".q.is-ko, .q.is-half, .sol.is-ko")).length, 0);
    assert.match(await p.innerText("tfoot .final-note"), /^20,0\/20/);
    assert.ok(await p.isDisabled(".q-input, .fast-q .sol input >> nth=0"), "réponse verrouillée après validation");
    assert.deepStrictEqual(erreurs, []);
    await p.close();
  });

  test(page + " : examen sans méthode ni correction avant la remise, 20/20 après", async () => {
    const { p, erreurs } = await ouvrir(page);
    await p.click("[data-mode=exam]");
    for (const sel of [".rail .tab.meth", ".dp-tabs button", ".doc-chip", "#btn-docs", ".btn-validate", ".btn-fast"])
      assert.ok(!(await p.isVisible(sel)), sel + " masqué en examen");
    await p.evaluate(() => window.__app__.openDoc("METH"));
    assert.ok(!(await p.isVisible("#doc-METH")), "la méthode ne s'ouvre pas, même par le script");
    await toutRemplir(p, false);
    assert.ok(!(await p.isVisible(".q-expl")), "aucune correction visible avant la remise");
    await p.emulateMedia({ media: "print" });
    assert.ok(await p.isVisible(".print-nograde"), "copie imprimée : « Copie non corrigée »");
    await p.emulateMedia({ media: "screen" });
    await p.click("#exam-submit");
    await p.click("#exam-submit");
    assert.match(await p.innerText("tfoot .final-note"), /^20,0\/20/);
    assert.ok(!(await p.isVisible(".rail .tab.meth")), "méthode toujours absente après la remise");
    assert.deepStrictEqual(erreurs, []);
    await p.close();
  });
}

for (const page of COURS) {
  test(page + " : simulateurs sans erreur, quiz entièrement juste = 3 étoiles, jeux réussis", async () => {
    const { p, erreurs } = await ouvrir(page);
    for (const fs of await p.$$(".quiz-q")) {
      const ok = await fs.getAttribute("data-ok");
      await (await fs.$(`input[value="${ok}"]`)).check();
    }
    assert.strictEqual(await p.innerText(".qz-stars"), "★★★");
    for (const t of await p.$$(".trous")) {
      await (await t.$(".trous-sol")).click();
      assert.match(await (await t.$(".trous-s")).innerText(), /Tout est juste/);
    }
    for (const j of await p.$$(".jeu")) {
      for (const l of await j.$$(".jeu-l")) await (await l.$(`button[data-v="${await l.getAttribute("data-ok")}"]`)).click();
      assert.match(await (await j.$(".jeu-s")).innerText(), /parfait/);
    }
    for (const c of await p.$$(".check")) {
      await (await c.$("input")).fill((await c.getAttribute("data-ans")).replace(".", ","));
      await (await c.$("button")).click();
      assert.ok(await c.evaluate((e) => e.classList.contains("is-ok")), "vérification rapide juste");
    }
    const deborde = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    assert.ok(!deborde, "pas de défilement horizontal");
    assert.deepStrictEqual(erreurs, []);
    await p.close();
  });
}

test("exercice-quadrants.html : séries reproductibles, signes par quadrant, 20/20 si tout est juste", async () => {
  const { p, erreurs } = await ouvrir("exercice-quadrants.html", "?graine=12345");
  const serie = await p.evaluate(() => window.__qd__.serie());
  assert.strictEqual(serie.liste.length, 10);
  const combis = {};
  serie.liste.forEach((c) => { combis[c.join()] = (combis[c.join()] || 0) + 1; });
  assert.strictEqual(Object.keys(combis).length, 8, "les 8 situations (4 quadrants × 2 axes) sont présentes");
  const premiere = await p.evaluate(() => window.__qd__.courant());
  await p.reload();
  assert.deepStrictEqual(await p.evaluate(() => window.__qd__.courant()), premiere, "même graine, même série");
  const signes = { 1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1] };
  for (let i = 0; i < 10; i++) {
    const c = await p.evaluate(() => window.__qd__.courant());
    assert.deepStrictEqual([Math.sign(c.Fx), Math.sign(c.Fy)], signes[c.q], "signes du quadrant " + c.q);
    assert.ok(c.a >= 10 && c.a <= 80 && c.a !== 45 && c.F >= 100 && c.F <= 990);
    assert.ok(Math.abs(Math.hypot(c.Fx, c.Fy) - c.F) < 0.02, "F² = Fx² + Fy²");
    const r = await p.evaluate(() => window.__qd__.reponses());
    for (const k of ["lx", "ly", "nx", "ny"]) await p.fill(`[data-k="${k}"] input`, r[k]);
    await p.press('[data-k="ny"] input', "Enter");
    assert.match(await p.getAttribute("#qd-fb", "class"), /\bok\b/, "question " + (i + 1) + " juste");
    assert.ok(await p.isVisible("#qd-corr"), "correction affichée");
    await p.press('[data-k="ny"] input', "Enter");
  }
  assert.match(await p.innerText("#qd-note"), /^20/);
  // série réglée : quadrant 3, angle depuis l'axe vertical ; « Correction » compte la question comme manquée
  await p.evaluate(() => window.__qd__.lancer(["v"], [3], 5));
  for (let i = 0; i < 5; i++) {
    const c = await p.evaluate(() => window.__qd__.courant());
    assert.ok(c.q === 3 && c.ref === "v" && c.tx === "sin" && c.ty === "cos");
    await p.fill('[data-k="lx"] input', "F cos α");
    await p.click("#qd-check");
    assert.ok(await p.$('[data-k="lx"].ko'), "cos au lieu de sin : refusé");
    await p.click("#qd-sol");
    assert.match(await p.innerText('[data-k="lx"] .ta-att'), /−F sin α/);
    await p.click("#qd-next");
  }
  assert.match(await p.innerText("#qd-note"), /^0/);
  // écritures équivalentes d'une expression littérale
  const v = await p.evaluate(() => [["-F sin α", 100, 30], ["−F×sin(a)", 100, 30], ["-Fsinα", 100, 30], ["F cos(90-α)", 2, 30],
    ["-F*sin(alpha)", 100, 30], ["F co", 1, 1]].map((x) => window.__qd__.analyser(x[0], x[1], x[2])));
  [-50, -50, -50, 1, -50].forEach((w, i) => assert.ok(Math.abs(v[i] - w) < 1e-9, "écriture " + i));
  assert.strictEqual(v[5], null, "écriture invalide");
  assert.deepStrictEqual(erreurs, []);
  await p.close();
  const m = await navigateur.newPage({ viewport: { width: 390, height: 800 } });
  await m.goto(URL("exercice-quadrants.html"));
  assert.ok(!(await m.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1)),
    "pas de défilement horizontal sur téléphone");
  await m.close();
});
