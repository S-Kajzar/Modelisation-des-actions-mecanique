// Parcours navigateur (Playwright, Chromium) : accueil, cours interactifs, exercices en entraînement et en examen.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const path = require("path");
const { chromium } = require("playwright");
const { reponseJuste } = require("./reponses.js");

const URL = (p) => "file://" + path.join(__dirname, "..", p);
const EXERCICES = ["force-moment.html", "exercice-projections.html", "exercice-quadrants.html", "exercice-couples-moments.html",
  "exercice-torseurs.html"];
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
  assert.deepStrictEqual(liens.sort(), COURS.concat(EXERCICES).sort());
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
    assert.ok(await p.isDisabled(".q-input >> nth=0"), "réponse verrouillée après validation");
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

test("exercice-quadrants.html : tirages reproductibles, une force par quadrant et par axe de référence", async () => {
  const { p, erreurs } = await ouvrir("exercice-quadrants.html", "?graine=12345");
  const t = await p.evaluate(() => window.__tirage__);
  assert.strictEqual(t.graine, 12345);
  const signes = { 1: [1, 1], 2: [-1, 1], 3: [-1, -1], 4: [1, -1] };
  t.forces.forEach((f, i) => {
    assert.strictEqual(f.q, Math.floor(i / 2) + 1, "deux forces par quadrant, dans l'ordre");
    assert.deepStrictEqual([Math.sign(Math.cos(f.th * Math.PI / 180)), Math.sign(Math.sin(f.th * Math.PI / 180))], signes[f.q]);
    assert.ok(f.a >= 10 && f.a <= 80 && f.a !== 45 && f.F >= 100 && f.F <= 990);
  });
  [0, 1, 2, 3].forEach((q) => assert.notStrictEqual(t.forces[2 * q].h, t.forces[2 * q + 1].h, "un angle horizontal, un vertical"));
  await p.reload();
  assert.deepStrictEqual(await p.evaluate(() => window.__tirage__), t, "même graine, même sujet");
  await p.goto(URL("exercice-quadrants.html") + "?graine=777");
  assert.notDeepStrictEqual((await p.evaluate(() => window.__tirage__)).forces, t.forces, "autre graine, autre sujet");
  for (const g of [1, 2, 99999]) {
    await p.goto(URL("exercice-quadrants.html") + "?graine=" + g);
    await p.click("[data-mode=training]");
    await toutRemplir(p, true);
    assert.match(await p.innerText("tfoot .final-note"), /^20,0\/20/, "graine " + g);
  }
  assert.deepStrictEqual(erreurs, []);
  await p.close();
});
