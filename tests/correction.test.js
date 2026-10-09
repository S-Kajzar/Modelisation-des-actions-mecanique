// Tests du moteur de correction sur chaque page d'exercice : une réponse juste par question (tests/reponses.js),
// puis les cas faux et limites des questions sensibles (signes, unités, formules littérales).
//   node --test tests/correction.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("fs");
const path = require("path");
const { reponseJuste } = require("./reponses.js");

const RACINE = path.join(__dirname, "..");
const PAGES = ["force-moment", "exercice-projections", "exercice-couples-moments", "exercice-torseurs"];

function charger(page) {
  const h = fs.readFileSync(path.join(RACINE, page + ".html"), "utf8");
  const g = h.slice(h.indexOf("/*GRADING-START*/"), h.indexOf("/*GRADING-END*/"));
  const m = { exports: {} };
  new Function("module", g + ";")(m);
  const cfg = JSON.parse(h.match(/window\.__QCFG__ = (\{.*?\});\n/)[1]);
  return { G: m.exports, cfg };
}
const P = {};
PAGES.forEach((p) => { P[p] = charger(p); });

function note(page, id, rep) {
  const { G, cfg } = P[page];
  assert.ok(cfg[id], page + " : question inconnue " + id);
  const r = G.grade(rep, cfg[id].grader);
  return r.invalid ? "invalide" : r.score;
}
function cas(page, id, liste) {
  liste.forEach(([rep, attendu]) => assert.strictEqual(note(page, id, rep), attendu, `${page} ${id} « ${rep} »`));
}

PAGES.forEach((page) => {
  test(page + " : la réponse juste de chaque question vaut tous les points", () => {
    const { G, cfg } = P[page];
    Object.keys(cfg).forEach((id) => {
      const r = G.grade(reponseJuste(cfg[id].grader), cfg[id].grader);
      assert.strictEqual(r.score, 1, `${id} : ${JSON.stringify(r)}`);
    });
  });
});

test("exercice 1.2 : composantes, unités et signes", () => {
  cas("exercice-projections", "q1_1", [["939,69 N", 1], ["939,69", 0.5], ["939,7 N", 1], ["342,02 N", 0], ["939,69 daN", 0.5]]);
  cas("exercice-projections", "q2_15", [["707,11 N", 1], ["-707,11 N", 0], ["707.11 newtons", 1]]);
  cas("exercice-projections", "q2_11", [["-866,03 N", 1], ["866,03 N", 0], ["−866,03 N", 1]]);
  cas("exercice-projections", "q3_3", [["-68,40 N", 1], ["68,40 N", 0], ["-68,4 N", 1]]);
  cas("exercice-projections", "q4_3", [["200 daN", 1], ["2000 N", 1], ["200", 0.5], ["100 daN", 0]]);
  cas("exercice-projections", "q4_5", [["314,63 daN", 1], ["-314,63 daN", 1], ["3146,26 N", 1], ["173,21 daN", 0]]);
});

test("exercice 1.2 : expressions littérales équivalentes acceptées, fausses refusées", () => {
  cas("exercice-projections", "q2_1", [["Fx = F*cos(α)", 1], ["F cos alpha", 1], ["F.cos a", 1], ["F*sin(α)", 0],
    ["866,03", 0], ["-F*cos(α)", 0]]);
  cas("exercice-projections", "q2_5", [["-F*sin(α)", 1], ["−F × sin α", 1], ["-F*cos(90-α)", 1], ["F*sin(α)", 0],
    ["-F*cos(α)", 0]]);
  cas("exercice-projections", "q2_10", [["F*cos(α)", 1], ["-F*cos(180-α)", 1], ["-F*sin(α)", 0], ["-F*cos(60)", 0]]);
  cas("exercice-projections", "q2_13", [["F*cos(α-β)", 1], ["F cos(alpha - beta)", 1], ["F*cos(45)", 0], ["F*sin(α-β)", 0]]);
  cas("exercice-projections", "q2_1", [["F*cos(x)", "invalide"], ["F*cos(", "invalide"]]);
});

test("exercice 2.1 : couples, moments, signes et unités", () => {
  cas("exercice-couples-moments", "q1_1", [["0,47 N·m", 1], ["469,85 N·mm", 1], ["0,47", 0.5], ["0,5 N·m", 0], ["-0,47 N.m", 1]]);
  cas("exercice-couples-moments", "q2_1", [["120 N·m", 1], ["12 daN·m", 1], ["120000 N.mm", 1], ["120 N", 0.5], ["12 N·m", 0]]);
  cas("exercice-couples-moments", "q2_2", [["-120 N·m", 1], ["120 N·m", 0], ["-12 daN.m", 1]]);
  cas("exercice-couples-moments", "q3_1", [["P = q*a/b", 1], ["P = a × q / b", 1], ["P = q*b/a", 0], ["P = 35", 0]]);
  cas("exercice-couples-moments", "q3_3", [["35,68 kg", 1], ["35,7 kg", 0], ["35,68", 0.5], ["35 kg", 0]]);
  cas("exercice-couples-moments", "q4_1", [["4700 daN·m", 1], ["47 000 N·m", 1], ["-4700 daN·m", 0], ["70300 daN·m", 0]]);
  cas("exercice-couples-moments", "q4_2", [["non", 1], ["oui", 0]]);
  cas("exercice-couples-moments", "q4_3", [["12619 daN", 1], ["12 619 daN", 1], ["12620 daN", 1], ["11500 daN", 0]]);
  cas("exercice-couples-moments", "q5_4", [["-6928,20 N·m", 1], ["-6928,24 N·m", 1], ["6928,20 N·m", 0]]);
});

test("exercice 2.2 : cases de torseur (valeur seule, signe compris)", () => {
  cas("exercice-torseurs", "q1_7_N", [["639,93", 1], ["639,9", 1], ["640", 0], ["-639,93", 0]]);
  cas("exercice-torseurs", "q2_3_N", [["40", 1], ["0", 0]]);
  cas("exercice-torseurs", "q3_5_L", [["720", 1], ["900", 0]]);
  cas("exercice-torseurs", "q3_1_Z", [["781,42", 1], ["-781,42", 0]]);
  cas("exercice-torseurs", "q5_4_L", [["-4,07", 1], ["4,07", 0]]);
  cas("exercice-torseurs", "q5_4_N", [["34", 1], ["34,00", 1], ["-34", 0]]);
  cas("exercice-torseurs", "q1_3", [["639,93 N·mm", 1], ["0,64 N·m", 1], ["639,93", 0.5]]);
});
