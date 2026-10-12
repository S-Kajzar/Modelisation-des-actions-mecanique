#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cours interactifs de la séquence « Modélisation des actions mécaniques : force, couple, torseur ».

    python3 src/construire_cours.py   # écrit src/cours/{modelisation,projection,couple-moment,torseur}-source.html
    python3 src/generer.py            # publie cours-*.html avec le lien de retour vers l'accueil

Construction reprise des cours du dépôt RDM : sections numérotées, formules encadrées, réponses « À toi » à
dévoiler, simulateurs à manipuler avec leurs défis, textes à trous, cartes à retourner, vérifications rapides,
exemples pas à pas et quiz final. Charte : bloc de style du gabarit, complété par src/cours/cours.css ;
comportements : src/cours/cours.js (aucune dépendance externe, page utilisable hors ligne).

  - Cours 1 (niveau 1) : modélisation des actions mécaniques — chapitre « Forces et actions mécaniques » ;
  - Cours 2 (niveau 1) : projection d'une force — pages 1 et 2 de la séquence ;
  - Cours 3 (niveau 1) : moments et couples — pages 5 et 6, enrichies du chapitre « Moments et couples » ;
  - Cours 4 (niveau 2) : torseur d'action mécanique — page 9.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commun import GABARIT, ROOT, esc, fig, figure, torseur_html  # noqa: E402
from figures_forces import schema, svg_ballon, svg_cable, svg_cable_coord, svg_contacts  # noqa: E402

COURS = ROOT / "src" / "cours"
HOUSE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.3" '
         'stroke-linejoin="round" stroke-linecap="round" width="18" height="18"><path d="M3 11.5 12 4l9 7.5"/>'
         '<path d="M5.5 9.8V20h4.5v-5.5h4V20h4.5V9.8"/></svg>')


def v(lettre):
    """Vecteur : lettre surmontée d'une flèche (classe .vec du gabarit)."""
    return f'<span class="vec">{lettre}</span>'


# ---------------------------------------------------------------- briques
def sec(n, ident, titre, body):
    return (f'<section class="part cours-sec" id="{ident}" aria-labelledby="{ident}-t"><header class="part-head">'
            f'<div class="part-num" aria-hidden="true">{n}</div><div><h2 id="{ident}-t">{titre}</h2></div></header>'
            f'<div class="part-body">{body}</div></section>')


def formule(main, units=""):
    u = f'<span class="f-units">{units}</span>' if units else ""
    return f'<div class="formule"><span class="f-main">{main}</span>{u}</div>'


def a_toi(question, reponse):
    return (f'<details class="a-toi"><summary>À toi : {question} Clique ensuite pour vérifier.</summary>'
            f'<div>{reponse}</div></details>')


def check(question, ans, tol, why, unite=""):
    return (f'<div class="check" data-ans="{ans}" data-tol="{tol}" data-why="{esc(why)}"><span>{question}</span>'
            f'<input type="text" inputmode="decimal" aria-label="Ta réponse" autocomplete="off"> {unite} '
            f'<button type="button" class="btn ghost">Vérifier</button><span class="check-fb" aria-live="polite"></span></div>')


def sel(ok, options):
    opts = "".join(f'<option value="{esc(o)}">{o}</option>' for o in options)
    return f'<select data-ok="{esc(ok)}" aria-label="Choisis"><option value="">…</option>{opts}</select>'


def trous(html):
    return (f'<div class="trous">{html}<div class="trous-foot"><button type="button" class="btn trous-ok">Vérifier</button>'
            '<button type="button" class="btn ghost trous-sol">Afficher la solution</button>'
            '<b class="trous-s" aria-live="polite"></b></div></div>')


def cartes(items):
    return '<div class="cartes">' + "".join(
        f'<button type="button" class="carte" aria-expanded="false"><b>{t}</b><span class="dos">{d}</span></button>'
        for t, d in items) + "</div>"


def stepper(titre, items):
    lis = "".join(f"<li>{x}</li>" for x in items)
    return (f'<div class="exemple stepper"><h3>{titre}</h3><ol>{lis}</ol><div class="stepper-foot">'
            '<button type="button" class="btn st-next">Étape suivante</button>'
            '<button type="button" class="btn ghost st-all">Tout afficher</button>'
            '<button type="button" class="btn ghost st-reset">Recommencer</button></div></div>')


def quiz(prefix, questions):
    qs = "".join(
        f'<fieldset class="quiz-q" data-ok="{ok}"><legend><span class="q-num">{i + 1}</span> {q}</legend>' +
        "".join(f'<label><input type="radio" name="{prefix}{i}" value="{j}"> {o}</label>' for j, o in enumerate(opts)) +
        f'<p class="quiz-fb" aria-live="polite"></p><p class="quiz-why" hidden>{why}</p></fieldset>'
        for i, (q, opts, ok, why) in enumerate(questions))
    return (f'<div class="quiz-bloc"><p>Choisis une réponse : la correction s\'affiche aussitôt.</p><div class="quiz">{qs}</div>'
            '<div class="quiz-score" aria-live="polite"><span class="qz-score"></span><span class="qz-stars" aria-hidden="true">'
            '</span><span class="qz-msg small"></span><button type="button" class="btn ghost qz-reset">Recommencer</button></div></div>')


def simu(widget, titre, svg, controles, sorties, defi="", aide=""):
    aide = f'<p class="simu-aide">{aide}</p>' if aide else ""
    defi = f'<div class="defi">{defi}</div>' if defi else ""
    return (f'<div class="simu" data-widget="{widget}"><h3>{titre}</h3><div class="simu-corps"><div>{svg}{aide}</div>'
            f'<div class="simu-grid">{controles}<div class="simu-out">{sorties}</div>{defi}</div></div></div>')


def curseur(cle, label, mn, mx, pas, val, sortie):
    return (f'<label><span>{label} : <output data-o="{sortie}"></output></span>'
            f'<input type="range" data-in="{cle}" min="{mn}" max="{mx}" step="{pas}" value="{val}"></label>')


def img(nom, alt, w, cap=""):
    return figure(fig("sequence/" + nom, alt, w, cap))


