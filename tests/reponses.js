// Réponse juste déduite de la configuration d'une question (window.__QCFG__ d'une page d'exercice).
// Sert aux tests du moteur (Node) et aux parcours navigateur : un sujet entièrement juste doit donner 20/20.
"use strict";

function nombre(v) {
  return String(v).replace(".", ",");
}

function reponseJuste(g) {
  switch (g.type) {
    case "num": return nombre(g.value) + (g.unit ? " " + g.unit.label : "");
    case "expr": return g.expected;                       // l'expression attendue s'écrit avec les noms acceptés
    case "yesno": return g.value ? "oui" : "non";
    case "kw": return g.any[0].map(function (alts) { return alts[0]; }).join(" ");
    case "code": return (g.equals || g.contains)[0];
    case "intset": return g.value.join(", ");
    default: throw new Error("type sans réponse type : " + g.type);
  }
}

module.exports = { reponseJuste: reponseJuste };