def page(*, fichier, titre, description, tag, niveau, sous_titre, objectif, prerequis, nav, sections, liens):
    g = GABARIT.read_text(encoding="utf-8")
    s0 = g.index("<style>:root{")
    styles = g[s0:g.index("</head>")]          # bloc du gabarit + extensions (méthode, torseurs…)
    css = (COURS / "cours.css").read_text(encoding="utf-8")
    js = (COURS / "cours.js").read_text(encoding="utf-8")
    pastille = f'<span class="pastille{" n2" if niveau == 2 else ""}">Niveau {niveau}</span>'
    navh = "".join(f'<a href="#{a}">{i}. {t}</a>' for i, (a, t) in enumerate(nav, 1))
    lh = "".join(f'<a class="btn" href="{h}">{t}</a>' for h, t in liens)
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page construite par src/construire_cours.py : ne pas modifier à la main. -->
<title>{titre} — cours interactif</title>
<meta name="description" content="{esc(description)}">
{styles}<style>
{css}</style>
</head>
<body class="cours-page">
<div class="lecture" aria-hidden="true"></div>
<main class="page cours">
<header class="cours-tete"><span class="mc-tag">{tag}</span>{pastille}<h1>{titre}</h1><p>{sous_titre}</p></header>
<div class="cours-cadre"><div><h2>Objectif</h2><ul><li>{objectif}</li></ul></div><div><h2>Prérequis</h2><ul><li>{prerequis}</li></ul></div></div>
<nav class="cours-nav no-print" aria-label="Étapes du cours">{navh}</nav>
{"".join(sections)}
<div class="cours-foot no-print"><span class="small">S'entraîner :</span> {lh}
<button type="button" class="btn ghost cours-print">Imprimer le cours</button>
<a class="btn ghost" href="index.html">{HOUSE} Retour à l'accueil</a></div>
</main>
<script>
{js}</script>
</body>
</html>
"""
    sortie = COURS / fichier
    sortie.write_text(html, encoding="utf-8")
    print(f"{sortie.relative_to(ROOT)} : {len(html.encode('utf-8')) / 1024:.0f} Kio")


# =====================================================================================================================
# COURS 2 — PROJECTION D'UNE FORCE (pages 1 et 2)
# =====================================================================================================================
NOEUDS = [("Accélération", 120, 52, "#E2A3A2", "dynamique"), ("Effort", 360, 60, "#F9C49A", "statique dynamique rdm"),
          ("Matériaux", 590, 114, "#CFC8A6", "rdm"), ("Vitesse", 96, 182, "#9BD2E0", "cinematique dynamique"),
          ("Géométrie", 360, 206, "#C8DCA4", "statique cinematique dynamique rdm")]
LIENS = [((120, 52), (360, 60), "dynamique"), ((120, 52), (96, 182), "dynamique"),
         ((96, 182), (360, 206), "cinematique dynamique"), ((360, 60), (360, 206), "statique dynamique rdm"),
         ((360, 60), (590, 114), "rdm"), ((360, 206), (590, 114), "rdm")]
DISCIPLINES = [("statique", "Statique", 405, 136,
                "Relation entre les <b>efforts</b> et la <b>géométrie</b> d'un système immobile : on écrit son "
                "équilibre. C'est le cœur de cette séquence : avant d'écrire un équilibre, il faut savoir "
                "<b>modéliser les actions mécaniques</b>."),
               ("cinematique", "Cinématique", 224, 236,
                "Étude des mouvements — trajectoires, <b>vitesses</b> — à partir de la <b>géométrie</b> du "
                "mécanisme, sans s'occuper des efforts qui les provoquent."),
               ("dynamique", "Dynamique", 70, 120,
                "Relie les <b>efforts</b> aux <b>accélérations</b> qu'ils provoquent, donc aux variations de "
                "<b>vitesse</b> : c'est le principe fondamental de la dynamique."),
               ("rdm", "Résistance des matériaux", 555, 186,
                "Relie les <b>efforts</b> appliqués, la <b>géométrie</b> des pièces et leur <b>matériau</b> pour "
                "prévoir les déformations et vérifier qu'une pièce résiste.")]


def carte_disciplines():
    liens = "".join(f'<line class="lien" data-d="{d}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a, b, d in LIENS)
    noeuds = "".join(f'<g class="noeud" data-d="{d}"><ellipse cx="{x}" cy="{y}" rx="76" ry="30" fill="{c}"/>'
                     f'<text x="{x}" y="{y + 5}">{t}</text></g>' for t, x, y, c, d in NOEUDS)
    disc = "".join(f'<text class="disc" data-d="{k}" x="{x}" y="{y}">{t}</text>' for k, t, x, y, _ in DISCIPLINES)
    btns = "".join(f'<button type="button" class="carte-btn" data-d="{k}" aria-pressed="false">{t}</button>'
                   for k, t, *_r in DISCIPLINES)
    txt = "".join(f'<p data-d="{k}" hidden>{d}</p>' for k, _t, _x, _y, d in DISCIPLINES)
    return (f'<div class="simu" data-widget="disciplines"><h3>Les grandes branches de la mécanique</h3>'
            f'<div class="disc-corps"><div><svg class="carte-svg" viewBox="0 0 680 256" role="img" '
            f'aria-label="Carte reliant accélération, effort, matériaux, vitesse et géométrie par la dynamique, la '
            f'statique, la cinématique et la résistance des matériaux">{liens}{noeuds}{disc}</svg></div>'
            f'<div><p class="cours-defi">À toi : clique sur chaque discipline.</p>'
            f'<div class="simu-choix carte-choix">{btns}</div><div class="carte-txt">'
            f'<p data-d="" class="small">Chaque discipline relie certaines grandeurs : choisis-en une pour les voir '
            f's\'allumer.</p>{txt}</div></div></div></div>')


QUIZ_1 = [
    ("A (1 ; 2) et B (4 ; 6). Le vecteur AB a pour coordonnées…", ["(3 ; 4)", "(5 ; 8)", "(−3 ; −4)"], 0,
     "AB = (x<sub>B</sub> − x<sub>A</sub> ; y<sub>B</sub> − y<sub>A</sub>) = (4 − 1 ; 6 − 2) = (3 ; 4)."),
    ("La norme du vecteur u (3 ; 4) vaut…", ["7", "5", "25"], 1, "‖u‖ = √(3² + 4²) = √25 = 5."),
    ("Dans un triangle rectangle, cos A est égal à…", ["côté adjacent / hypoténuse", "côté opposé / hypoténuse",
                                                      "côté opposé / côté adjacent"], 0, "CAH : Cosinus = Adjacent / Hypoténuse."),
    ("F = 200 N est inclinée de 60° sur l'axe x. F<sub>x</sub> vaut…", ["173,21 N", "100 N", "200 N"], 1,
     "F<sub>x</sub> = F cos 60° = 200 × 0,5 = 100 N."),
    ("Même force : F<sub>y</sub> vaut…", ["100 N", "115,47 N", "173,21 N"], 2, "F<sub>y</sub> = F sin 60° = 200 × 0,866 ≈ 173,21 N."),
    ("F = 100 N est inclinée de β = 30° sur l'axe vertical, vers la gauche (comme dans le cours). F<sub>x</sub> vaut…",
     ["50 N", "−50 N", "−86,6 N"], 1, "F<sub>x</sub> = −F sin β = −100 × 0,5 = −50 N : la projection pointe vers x'."),
    ("Une force pointe vers la gauche et vers le bas. Les signes de (F<sub>x</sub> ; F<sub>y</sub>) sont…",
     ["(+ ; −)", "(− ; +)", "(− ; −)"], 2, "Vers la gauche : F<sub>x</sub> &lt; 0 ; vers le bas : F<sub>y</sub> &lt; 0."),
    ("F<sub>x</sub> = 300 N et F<sub>y</sub> = 400 N. L'intensité F vaut…", ["700 N", "500 N", "350 N"], 1,
     "F = √(300² + 400²) = √250 000 = 500 N : on n'additionne jamais directement les coordonnées."),
]


def cours_projection():
    s1 = sec(1, "c1-meca", "Pourquoi modéliser les actions mécaniques ?",
             "<p>Le comportement mécanique d'une structure est conditionné par une <b>géométrie</b>, un ou des "
             "<b>matériaux</b>, des <b>mouvements</b>, des <b>efforts</b> appliqués et des déformations qui en découlent. "
             "Prédire et maîtriser le comportement mécanique d'un système, c'est maîtriser la relation entre tous ces "
             "éléments.</p>" + carte_disciplines() +
             "<p>Toutes ces disciplines manipulent des <b>forces</b>, que l'on représente par des <b>vecteurs</b>. Ce "
             "premier cours rappelle les outils mathématiques pour décrire une force par ses <b>coordonnées</b>.</p>")
    rep = ('<svg viewBox="0 0 460 320" role="img" aria-label="Repère (O, i, j) quadrillé ; points A et B déplaçables ; '
           'vecteur AB et ses deux composantes"></svg>')
    s2 = sec(2, "c1-coord", "Coordonnées d'un vecteur dans un repère",
             "<div class=\"cours-split\"><div><p>Le plan étant muni d'un repère (O, " + v("i") + ", " + v("j") + "), "
             "soit " + v("u") + " un vecteur donné et M le point du plan tel que " + v("OM") + " = " + v("u") + ".</p>"
             "<p>Si on note (x ; y) les coordonnées de M, alors :</p>" +
             formule(v("OM") + " = " + v("u") + " = x " + v("i") + " + y " + v("j")) +
             "<p><b>Propriété</b> : soient les points O (x<sub>O</sub> ; y<sub>O</sub>) et M (x<sub>M</sub> ; "
             "y<sub>M</sub>). Le vecteur " + v("OM") + " a pour coordonnées :</p>" +
             formule(v("OM") + " (x<sub>M</sub> − x<sub>O</sub> ; y<sub>M</sub> − y<sub>O</sub>)",
                     "« arrivée moins départ », coordonnée par coordonnée") + "</div></div>" +
             simu("repere", "Simulateur : déplace les points A et B", rep,
                  "<p class=\"small\">Fais glisser A et B (ou sélectionne-les et utilise les flèches du clavier). "
                  "Les points s'accrochent au quadrillage.</p>",
                  '<div><span>Point A</span><b data-o="A"></b></div><div><span>Point B</span><b data-o="B"></b></div>'
                  '<div><span>Coordonnées de AB</span><b data-o="AB"></b></div><div><span>Décomposition</span><b data-o="dec"></b></div>'
                  '<div><span>Norme ‖AB‖</span><b data-o="n"></b></div>',
                  defi="<b>Défi :</b> place A et B pour que ‖AB‖ = 5 exactement, avec deux coordonnées non nulles. "
                       "<span class=\"defi-ok\" aria-live=\"polite\"></span>") +
             check("A (2 ; 7) et B (5 ; 3). Que vaut la coordonnée y du vecteur AB ?", -4, 0.001,
                   "y<sub>B</sub> − y<sub>A</sub> = 3 − 7 = −4 : de A vers B, on descend de 4."))
    s3 = sec(3, "c1-norme", "Norme d'un vecteur",
             "<p>La norme du vecteur " + v("u") + ", c'est-à-dire sa longueur, se calcule par la relation de "
             "<b>Pythagore</b> : les deux coordonnées sont les côtés de l'angle droit, le vecteur est l'hypoténuse.</p>" +
             a_toi("complète la formule ‖" + v("u") + "‖ = … sur ta feuille.",
                   formule("‖" + v("u") + "‖ = √(x² + y²)", "pour une force : F = √(F<sub>x</sub>² + F<sub>y</sub>²)")) +
             check("Calcule la norme du vecteur u (6 ; 8).", 10, 0.001, "√(6² + 8²) = √(36 + 64) = √100 = 10.") +
             check("Calcule la norme du vecteur AB (3 ; −4).", 5, 0.001,
                   "√(3² + (−4)²) = √(9 + 16) = 5 : le signe disparaît, (−4)² = 16."))
    tri = ('<svg viewBox="0 0 460 300" role="img" aria-label="Triangle rectangle ABC, rectangle en C, d\'angle A '
           'réglable : côté adjacent, côté opposé et hypoténuse"></svg>')
    rapports = trous(
        "<p>cos(A) = <span class=\"frac\"><span>" + sel("côté adjacent", ["côté adjacent", "côté opposé", "hypoténuse"]) +
        "</span><span>" + sel("hypoténuse", ["côté adjacent", "côté opposé", "hypoténuse"]) + "</span></span></p>"
        "<p>sin(A) = <span class=\"frac\"><span>" + sel("côté opposé", ["côté adjacent", "côté opposé", "hypoténuse"]) +
        "</span><span>" + sel("hypoténuse", ["côté adjacent", "côté opposé", "hypoténuse"]) + "</span></span></p>"
        "<p>tan(A) = <span class=\"frac\"><span>" + sel("côté opposé", ["côté adjacent", "côté opposé", "hypoténuse"]) +
        "</span><span>" + sel("côté adjacent", ["côté adjacent", "côté opposé", "hypoténuse"]) + "</span></span></p>")
    s4 = sec(4, "c1-trigo", "Relations trigonométriques",
             "<p>Par définition, le <b>sinus</b>, le <b>cosinus</b> et la <b>tangente</b> de l'angle aigu de sommet A "
             "du triangle rectangle ABC (rectangle en C) sont des rapports de longueurs.</p>"
             "<p class=\"cours-defi\">À toi : complète les trois rapports, puis vérifie.</p>" + rapports +
             '<div class="remarque"><p><b>Moyen mnémotechnique : CAH SOH TOA</b> — <b>C</b>osinus = <b>A</b>djacent / '
             '<b>H</b>ypoténuse ; <b>S</b>inus = <b>O</b>pposé / <b>H</b>ypoténuse ; <b>T</b>angente = <b>O</b>pposé / '
             '<b>A</b>djacent.</p></div>' +
             simu("trigo", "Simulateur : fais varier l'angle et la taille du triangle", tri,
                  curseur("a", "Angle A", 5, 85, 1, 35, "a") + curseur("h", "Hypoténuse (cm)", 2, 10, 0.5, 8, "h"),
                  '<div><span>cos A = adjacent / hypoténuse</span><b data-o="cos"></b></div>'
                  '<div><span>sin A = opposé / hypoténuse</span><b data-o="sin"></b></div>'
                  '<div><span>tan A = opposé / adjacent</span><b data-o="tan"></b></div>',
                  defi="<b>Défis :</b> trouve l'angle pour lequel le côté opposé est égal au côté adjacent. "
                       "<span class=\"defi-ok\" data-defi=\"45\"></span><br>Trouve l'angle pour lequel sin A = 0,5. "
                       "<span class=\"defi-ok\" data-defi=\"30\"></span>",
                  aide="Change la taille de l'hypoténuse : les rapports ne bougent pas. Ils ne dépendent que de l'angle.") +
             check("Hypoténuse de 10 cm, angle A = 30°. Combien mesure le côté opposé à A (en cm) ?", 5, 0.01,
                   "Côté opposé = hypoténuse × sin A = 10 × sin 30° = 10 × 0,5 = 5 cm.", "cm"))
    pro = ('<svg viewBox="0 0 460 380" role="img" aria-label="Repère (O, x, y) ; force F réglable et ses projections '
           'Fx sur x et Fy sur y"></svg>')
    s5 = sec(5, "c1-proj", "Projection d'un vecteur force",
             "<div class=\"cours-split\"><div><p>Soit une force " + v("F") + " inclinée d'un angle α par rapport à l'axe "
             "horizontal dans un repère (O, " + v("i") + ", " + v("j") + ").</p>"
             "<p>La coordonnée <b style=\"color:#B42318\">F<sub>x</sub></b> correspond à la projection du vecteur force "
             + v("F") + " sur l'axe des abscisses ; la coordonnée <b style=\"color:#1F5FA8\">F<sub>y</sub></b>, à sa "
             "projection sur l'axe des ordonnées.</p></div></div>" +
             a_toi("écris F<sub>x</sub> et F<sub>y</sub> en fonction de ‖" + v("F") + "‖ et de α.",
                   formule("F<sub>x</sub> = ‖" + v("F") + "‖ × cos α &nbsp; soit &nbsp; F<sub>x</sub> = F cos α") +
                   formule("F<sub>y</sub> = ‖" + v("F") + "‖ × sin α &nbsp; soit &nbsp; F<sub>y</sub> = F sin α",
                           "F<sub>x</sub> est le côté adjacent à α, F<sub>y</sub> le côté opposé")) +
             "<h3>Cas d'un vecteur ayant une coordonnée négative</h3><p>Soit une force " + v("F") + " inclinée d'un "
             "angle β par rapport à l'axe vertical, vers la gauche, dans le repère (O, " + v("i") + ", " + v("j") + ").</p>" +
             a_toi("écris F<sub>x</sub> et F<sub>y</sub> en fonction de F et de β.",
                   formule("F<sub>x</sub> = −‖" + v("F") + "‖ × sin β &nbsp; soit &nbsp; F<sub>x</sub> = −F sin β",
                           "côté opposé à β, la projection pointe vers x' : signe −") +
                   formule("F<sub>y</sub> = ‖" + v("F") + "‖ × cos β &nbsp; soit &nbsp; F<sub>y</sub> = F cos β",
                           "côté adjacent à β")) +
             simu("projection", "Simulateur : projette une force", pro,
                  '<div class="simu-choix" role="group" aria-label="Angle de référence">'
                  '<button type="button" data-mode="alpha" aria-pressed="true">α depuis l\'axe x</button>'
                  '<button type="button" data-mode="beta" aria-pressed="false">β depuis l\'axe y</button></div>' +
                  curseur("F", "Intensité F", 0, 1000, 10, 500, "F") +
                  '<label><span><span data-o="nom"></span> : <output data-o="ang"></output></span>'
                  '<input type="range" data-in="ang" min="-180" max="180" step="1" value="30"></label>',
                  '<div class="simu-calc"><p data-o="fx"></p><p data-o="fy"></p></div>'
                  '<p class="small" data-o="signe"></p><p class="small" data-o="verif"></p>',
                  defi="<b>Défis :</b> trouve un angle α pour lequel F<sub>x</sub> = F<sub>y</sub>. "
                       "<span class=\"defi-ok\" data-defi=\"egal\"></span><br>Trouve un réglage pour lequel "
                       "F<sub>x</sub> &lt; 0 et F<sub>y</sub> &gt; 0. <span class=\"defi-ok\" data-defi=\"signe\"></span>",
                  aide="Fais glisser l'extrémité jaune de la force, ou utilise les curseurs.") +
             '<div class="remarque"><p><b>Le signe se lit sur la figure</b> : une coordonnée est positive si la '
             "projection pointe dans le sens de l'axe, négative sinon. Vérifie toujours que F<sub>x</sub>² + "
             "F<sub>y</sub>² = F².</p></div>" +
             stepper("Exemple résolu : une corde tirée vers le bas", [
                 "Une corde exerce une force F = 400 N, inclinée de 25° <b>sous</b> l'axe x, vers la droite.",
                 "L'angle est mesuré depuis l'axe x : F<sub>x</sub> est le côté adjacent, F<sub>y</sub> le côté opposé.",
                 "F<sub>x</sub> = F cos 25° = 400 × 0,906 ≈ <b>362,52 N</b>, positive : la projection pointe vers la droite.",
                 "F<sub>y</sub> = −F sin 25° = −400 × 0,423 ≈ <b>−169,05 N</b>, négative : la force tire vers le bas.",
                 "Vérification : √(362,52² + 169,05²) ≈ 400 N. ✔"]) +
             check("F = 250 N, inclinée de α = 40° sur l'axe x. Calcule F<sub>x</sub> au centième (en N).", 191.51, 0.01,
                   "F<sub>x</sub> = 250 × cos 40° ≈ 191,51 N.", "N"))
    s6 = sec(6, "c1-quiz", "Quiz : vérifie tes connaissances", quiz("q1-", QUIZ_1))
    page(fichier="projection-source.html", titre="Projection d'une force", tag="Cours 2", niveau=1,
         description="Cours interactif : coordonnées d'un vecteur, norme, relations trigonométriques et projection d'une "
                     "force sur les axes d'un repère, avec simulateurs et quiz.",
         sous_titre="Décrire une force par ses coordonnées : vecteur, norme, trigonométrie et projection sur les axes. "
                    "Environ 30 minutes : manipule les figures, relève les défis, puis teste-toi avec le quiz.",
         objectif="Écrire les coordonnées d'un vecteur force.", prerequis="Cours 1 : le vecteur-force ; mathématiques : notion de vecteur.",
         nav=[("c1-meca", "La mécanique"), ("c1-coord", "Coordonnées"), ("c1-norme", "Norme"), ("c1-trigo", "Trigonométrie"),
              ("c1-proj", "Projection"), ("c1-quiz", "Quiz")],
         sections=[s1, s2, s3, s4, s5, s6],
         liens=[("exercice-projections.html", "Exercice 1.2 — Projections d'une force"),
                ("exercice-quadrants.html", "Exercice 1.3 — Les quatre quadrants")])


# =====================================================================================================================
# COURS 3 — MOMENTS ET COUPLES (pages 5 et 6 de la séquence, enrichies du chapitre « Moments et couples »)
# =====================================================================================================================
QUIZ_2 = [
    ("Le moment d'une force s'exprime en…", ["N", "N·m", "N/m"], 1, "Une force (N) multipliée par une distance (m)."),
    ("Une poussée dont la droite d'action passe par le centre de gravité G de la navette provoque…",
     ["une translation seule", "une rotation seule", "une translation et une rotation"], 0,
     "Le moment en G est nul : pas de rotation, la navette avance en ligne droite."),
    ("Une force de 50 N, perpendiculaire à une clé de 0,3 m, crée un couple de…", ["15 N·m", "166,7 N·m", "50,3 N·m"], 0,
     "M = F × d = 50 × 0,3 = 15 N·m."),
    ("Même clé, même force, mais inclinée de 30° sur la clé :", ["15 N·m", "13 N·m", "7,5 N·m"], 2,
     "M = F × AB × sin α = 50 × 0,3 × sin 30° = 7,5 N·m : la force est moins efficace."),
    ("Une rotation dans le sens horaire correspond à un moment…", ["positif", "négatif", "nul"], 1,
     "Convention : sens trigonométrique positif, sens horaire négatif."),
    ("Le théorème de Varignon dit que le moment d'une force est égal…",
     ["à la somme des moments de ses composantes", "au produit de ses composantes", "à la norme de la force"], 0,
     "M<sub>A</sub>(F) = M<sub>A</sub>(U) + M<sub>A</sub>(V) : pratique quand le bras de levier est difficile à trouver."),
    ("AB = (0,2 ; 0 ; 0) m et F = (0 ; 100 ; 0) N. M<sub>A</sub>(F) = AB ∧ F vaut…",
     ["(0 ; 0 ; 20) N·m", "(0 ; 0 ; −20) N·m", "(20 ; 0 ; 0) N·m"], 0,
     "Sur z : x<sub>AB</sub> y<sub>F</sub> − y<sub>AB</sub> x<sub>F</sub> = 0,2 × 100 − 0 = 20 N·m."),
    ("Deux forces opposées de 30 N, distantes de 0,5 m : leur couple vaut, en n'importe quel point O…",
     ["15 N·m", "0", "60 N·m"], 0, "M = F × d = 30 × 0,5 = 15 N·m, quel que soit O."),
    ("Un couple de 50 N·m peut être obtenu avec…", ["25 N à 2 m", "25 N à 0,5 m", "100 N à 2 m"], 0,
     "M = F × d : 25 × 2 = 50 N·m. Seul le produit compte."),
    ("Pour serrer plus fort sans forcer davantage, on…", ["raccourcit la clé", "allonge la clé", "incline la force vers la clé"],
     1, "Un bras de levier plus long donne un moment plus grand pour la même force."),
]


def cours_couple():
    nav_svg = ('<svg viewBox="0 0 560 260" role="img" aria-label="Navette spatiale vue de profil, centre de gravité G, '
               'poussée F des moteurs à l\'arrière, décalée de d par rapport à G"></svg>')
    s1 = sec(1, "c2-navette", "Pourquoi le moment ?",
             "<p>Les effets d'une force sur un solide dépendent non seulement de son intensité et de sa direction, mais "
             "aussi du <b>moment</b> qu'elle peut engendrer. Le moment d'une force mesure son aptitude à faire "
             "<b>tourner</b> l'objet sur lequel elle agit.</p><p>Exemple : la navette spatiale, au repos dans l'espace, "
             "est poussée par ses moteurs (force " + v("F") + ").</p><ul><li><b>Cas 1</b> : si " + v("F") + " passe par "
             "le centre de gravité G, la navette est animée d'un mouvement de <b>translation</b> rectiligne, de même "
             "direction et de même sens que " + v("F") + ".</li><li><b>Cas 2</b> : si " + v("F") + " ne passe pas par G, "
             "elle est à la fois animée d'une <b>translation</b> et d'une <b>rotation</b> autour de G. L'importance de "
             "la rotation dépend de la distance d entre G et la droite d'action de " + v("F") + ".</li></ul>" +
             simu("navette", "Simulateur : pilote la navette", nav_svg,
                  curseur("F", "Poussée F", 100, 1000, 50, 600, "F") + curseur("d", "Décalage d de la poussée", -1.5, 1.5, 0.05, 0.8, "d") +
                  '<p><button type="button" class="btn nav-go">Allumer les moteurs</button></p>',
                  '<div class="simu-calc"><p data-o="M"></p></div><p class="simu-verdict" data-o="cas" aria-live="polite"></p>',
                  aide="Ramène d à 0 : la poussée passe par G et la navette file droit. Plus d est grand, plus elle tourne."))
    s2 = sec(2, "c2-action", "Action mécanique : force et moment",
             "<p>On appelle <b>actions mécaniques</b> toute cause susceptible de maintenir un corps en équilibre, de "
             "créer ou de modifier un mouvement de ce corps, et de déformer un corps.</p>"
             "<p>La force de l'action mécanique peut créer un mouvement de rotation autour d'un point ou d'un axe. "
             "<b>Le moment d'une force</b> par rapport à ce point est une grandeur physique vectorielle traduisant "
             "l'aptitude de cette force à faire tourner un système mécanique autour de ce point. Il s'exprime en "
             "<b>N·m</b> (newton-mètre). Lorsque la rotation se fait <b>autour d'un axe</b>, le moment est appelé "
             "<b>couple</b>.</p>"
             '<div class="remarque"><p><b>Expérience</b> : pousse une porte tout près de ses gonds, puis près de la '
             "poignée. Même force, effet très différent : c'est la <b>distance</b> à l'axe qui change le moment.</p></div>"
             "<p class=\"cours-defi\">À toi : complète la phrase, puis vérifie.</p>" +
             trous("<p>Une action mécanique se modélise par deux vecteurs :</p><ul><li>la " +
                   sel("force", ["force", "moment"]) + " qui engendre un mouvement de " +
                   sel("translation", ["translation", "rotation"]) + " et s'exprime en " +
                   sel("newtons (N)", ["newtons (N)", "newtons-mètres (N·m)", "mètres (m)"]) + " ;</li><li>le " +
                   sel("moment", ["force", "moment"]) + " qui engendre un mouvement de " +
                   sel("rotation", ["translation", "rotation"]) + " et s'exprime en " +
                   sel("newtons-mètres (N·m)", ["newtons (N)", "newtons-mètres (N·m)", "mètres (m)"]) + ".</li></ul>"))
    cle = ('<svg viewBox="0 0 520 300" role="img" aria-label="Clé plate vue de dessus : écrou en O, force F en A '
           'inclinée de α sur la clé, bras de levier d en jaune"></svg>')
    s3 = sec(3, "c2-calcul", "Moment d'une force par rapport à un point",
             "<p>Le moment de la force " + v("F") + " par rapport au point A, noté M<sub>A</sub>(" + v("F") + "), est égal "
             "au produit de F par le <b>bras de levier</b> d, distance entre A et la droite d'action de " + v("F") + " :</p>" +
             formule("M<sub>A</sub>(" + v("F") + ") = F × d", "d = AH, H pied de la perpendiculaire menée de A<br>"
                     "M en N·m, F en N, d en m") +
             '<div class="remarque"><p><b>Convention de signe</b> : si F fait tourner le solide autour de A dans le '
             "<b>sens trigonométrique</b>, le moment est <b>positif</b> ; dans le sens horaire, il est <b>négatif</b>.</p></div>" +
             check("Exemple 1 : F<sub>1</sub> = 240 N à d<sub>1</sub> = 0,1 m fait tourner le solide dans le sens "
                   "trigonométrique autour de A ; F<sub>2</sub>, à d<sub>2</sub> = 0,12 m, le fait tourner dans le sens "
                   "horaire. Quelle intensité F<sub>2</sub> (en N) annule le moment total en A ?", 200, 0.01,
                   "M<sub>A</sub>(F<sub>1</sub>) + M<sub>A</sub>(F<sub>2</sub>) = 240 × 0,1 − 0,12 F<sub>2</sub> = 0, d'où "
                   "F<sub>2</sub> = 24 / 0,12 = 200 N.", "N") +
             "<h3>Avec le point d'application</h3><div class=\"cours-split\"><div><p>Si B est le point d'application de "
             + v("F") + " et si la longueur AB est connue, on remarque que AB × sin α = d, d'où :</p>" +
             formule("M<sub>A</sub>(" + v("F") + ") = F × AB × sin α", "α : angle entre AB et la force") +
             "<p>Exemple de l'écrou serré avec une clé : le couple de serrage est d'autant plus élevé que la distance "
             "est grande, que la force est importante et que l'angle α se rapproche de 90° (couple nul pour α = 0° "
             "et 180°).</p></div>" +
             img("c-cle.png", "Clé plate serrant un écrou en O ; force F en A inclinée de α par rapport à la clé", 420) +
             "</div>" +
             simu("cle", "Simulateur : serre l'écrou", cle,
                  curseur("F", "Force F", 0, 200, 1, 100, "F") + curseur("L", "Longueur OA", 100, 400, 10, 250, "L") +
                  curseur("a", "Angle α", 0, 180, 1, 60, "a"),
                  '<div class="simu-calc"><p data-o="d"></p><p data-o="M"></p></div><p class="small" data-o="sens"></p>'
                  '<div><span>Couple de serrage (repère rouge : objectif 30 N·m)</span><div class="jauge"><div class="jauge-bar">'
                  '</div><div class="jauge-cible"></div></div></div>',
                  defi="<b>Défi :</b> serre l'écrou à 30 N·m avec la plus petite force possible. "
                       "<span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="En jaune, le bras de levier d : la distance de O à la droite d'action de F (en pointillés).") +
             a_toi("clé à molette : la main exerce 100 N à 0,2 m du centre de l'écrou. Calcule le couple de serrage pour "
                   "α = 90°, 60°, 30° et 0°.",
                   "<p>M = 100 × 0,2 × sin α = 20 sin α : <b>20 N·m</b> à 90°, <b>17,32 N·m</b> à 60°, <b>10 N·m</b> à 30°, "
                   "<b>0</b> à 0°. Plus la main est inclinée, plus le couple diminue : la position la plus efficace est "
                   "α = 90°. Les clés dynamométriques permettent des serrages contrôlés et mesurés.</p>") +
             check("Clé de 0,25 m, force de 120 N perpendiculaire à la clé : que vaut le couple (en N·m) ?", 30, 0.01,
                   "M = F × d = 120 × 0,25 = 30 N·m.", "N·m"))
    s4 = sec(4, "c2-varignon", "Théorème de Varignon",
             "<p>Le moment de la force " + v("F") + " au point A est égal à la <b>somme des moments de ses composantes</b> "
             + v("U") + " et " + v("V") + " par rapport au même point.</p>" +
             formule("M<sub>A</sub>(" + v("F") + ") = M<sub>A</sub>(" + v("U") + ") + M<sub>A</sub>(" + v("V") + ")",
                     "avec les composantes sur x et y : M<sub>A</sub>(F) = −F<sub>x</sub> × d<sub>y</sub> + F<sub>y</sub> × d<sub>x</sub>") +
             stepper("Exemple : une force de 1 000 N à 60°", [
                 "Une force F = 1 000 N, inclinée de 60° sur l'axe x, s'applique en B, situé à 160 mm à droite et à "
                 "100 mm au-dessus de A. Trouver d, la distance de A à la droite d'action, est difficile.",
                 "Composantes : F<sub>x</sub> = F cos 60° = 1 000 × 0,5 = 500 N ; F<sub>y</sub> = F sin 60° = 1 000 × "
                 "0,866 = 866 N.",
                 "F<sub>x</sub>, horizontale, passe à 0,1 m au-dessus de A et fait tourner dans le sens horaire : "
                 "M<sub>A</sub>(F<sub>x</sub>) = −500 × 0,1 = −50 N·m.",
                 "F<sub>y</sub>, verticale, passe à 0,16 m à droite de A et fait tourner dans le sens trigonométrique : "
                 "M<sub>A</sub>(F<sub>y</sub>) = 866 × 0,16 = 138,6 N·m.",
                 "Varignon : M<sub>A</sub>(F) = −50 + 138,6 = <b>88,6 N·m</b> = F × d, d'où d = 88,6 mm. Le calcul par "
                 "les composantes est ici plus simple que la recherche directe de d."]) +
             check("Même méthode : F<sub>x</sub> = 300 N passe à 0,2 m au-dessus de A (sens horaire) et F<sub>y</sub> = "
                   "400 N passe à 0,5 m à droite de A (sens trigonométrique). Que vaut M<sub>A</sub>(F) en N·m ?", 140, 0.01,
                   "−300 × 0,2 + 400 × 0,5 = −60 + 200 = 140 N·m.", "N·m"))
    s5 = sec(5, "c2-vecteur", "Le vecteur-moment",
             "<p>En statique ou en dynamique <b>dans l'espace</b>, le moment scalaire ne suffit plus : le moment d'une "
             "force est décrit par un <b>vecteur</b>, défini à partir d'un produit vectoriel. Soit B un point quelconque "
             "de la droite d'action de " + v("F") + " ; le moment en A de " + v("F") + " est :</p>" +
             formule(v("M") + "<sub>A</sub>(" + v("F") + ") = " + v("AB") + " ∧ " + v("F"),
                     "vecteur perpendiculaire à la fois à " + v("F") + " et à " + v("AB")) +
             img("c-moment.png", "Plan P contenant la force F appliquée en A et le point B ; H pied de la perpendiculaire "
                 "menée de B à la droite d'action ; vecteur moment en B dessiné avec une double flèche", 480,
                 "Pour distinguer une force d'un moment, on dessine ce dernier avec une <b>double flèche</b>.") +
             "<p class=\"cours-defi\">À toi : retourne chaque carte.</p>" +
             cartes([("Son point d'application", "Le point par rapport auquel on calcule le moment : on écrit "
                      "M<sub>A</sub>(F)."),
                     ("Sa direction", "Perpendiculaire au plan qui contient " + v("AB") + " et " + v("F") + " : c'est l'axe de rotation."),
                     ("Son sens", "Règle des trois doigts de la main droite : pouce selon " + v("AB") + ", index selon " +
                      v("F") + ", le majeur donne le sens du moment. C'est aussi la règle du tire-bouchon."),
                     ("Son intensité", "‖M<sub>A</sub>(F)‖ = F × d = F × AB × sin α, en N·m.")]) +
             '<div class="remarque"><p>Le produit vectoriel n\'est <b>pas commutatif</b> : ' + v("AB") + " ∧ " + v("F") +
             " = −" + v("F") + " ∧ " + v("AB") + ". L'ordre compte : d'abord le vecteur position, ensuite la force.</p></div>")
    pv_rows = "".join(
        f'<tr><th>{c}</th><td><input type="text" data-v="a{c}" value="{a}" aria-label="{c} de AB"></td>'
        f'<td class="pv-op">{"∧" if c == "y" else ""}</td>'
        f'<td><input type="text" data-v="b{c}" value="{b}" aria-label="{c} de F"></td><td class="pv-op">{"=" if c == "y" else ""}</td>'
        f'<td class="res" data-r="{c}"></td></tr>'
        for c, a, b in [("x", "0", "−2000"), ("y", "0", "4000"), ("z", "0,05", "−1000")])
    pvect = (f'<div class="simu" data-widget="pvect"><h3>Calculateur : le produit vectoriel pas à pas</h3>'
             f'<div class="simu-choix" role="group" aria-label="Composante">'
             f'<button type="button" data-c="x" aria-pressed="true">Composante x</button>'
             f'<button type="button" data-c="y" aria-pressed="false">Composante y</button>'
             f'<button type="button" data-c="z" aria-pressed="false">Composante z</button></div>'
             f'<div style="overflow-x:auto"><table class="pv"><thead><tr><th></th><th>{v("AB")} (m)</th><th></th>'
             f'<th>{v("F")} (N)</th><th></th><th>{v("M")}<sub>A</sub> (N·m)</th></tr></thead><tbody>{pv_rows}</tbody></table></div>'
             f'<p class="simu-calc" data-o="detail"></p><p class="small" data-o="plan"></p>'
             f'<div class="simu-choix"><button type="button" data-preset="0 0 0.05 -2000 4000 -1000">Roue hélicoïdale</button>'
             f'<button type="button" data-preset="0.5 -0.3 0 500 -866 0">Poutre encastrée</button>'
             f'<button type="button" data-preset="0.2 0 0 0 100 0">Clé : AB sur x, F sur y</button></div>'
             f'<p class="simu-aide">Change les valeurs : en vert le produit qu\'on ajoute, en rouge celui qu\'on retranche.</p></div>')
    s6 = sec(6, "c2-coord", "Coordonnées du vecteur-moment, moment par rapport à un axe",
             "<p>Posons " + v("AB") + " = r<sub>x</sub> " + v("i") + " + r<sub>y</sub> " + v("j") + " + r<sub>z</sub> " +
             v("k") + " et " + v("F") + " = F<sub>x</sub> " + v("i") + " + F<sub>y</sub> " + v("j") + " + F<sub>z</sub> " +
             v("k") + ". Les composantes du produit vectoriel sont les différences des <b>produits en croix</b> :</p>" +
             a_toi("écris les trois composantes de " + v("AB") + " ∧ " + v("F") + ".",
                   formule(v("M") + "<sub>A</sub>(" + v("F") + ") = (r<sub>y</sub>F<sub>z</sub> − r<sub>z</sub>F<sub>y</sub> ; "
                           "r<sub>z</sub>F<sub>x</sub> − r<sub>x</sub>F<sub>z</sub> ; r<sub>x</sub>F<sub>y</sub> − r<sub>y</sub>F<sub>x</sub>)",
                           "pour la composante sur x, on cache la ligne x et on croise les lignes y et z")) + pvect +
             a_toi("poutre encastrée : AB = (0,5 ; −0,3 ; 0) m et F = (500 ; −866 ; 0) N (force de 1 000 N à 30° de la "
                   "verticale). Calcule M<sub>A</sub>(F), puis vérifie avec le bouton « Poutre encastrée ».",
                   "<p>Sur z : 0,5 × (−866) − (−0,3) × 500 = −433 + 150 = <b>−283 N·m</b> ; les composantes sur x et y "
                   "sont nulles. M<sub>A</sub>(F) = −283 " + v("k") + " N·m : rotation dans le sens horaire.</p>") +
             "<h3>Moment d'une force par rapport à un axe</h3><p>Le moment de " + v("F") + " par rapport à un axe de "
             "vecteur unitaire " + v("u") + " est le produit scalaire de " + v("u") + " par le vecteur-moment en un point A "
             "de l'axe : c'est la projection de " + v("M") + "<sub>A</sub>(" + v("F") + ") sur " + v("u") + ".</p>" +
             formule("M<sub>u</sub>(" + v("F") + ") = " + v("u") + " · " + v("M") + "<sub>A</sub>(" + v("F") + ")") +
             "<div class=\"cours-split\">" +
             img("c-roue-helicoidale.jpg", "Roue dentée à denture hélicoïdale : en A, la force F décomposée en Fa, Ft et Fr ; "
                 "x parallèle à l'axe u de la roue ; rayon r = 50 mm", 340) +
             "<div><p>Exemple de la roue dentée hélicoïdale : " + v("F") + " = −2 000 " + v("x") + " + 4 000 " + v("y") +
             " − 1 000 " + v("z") + " (N) et " + v("OA") + " = 0,05 " + v("z") + " (m), x parallèle à l'axe u de la roue.</p>" +
             a_toi("calcule M<sub>O</sub>(F), puis M<sub>u</sub>(F).",
                   formule(v("M") + "<sub>O</sub>(" + v("F") + ") = (−200 ; −100 ; 0) N·m") +
                   "<p>M<sub>u</sub>(F) = " + v("x") + " · M<sub>O</sub>(F) = <b>−200 N·m</b>. Des trois composantes de F, "
                   "seul l'effort tangentiel F<sub>t</sub> (4 000 N, orthogonal à u) fait tourner la roue : 4 000 × 0,05 "
                   "= 200 N·m. F<sub>a</sub>, parallèle à u, et F<sub>r</sub>, qui coupe u, n'interviennent pas.</p>") +
             "</div></div>")
    cp = ('<svg viewBox="0 0 520 260" role="img" aria-label="Disque soumis à deux forces opposées F et −F distantes de '
          'd ; point O déplaçable"></svg>')
    s7 = sec(7, "c2-couple", "Couple et vecteur-couple",
             "<p>Le moment engendré par <b>deux forces égales et opposées</b>, de lignes d'action différentes (non "
             "colinéaires), constitue un <b>couple</b> M. Son intensité F × d est <b>indépendante du point O</b> choisi : "
             "elle ne dépend que de la distance d entre les deux forces et de l'intensité F.</p>" +
             formule("M = M<sub>O</sub>(" + v("F") + ") + M<sub>O</sub>(−" + v("F") + ") = F × d",
                     "avec O à la distance a de −F : F(a + d) − F a = F d") +
             simu("couple", "Simulateur : déplace le point O", cp,
                  curseur("F", "Intensité F", 10, 100, 5, 50, "F") + curseur("d", "Distance d", 0.2, 2, 0.05, 1, "d"),
                  '<div class="simu-calc"><p data-o="mB"></p><p data-o="mA"></p><p data-o="M"></p></div>',
                  defi="<b>Défi :</b> place O sur la droite d'action de F. <span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="Où que soit O, les deux moments changent mais leur somme reste F × d.") +
             "<h3>Vecteur-couple et signes</h3><p>Soit A et B deux points quelconques des supports de −" + v("F") +
             " et de " + v("F") + " : " + v("M") + " = " + v("AB") + " ∧ " + v("F") + ", vecteur perpendiculaire au plan "
             "formé par " + v("F") + " et −" + v("F") + ", de norme AB × F × sin θ = F × d. Un <b>couple positif</b> "
             "fait tourner dans le sens trigonométrique.</p>" +
             '<div class="remarque"><p><b>Propriétés</b> : la valeur d\'un couple ne change pas si l\'on déplace F et −F '
             "dans des plans parallèles (d constant), si on les tourne en bloc dans leur plan, ou si on les fait glisser "
             "le long de leur support. Elle reste aussi la même si l'on modifie F et d en proportions inverses : "
             "M = F<sub>1</sub> d<sub>1</sub> = F<sub>2</sub> d<sub>2</sub>.</p></div>" +
             check("Couples équivalents : 50 N·m = 50 N × 1 m = 25 N × 2 m. Quelle force faut-il avec d = 0,4 m (en N) ?",
                   125, 0.01, "F = M / d = 50 / 0,4 = 125 N.", "N") +
             "<h3>Exemple : la clé à bougie</h3><p>Une clé à bougie a une tige de manœuvre coulissante de 0,4 m. Les mains "
             "exercent F et −F de 100 N à ses extrémités A et B ; E est l'axe de la bougie. Selon la position de la tige :</p>"
             '<div class="recap-wrap" style="padding:0"><table class="t"><thead><tr><th>Position</th><th>EB</th><th>EA</th>'
             "<th>M = F × EB + F × EA</th></tr></thead><tbody>"
             "<tr><td>1</td><td>0,2 m</td><td>0,2 m</td><td>100 × 0,2 + 100 × 0,2 = 40 N·m</td></tr>"
             "<tr><td>2</td><td>0,3 m</td><td>0,1 m</td><td>100 × 0,3 + 100 × 0,1 = 40 N·m</td></tr>"
             "<tr><td>3</td><td>0,15 m</td><td>0,25 m</td><td>100 × 0,15 + 100 × 0,25 = 40 N·m</td></tr>"
             "<tr><td>4</td><td>0 m</td><td>0,4 m</td><td>0 + 100 × 0,4 = 40 N·m</td></tr></tbody></table></div>"
             "<p>Le couple de desserrage vaut toujours F × AB = 100 × 0,4 = <b>40 N·m</b> : c'est un couple, sa valeur ne "
             "dépend pas du point E. En vectoriel : " + v("M") + " = " + v("AB") + " ∧ " + v("F") + " = 40 " + v("k") + " N·m.</p>")
    s8 = sec(8, "c2-resultant", "Moment résultant de plusieurs forces",
             "<p>Le moment résultant en un point A de n forces F<sub>1</sub>, F<sub>2</sub>, …, F<sub>n</sub> est égal à la "
             "<b>somme des moments en A</b> de chacune des forces.</p>" +
             formule(v("M") + "<sub>A</sub> = " + v("M") + "<sub>A</sub>(" + v("F") + "<sub>1</sub>) + " + v("M") + "<sub>A</sub>(" +
                     v("F") + "<sub>2</sub>) + … + " + v("M") + "<sub>A</sub>(" + v("F") + "<sub>n</sub>)",
                     "forces coplanaires : la même somme, en moments algébriques (avec leur signe)") +
             '<div class="remarque"><p>C\'est l\'outil des problèmes d\'<b>équilibre</b> (moment résultant nul) et de '
             "<b>basculement</b> (signe du moment résultant) : balance romaine, chargeur sur pneus… à pratiquer dans "
             "l'exercice 2.1.</p></div>" +
             check("Trois forces sur une barre, moments en A : +120 N·m, −45 N·m et −30 N·m. Que vaut le moment résultant "
                   "en A (en N·m) ?", 45, 0.01, "120 − 45 − 30 = 45 N·m, positif : sens trigonométrique.", "N·m"))
    s9 = sec(9, "c2-quiz", "Quiz : vérifie tes connaissances", quiz("q2-", QUIZ_2))
    page(fichier="couple-moment-source.html", titre="Moments et couples", tag="Cours 3", niveau=1,
         description="Cours interactif : moment d'une force, théorème de Varignon, vecteur-moment, moment par rapport à "
                     "un axe, couple et vecteur-couple, avec des simulateurs (navette, clé, couple) et un quiz.",
         sous_titre="Ce qui fait tourner : moment d'une force par rapport à un point, théorème de Varignon, "
                    "vecteur-moment et moment par rapport à un axe, couple et vecteur-couple. Environ 50 minutes, avec "
                    "une navette à piloter, une clé à serrer, un couple à explorer, un calculateur et un quiz.",
         objectif="Déterminer le moment d'une force et le couple engendré par des forces.",
         prerequis="Cours 1 et 2 : vecteur-force, coordonnées et projection d'une force.",
         nav=[("c2-navette", "Pourquoi"), ("c2-action", "Force et moment"), ("c2-calcul", "Moment en un point"),
              ("c2-varignon", "Varignon"), ("c2-vecteur", "Vecteur-moment"), ("c2-coord", "Coordonnées et axe"),
              ("c2-couple", "Couple"), ("c2-resultant", "Plusieurs forces"), ("c2-quiz", "Quiz")],
         sections=[s1, s2, s3, s4, s5, s6, s7, s8, s9],
         liens=[("force-moment.html", "Exercice 1.1 — Force, moment et couple"),
                ("exercice-couples-moments.html", "Exercice 2.1 — Couples et moments")])


# =====================================================================================================================
# COURS 1 — MODÉLISATION DES ACTIONS MÉCANIQUES (chapitre « Forces et actions mécaniques »)
# =====================================================================================================================
QUIZ_0 = [
    ("Un vecteur-force est défini par…", ["une intensité et un point", "une intensité, une direction, un sens et un point "
                                                                       "d'application", "une masse et une vitesse"], 1,
     "Les quatre caractéristiques : point d'application, direction, sens, intensité."),
    ("L'intensité d'une force s'exprime en…", ["kg", "N (ou daN, kN)", "N·m"], 1, "Le newton et ses multiples ; 1 daN = 10 N."),
    ("Une force F peut être remplacée par deux composantes U et V…", ["d'une seule façon", "d'une infinité de façons",
                                                                     "jamais"], 1,
     "Il y a une infinité de solutions, selon les directions choisies : F = U + V."),
    ("F = 1 000 daN est inclinée de 30° sous l'axe x. F<sub>y</sub> vaut…", ["−500 daN", "500 daN", "−866 daN"], 0,
     "F<sub>y</sub> = −F sin 30° = −500 daN : la force tire vers le bas."),
    ("Un sac de 10 kg sur Terre (g = 9,81 m·s⁻²) a un poids de…", ["10 N", "98,1 N", "981 N"], 1, "P = m × g = 10 × 9,81 = 98,1 N."),
    ("Le poids et l'attraction d'un aimant sont des actions…", ["de contact", "à distance", "réparties"], 1,
     "Elles s'exercent sans contact : ce sont les actions à distance."),
    ("Une charge linéique de 500 N/m répartie sur 2 m équivaut à une résultante de…", ["250 N", "1 000 N", "500 N"], 1,
     "R = q × L = 500 × 2 = 1 000 N, au milieu de la longueur."),
    ("100 bars sur un piston de 50 cm² donnent une poussée de…", ["5 000 daN", "2 daN", "500 daN"], 0,
     "R = p × S = 100 bar × 50 cm² = 5 000 daN (1 bar = 1 daN/cm²)."),
]
JEU_DISTANCE = [("Le poids d'un sac à dos", "distance"), ("Le pied du footballeur sur le ballon", "contact"),
                ("Un aimant qui attire un trombone", "distance"), ("Le câble qui tire sur un support", "contact"),
                ("L'huile sous pression sur un piston", "contact"), ("Le vent sur un panneau", "contact")]
JEU_CONTACT = [("Une bille posée sur un plan", "concentree"), ("Un cylindre couché sur une table", "lineique"),
               ("Un cube posé sur le sol", "surfacique"), ("L'huile sur le piston d'un vérin", "surfacique"),
               ("Une roue de train sur le rail", "concentree"), ("Un rouleau de peinture sur un mur", "lineique")]


def jeu(titre, lignes, choix):
    ls = "".join(f'<div class="jeu-l" data-ok="{ok}"><span>{t}</span>' +
                 "".join(f'<button type="button" data-v="{k}" aria-pressed="false">{n}</button>' for k, n in choix) +
                 '<b class="jeu-fb" aria-live="polite"></b></div>' for t, ok in lignes)
    return f'<div class="jeu"><h3>{titre}</h3>{ls}<p class="jeu-s" aria-live="polite"></p></div>'


def cours_modelisation():
    s1 = sec(1, "c0-force", "Le vecteur-force",
             "<p>Une <b>force</b> modélise une action mécanique : ce qui peut maintenir un corps en équilibre, créer ou "
             "modifier son mouvement, ou le déformer. On la représente par un <b>vecteur-force</b>, défini par quatre "
             "caractéristiques.</p><p class=\"cours-defi\">À toi : retourne chaque carte.</p>" +
             cartes([("Son point d'application", "Le point où s'exerce l'action (ou un point de son support)."),
                     ("Sa direction", "La droite d'action, ou support, de la force : verticale, horizontale, inclinée de 30°…"),
                     ("Son sens", "Vers où la force agit sur sa droite d'action : le câble tire, le pied pousse."),
                     ("Son intensité", "Sa valeur, ou module, en newtons (N) ou unités dérivées : daN, kN.")]) +
             '<div class="remarque"><p>Les forces sont aussi appelées <b>glisseurs</b> (voir le cours sur les torseurs) : '
             "on peut faire glisser une force le long de sa droite d'action sans changer son effet sur un solide.</p></div>"
             "<h3>Du réel au modèle : la schématisation</h3>" +
             "<p>Observe le système réel, repère les quatre caractéristiques de l'action, puis clique sur "
             "« Schématiser » pour voir le modèle.</p>" +
             schema(svg_cable(), "<b>Exemple 1</b> : l'action du câble 2 sur le support 1 est schématisée par le "
                    "vecteur-force " + v("A") + "<sub>2/1</sub> : point d'application A, direction celle du câble, sens de A "
                    "vers I (le câble tire), intensité 1 000 daN.") +
             schema(svg_ballon(), "<b>Exemple 2</b> : au moment du tir, l'action du pied 2 sur le ballon 1 est " +
                    v("T") + "<sub>2/1</sub> : point T, inclinée de 40° sur la verticale, de T vers K, 15 N. Le poids " +
                    v("P") + "<sub>1</sub> est vertical, vers le bas, appliqué en G, 5 N.") +
             check("Combien vaut l'intensité de l'action du câble sur le support, en newtons ?", 10000, 0.5,
                   "1 000 daN = 10 000 N, car 1 daN = 10 N.", "N"))
    co = ('<svg viewBox="0 0 480 320" role="img" aria-label="Force F appliquée en A et ses composantes U et V selon deux '
          'directions réglables"></svg>')
    s2 = sec(2, "c0-comp", "Composantes d'une force",
             "<p>Une force " + v("F") + " agissant en un point A peut toujours être remplacée par deux autres forces, ses "
             "<b>composantes</b> " + v("U") + " et " + v("V") + ", agissant au même point et vérifiant :</p>" +
             formule(v("F") + " = " + v("U") + " + " + v("V"), "c'est l'inverse de la résultante : une infinité de solutions, "
                     "selon les directions choisies") +
             simu("composantes", "Simulateur : choisis les directions de U et de V", co,
                  curseur("u", "Direction de U", -90, 90, 1, 0, "u") + curseur("v", "Direction de V", 0, 180, 1, 90, "v"),
                  '<div class="simu-calc"><p data-o="res"></p></div>',
                  defi="<b>Défi :</b> trouve deux directions pour lesquelles U et V sont toutes deux plus grandes que F "
                       "(100 N). <span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="F = 100 N est fixe. Le parallélogramme montre que U + V redonne toujours F.") +
             '<div class="remarque"><p>Lorsque U et V sont perpendiculaires, les composantes sont dites '
             "<b>orthogonales</b>. Suivant les axes x et y : " + v("F") + " = " + v("F") + "<sub>x</sub> + " + v("F") +
             "<sub>y</sub> ; dans l'espace : " + v("F") + " = " + v("F") + "<sub>x</sub> + " + v("F") + "<sub>y</sub> + " +
             v("F") + "<sub>z</sub>.</p></div>")
    pro = ('<svg viewBox="0 0 460 380" role="img" aria-label="Repère (O, x, y) ; force F réglable et ses projections '
           'Fx sur x et Fy sur y"></svg>')
    s3 = sec(3, "c0-coord", "Coordonnées cartésiennes d'une force",
             "<p>Les coordonnées cartésiennes F<sub>x</sub> et F<sub>y</sub> sont les composantes orthogonales "
             "particulières de " + v("F") + " suivant x et y. Avec α, l'angle entre F et l'axe x :</p>" +
             formule("F<sub>x</sub> = F cos α &nbsp; F<sub>y</sub> = F sin α", "tan α = F<sub>y</sub> / F<sub>x</sub> "
                     "&nbsp;·&nbsp; F² = F<sub>x</sub>² + F<sub>y</sub>²") +
             simu("projection", "Simulateur : projette une force", pro,
                  '<div class="simu-choix" role="group" aria-label="Angle de référence">'
                  '<button type="button" data-mode="alpha" aria-pressed="true">α depuis l\'axe x</button>'
                  '<button type="button" data-mode="beta" aria-pressed="false">β depuis l\'axe y</button></div>' +
                  curseur("F", "Intensité F", 0, 1000, 10, 500, "F") +
                  '<label><span><span data-o="nom"></span> : <output data-o="ang"></output></span>'
                  '<input type="range" data-in="ang" min="-180" max="180" step="1" value="30"></label>',
                  '<div class="simu-calc"><p data-o="fx"></p><p data-o="fy"></p></div>'
                  '<p class="small" data-o="signe"></p><p class="small" data-o="verif"></p>',
                  defi="<b>Défis :</b> trouve un angle pour lequel F<sub>x</sub> = F<sub>y</sub>. "
                       "<span class=\"defi-ok\" data-defi=\"egal\"></span><br>Trouve un réglage où F<sub>x</sub> &lt; 0 et "
                       "F<sub>y</sub> &gt; 0. <span class=\"defi-ok\" data-defi=\"signe\"></span>",
                  aide="Fais glisser l'extrémité jaune de la force, ou utilise les curseurs.") +
             a_toi("reprends le câble : A<sub>2/1</sub> = 1 000 daN, incliné de 30° sous l'axe x. Calcule ses coordonnées.",
                   "<p>A<sub>x</sub> = 1 000 × cos 30° = <b>866 daN</b> ; A<sub>y</sub> = −1 000 × sin 30° = <b>−500 daN</b> "
                   "(le câble tire vers le bas). " + v("A") + "<sub>2/1</sub> = 866 " + v("i") + " − 500 " + v("j") + ". "
                   "Contrôle : tan 30° = 500 / 866 ≈ 0,577 et √(866² + 500²) ≈ 1 000 daN.</p>" +
                   '<figure class="fig-svg">' + svg_cable_coord() + "<figcaption>Les deux coordonnées de " + v("A") +
                   "<sub>2/1</sub> : A<sub>x</sub> suivant x, A<sub>y</sub> suivant y.</figcaption></figure>") +
             "<p class=\"small\">Pour t'entraîner davantage : cours 2 (projection d'une force) et exercice 1.3 (les quatre "
             "quadrants).</p>")
    s4 = sec(4, "c0-distance", "Actions à distance : le poids",
             "<p>Les actions mécaniques représentent les efforts exercés sur et entre les solides réels. On les divise en "
             "deux grandes familles : les actions <b>à distance</b> et les actions <b>de contact</b> (les plus nombreuses "
             "et les plus diverses).</p>" +
             jeu("Jeu : à distance ou de contact ?", JEU_DISTANCE, [("distance", "à distance"), ("contact", "de contact")]) +
             "<p>Les actions à distance sont essentiellement de deux types : le <b>poids</b> et l'<b>aimantation</b>. Le "
             "poids d'un solide est représenté par le <b>vecteur-poids</b> " + v("P") + " :</p><ul><li>point d'application : "
             "G, le centre de gravité ;</li><li>direction : la verticale passant par G ;</li><li>sens : vers le bas ;</li>"
             "<li>intensité :</li></ul>" +
             formule("P = m × g", "P en N ; m en kg<br>g = 9,81 m·s⁻² : accélération de la pesanteur") +
             '<div class="remarque"><p>g varie avec la latitude (de 9,78 m·s⁻² à l\'équateur à 9,83 m·s⁻² aux pôles) et avec '
             "l'altitude h : g = g<sub>0</sub> × R² / (R + h)², avec g<sub>0</sub> = 9,81 m·s⁻² et R ≈ 6 378 km, le "
             "rayon de la Terre.</p></div>" +
             simu("poids", "Simulateur : combien pèse-t-on ?",
                  '<svg viewBox="0 0 420 360" role="img" aria-label="Un objet de centre de gravité G posé sur un astre ou '
                  'à l\'altitude h, et son poids P, vertical vers le bas"></svg>',
                  '<div class="simu-choix" role="group" aria-label="Astre"><button type="button" data-astre="terre" '
                  'aria-pressed="true">Terre</button><button type="button" data-astre="lune" aria-pressed="false">Lune</button>'
                  '<button type="button" data-astre="mars" aria-pressed="false">Mars</button></div>' +
                  curseur("m", "Masse m", 1, 100, 1, 60, "m") + curseur("h", "Altitude h", 0, 20000, 100, 0, "h"),
                  '<div class="simu-calc"><p data-o="g"></p><p data-o="P"></p></div>'
                  '<div><span>Poids (barre pleine : 981 N)</span><div class="jauge"><div class="jauge-bar"></div></div></div>',
                  defi="<b>Défi :</b> sur Terre, à quelle altitude ton poids est-il divisé par 4 ? "
                       "<span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="La longueur de P suit son intensité : change d'astre, monte en altitude.") +
             check("Une valise de 23 kg : quel est son poids sur Terre, en N (au dixième) ?", 225.6, 0.06,
                   "P = 23 × 9,81 ≈ 225,6 N.", "N"))
    li = ('<svg viewBox="0 0 520 250" role="img" aria-label="Cylindre 1 couché sur le plan 0 : charge linéique uniforme '
          'q le long du contact AB, ou sa résultante R au milieu de AB, opposée au poids P"></svg>')
    ve = ('<svg viewBox="0 0 560 300" role="img" aria-label="Vérin en coupe : l\'huile sous pression p, admise derrière le '
          'piston de diamètre d, le pousse ; la tige transmet la poussée F = R = p × S"></svg>')
    s5 = sec(5, "c0-contact", "Actions de contact : concentrées ou réparties",
             "<p>Les actions de contact se divisent en trois groupes :</p><ul><li>les actions ou charges "
             "<b>concentrées</b> : l'effort s'exerce en un point ou sur une toute petite surface ; il est schématisé par "
             "un vecteur-force (N, daN, kN) ;</li><li>les actions <b>réparties sur une ligne</b> : charge ou pression "
             "linéique q, en N/m ;</li><li>les actions <b>réparties sur une surface</b> : pression superficielle p, en "
             "Pa (N/m²).</li></ul>" + svg_contacts() +
             jeu("Jeu : concentrée, linéique ou surfacique ?", JEU_CONTACT,
                 [("concentree", "concentrée"), ("lineique", "linéique"), ("surfacique", "surfacique")]) +
             "<h3>Charge linéique uniforme</h3><p>Pour simplifier les calculs, une charge linéique uniforme q, répartie "
             "sur une longueur L, est remplacée par sa <b>résultante</b> R, située au milieu, en général perpendiculaire "
             "au contact :</p>" + formule("R = q × L", "R en N ; q en N/m ; L en m") +
             simu("lineique", "Simulateur : charge répartie sur une ligne", li,
                  '<div class="simu-choix" role="group" aria-label="Représentation"><button type="button" data-vue="q" '
                  'aria-pressed="true">Charge répartie q</button><button type="button" data-vue="R" aria-pressed="false">'
                  'Résultante R</button></div>' +
                  curseur("q", "Charge linéique q", 100, 5000, 100, 1000, "q") + curseur("L", "Longueur L", 0.1, 2, 0.05, 1, "L"),
                  '<div class="simu-calc"><p data-o="R"></p></div>',
                  aide="Bascule entre la charge répartie et sa résultante : les deux modèles sont équivalents.") +
             check("Un cylindre de poids 100 N repose sur une ligne de contact de 10 cm. Que vaut la charge linéique q, "
                   "en N/m ?", 1000, 0.5, "q = R / L = 100 / 0,1 = 1 000 N/m.", "N/m") +
             "<h3>Pression de contact sur une surface</h3><p>Sur une surface plane, l'ensemble des pressions est remplacé "
             "par sa résultante R, perpendiculaire à la surface :</p>" +
             formule("p = R / S &nbsp; ou &nbsp; R = p × S", "R en N, S en m², p en Pa (N/m²)<br>ou R en daN, S en cm², "
                     "p en bar") +
             '<div class="remarque"><p><b>Correspondances</b> : 1 bar = 10⁵ Pa = 100 000 Pa = 1 daN/cm² ; 1 MPa = 10⁶ Pa '
             "= 1 N/mm² = 10 bars.</p></div>" +
             check("Un cube de poids 100 N repose sur une base de 10 cm × 10 cm. Quelle pression de contact, en Pa ?", 10000,
                   0.5, "p = R / S = 100 / (0,1 × 0,1) = 100 / 0,01 = 10 000 Pa = 10⁴ Pa.", "Pa") +
             "<h3>Exemple : le vérin hydraulique</h3><p>L'huile sous pression p, admise derrière le piston, agit "
             "perpendiculairement à toute sa surface. Sa résultante R = p × S est portée par l'axe du vérin : c'est la "
             "poussée F transmise par la tige.</p>" +
             simu("verin", "Simulateur : la poussée d'un vérin", ve,
                  curseur("p", "Pression p", 0, 300, 5, 100, "p") + curseur("d", "Diamètre d du piston", 20, 200, 1, 100, "d"),
                  '<div class="simu-calc"><p data-o="S"></p><p data-o="R"></p></div>',
                  defi="<b>Défi :</b> avec 100 bars, quel diamètre faut-il pour pousser 8 tonnes (8 000 daN) ? "
                       "<span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="Plus la pression est forte, plus l'huile est foncée et les flèches de pression longues.") +
             a_toi("calcule la poussée d'un vérin de diamètre 10 cm alimenté à 100 bars.",
                   "<p>R = p × S = 100 × π × 10² / 4 = 100 × 78,54 = <b>7 854 daN</b> : la « poussée de 8 tonnes » d'un vérin "
                   "courant.</p>"))
    s6 = sec(6, "c0-quiz", "Quiz : vérifie tes connaissances", quiz("q0-", QUIZ_0))
    page(fichier="modelisation-source.html", titre="Modélisation des actions mécaniques", tag="Cours 1", niveau=1,
         description="Cours interactif : vecteur-force, composantes et coordonnées d'une force, poids, actions de contact "
                     "concentrées ou réparties, pression, avec des simulateurs, des jeux et un quiz.",
         sous_titre="Du réel au modèle : vecteur-force, composantes, coordonnées, poids et actions de contact "
                    "(concentrées, linéiques, surfaciques). Environ 40 minutes, avec des simulateurs, deux jeux de "
                    "classement et un quiz.",
         objectif="Schématiser une action mécanique par une force, une charge répartie ou une pression.",
         prerequis="Mathématiques : notion de vecteur.",
         nav=[("c0-force", "Le vecteur-force"), ("c0-comp", "Composantes"), ("c0-coord", "Coordonnées"),
              ("c0-distance", "Le poids"), ("c0-contact", "Actions de contact"), ("c0-quiz", "Quiz")],
         sections=[s1, s2, s3, s4, s5, s6],
         liens=[("exercice-projections.html", "Exercice 1.2 — Projections d'une force"),
                ("exercice-quadrants.html", "Exercice 1.3 — Les quatre quadrants")])


# =====================================================================================================================
# COURS 4 — TORSEUR D'ACTION MÉCANIQUE (page 9)
# =====================================================================================================================
LETTRES = {
    "X": "<b>X</b> : coordonnée de la force " + v("F") + " sur l'axe x du repère R, en N.",
    "Y": "<b>Y</b> : coordonnée de la force sur l'axe y, en N.",
    "Z": "<b>Z</b> : coordonnée de la force sur l'axe z, en N.",
    "L": "<b>L</b> : coordonnée du moment " + v("M") + "<sub>B</sub>(" + v("F") + ") sur l'axe x, en N·m : il fait tourner "
         "autour de x.",
    "M": "<b>M</b> : coordonnée du moment sur l'axe y, en N·m.",
    "N": "<b>N</b> : coordonnée du moment sur l'axe z, en N·m. Pour une force dans le plan (x, y), c'est la seule non nulle.",
}
QUIZ_3 = [
    ("Le torseur d'une force F appliquée en A, écrit au point A, a un moment…", ["nul", "égal à F", "égal à OA ∧ F"], 0,
     "Le moment d'une force en son point d'application est toujours nul."),
    ("Quand on change de point de réduction, la résultante…", ["change", "ne change pas", "s'annule"], 1,
     "Les coordonnées de la force ne varient pas : seul le moment est à recalculer."),
    ("Dans {X L ; Y M ; Z N}<sub>B</sub>, les lettres L, M, N sont…", ["les coordonnées de la force",
                                                                      "les coordonnées du point B",
                                                                      "les coordonnées du moment en B"], 2,
     "X, Y, Z : la force ; L, M, N : le moment au point de réduction B."),
    ("F = (0 ; 100 ; 0) N est appliquée en A (2 ; 0 ; 0) m. Au point O, N vaut…", ["200 N·m", "−200 N·m", "0"], 0,
     "N = x<sub>A</sub> F<sub>y</sub> − y<sub>A</sub> F<sub>x</sub> = 2 × 100 − 0 = 200 N·m."),
    ("Même force, au point B (2 ; 5 ; 0) m, le moment vaut…", ["500 N·m", "200 N·m", "0"], 2,
     "B est sur la droite d'action de F (la verticale x = 2) : le bras de levier est nul."),
    ("Pour additionner deux torseurs, il faut d'abord…", ["les écrire au même point", "additionner leurs points",
                                                          "rien de particulier"], 0,
     "On ne peut additionner que des torseurs réduits au même point."),
    ("La relation M<sub>B</sub> = M<sub>A</sub> + BA ∧ R sert à…", ["calculer une force", "transporter le moment d'un point à un autre",
                                                                    "calculer une norme"], 1,
     "C'est la formule de transport du moment : elle donne le moment en B à partir de celui en A."),
]


def cours_torseur():
    lettres = '<span class="tm"><span class="tm-nom">{<i>T</i><sub>F</sub>}<sub>B</sub> =</span><span class="tm-b" aria-hidden="true">{</span><span class="tm-g">' + "".join(
        f'<span class="tm-c clic" role="button" tabindex="0" aria-pressed="false" data-info="{esc(LETTRES[c])}">{c}</span>'
        for c in "XLYMZN") + '</span><span class="tm-b" aria-hidden="true">}</span><sub class="tm-p">B</sub></span>'
    s1 = sec(1, "c3-def", "Une action, deux vecteurs : le torseur",
             "<p>Une action mécanique possède donc deux composantes : la <b>force</b> et le <b>moment</b> de cette force. "
             "Le <b>torseur</b> d'une action mécanique est une forme d'écriture, de présentation : elle peut être sous "
             "forme <b>vectorielle</b> ou sous forme <b>analytique</b>. Ses coordonnées varient suivant le <b>point de "
             "réduction</b> du torseur.</p>" +
             a_toi("écris le torseur de la force " + v("F") + " au point B, sous les deux formes.",
                   formule("{<i>T</i><sub>F</sub>}<sub>B</sub> = { " + v("F") + " ; " + v("M") + "<sub>B</sub>(" + v("F") +
                           ") }<sub>B</sub>", "forme vectorielle : la résultante, puis le moment au point B") +
                   formule("{<i>T</i><sub>F</sub>}<sub>B</sub> = " + torseur_html(["X", "L", "Y", "M", "Z", "N"], "B (R)"),
                           "forme analytique, dans le repère R")) +
             '<div class="remarque"><p>Le torseur rassemble en une seule écriture ce qui fait <b>avancer</b> (la force) '
             "et ce qui fait <b>tourner</b> (le moment) : c'est l'outil de la statique pour écrire l'équilibre.</p></div>")
    s2 = sec(2, "c3-lettres", "Que représente chaque lettre ?",
             f'<div class="simu" data-widget="lettres"><h3>Explore le torseur</h3><p class="cours-defi">À toi : clique sur '
             f'chaque lettre.</p><p style="font-size:1.3rem">{lettres}</p><div class="carte-txt tm-info" aria-live="polite">'
             f'<p class="small">X, Y, Z sont les coordonnées de la force ; L, M, N celles du moment au point B, dans le même '
             f'repère R.</p></div></div>' +
             check("Une force " + v("F") + " = (120 ; −50 ; 0) N est appliquée en B. Dans {<i>T</i><sub>F</sub>}<sub>B</sub>, "
                   "que vaut Y (en N) ?", -50, 0.001, "Y est la coordonnée de la force sur y : −50 N. Et L = M = N = 0, "
                   "car B est le point d'application.", "N"))
    tr = ('<svg viewBox="0 0 520 330" role="img" aria-label="Plan quadrillé : force F appliquée en A, point de réduction '
          'B déplaçable, droite d\'action en pointillés et bras de levier en jaune"></svg>')
    s3 = sec(3, "c3-transport", "Changer de point de réduction",
             '<div class="remarque"><p><b>Remarques</b></p><ul><li>Si le point de réduction du torseur change, les '
             "coordonnées de la force ne varient pas : <b>seul le moment est à recalculer</b>.</li><li>Le moment au "
             "<b>point d'application</b> de la force est <b>toujours nul</b>.</li></ul></div>"
             "<p>Pour une force " + v("F") + " appliquée en A, le moment en un autre point B se calcule avec le produit "
             "vectoriel. Plus généralement, on <b>transporte</b> le moment d'un point A à un point B :</p>" +
             formule(v("M") + "<sub>B</sub> = " + v("M") + "<sub>A</sub> + " + v("BA") + " ∧ " + v("R"),
                     "formule de transport du moment<br>pour une force seule appliquée en A : " + v("M") + "<sub>B</sub> = "
                     + v("BA") + " ∧ " + v("F")) +
             simu("transport", "Simulateur : déplace le point de réduction B", tr,
                  "<p class=\"small\">Fais glisser B (jaune), le point d'application A ou l'extrémité verte de la force. "
                  "Les points s'accrochent tous les 0,5 m ; 1 m de flèche représente 200 N.</p>"
                  '<p class="small"><span data-o="A"></span> · <span data-o="B"></span><br><span data-o="F"></span></p>',
                  '<div class="simu-calc torseurs-vivants"><p data-o="tA"></p><p data-o="tB"></p></div>'
                  '<p class="simu-calc small" data-o="N"></p><p class="simu-verdict" data-o="verdict" aria-live="polite"></p>',
                  defi="<b>Défi :</b> trouve trois positions de B, différentes de A, où le moment est nul. "
                       "<span data-o=\"defi\" aria-live=\"polite\"></span>",
                  aide="La résultante est la même en A et en B ; seule la dernière case, le moment N, change."))
    s4 = sec(4, "c3-somme", "Plusieurs actions : le torseur résultant",
             "<p>Pour additionner des actions mécaniques, on écrit leurs torseurs <b>au même point</b>, puis on "
             "additionne les résultantes et les moments :</p>" +
             formule("{<i>T</i><sub>1</sub>}<sub>O</sub> + {<i>T</i><sub>2</sub>}<sub>O</sub> = { " + v("R") + "<sub>1</sub> + "
                     + v("R") + "<sub>2</sub> ; " + v("M") + "<sub>O1</sub> + " + v("M") + "<sub>O2</sub> }<sub>O</sub>",
                     "deux torseurs écrits en des points différents ne s'additionnent pas") +
             a_toi("deux forces opposées de 100 N sont appliquées en A (0 ; 1 ; 0) m, " + v("F") + "<sub>A</sub> = (100 ; 0 ; 0) N, "
                   "et en B (0 ; −1 ; 0) m, " + v("F") + "<sub>B</sub> = (−100 ; 0 ; 0) N. Écris leur torseur résultant en O.",
                   "<p>Résultante : (100 − 100 ; 0 ; 0) = (0 ; 0 ; 0). Moments en O, sur z : x<sub>A</sub>F<sub>Ay</sub> − "
                   "y<sub>A</sub>F<sub>Ax</sub> = 0 − 1 × 100 = −100 N·m et 0 − (−1) × (−100) = −100 N·m.</p>" +
                   formule("{<i>T</i>}<sub>O</sub> = " + torseur_html(["0", "0", "0", "0", "0", "−200"], "O"),
                           "résultante nulle, moment non nul : c'est un <b>couple pur</b>, comme celui d'un tourne-vis")))
    s5 = sec(5, "c3-exemple", "Exemple résolu pas à pas",
             stepper("Torseur d'une force en A, puis en O", [
                 "Une force " + v("F") + " = (300 ; −400 ; 0) N est appliquée au point A (2 ; 1 ; 0) m.",
                 "Coordonnées de la résultante : X = 300 N, Y = −400 N, Z = 0.",
                 "Au point d'application, le moment est nul : {<i>T</i>}<sub>A</sub> = " +
                 torseur_html(["300", "0", "−400", "0", "0", "0"], "A") + ".",
                 v("OA") + " = (2 ; 1 ; 0) m. " + v("M") + "<sub>O</sub> = " + v("OA") + " ∧ " + v("F") + " = (1 × 0 − 0 × (−400) ; "
                 "0 × 300 − 2 × 0 ; 2 × (−400) − 1 × 300) = (0 ; 0 ; −1 100) N·m.",
                 "Torseur au point O : {<i>T</i>}<sub>O</sub> = " + torseur_html(["300", "0", "−400", "0", "0", "−1 100"], "O") +
                 " : même résultante, nouveau moment.",
                 "Contrôle par la formule de transport au point C (5 ; 1 ; 0) m : " + v("CO") + " = (−5 ; −1 ; 0) ; "
                 + v("CO") + " ∧ " + v("F") + " a pour composante sur z (−5) × (−400) − (−1) × 300 = 2 300 ; donc N<sub>C</sub> = "
                 "−1 100 + 2 300 = <b>1 200 N·m</b>. Directement : " + v("CA") + " = (−3 ; 0 ; 0), (−3) × (−400) − 0 × 300 = "
                 "1 200 N·m. ✔"]))
    s6 = sec(6, "c3-quiz", "Quiz : vérifie tes connaissances", quiz("q3-", QUIZ_3))
    page(fichier="torseur-source.html", titre="Torseur d'action mécanique", tag="Cours 4", niveau=2,
         description="Cours interactif : écrire une action mécanique sous forme de torseur, changer de point de réduction "
                     "et additionner des torseurs, avec un simulateur, un exemple pas à pas et un quiz.",
         sous_titre="Écrire une action mécanique sous forme de torseur, puis changer de point de réduction. Environ "
                    "30 minutes : un torseur à explorer, un simulateur de transport du moment, un exemple résolu pas à "
                    "pas et un quiz.",
         objectif="Écrire une action mécanique sous forme de torseur.",
         prerequis="Cours 1 à 3 : coordonnées d'une force, moment et produit vectoriel.",
         nav=[("c3-def", "Le torseur"), ("c3-lettres", "Les lettres"), ("c3-transport", "Changer de point"),
              ("c3-somme", "Plusieurs actions"), ("c3-exemple", "Exemple"), ("c3-quiz", "Quiz")],
         sections=[s1, s2, s3, s4, s5, s6],
         liens=[("exercice-torseurs.html", "Exercice 2.2 — Torseurs : les bases")])


if __name__ == "__main__":
    cours_modelisation()
    cours_projection()
    cours_couple()
    cours_torseur()
