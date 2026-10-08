#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit l'exercice « Force, moment et couple » à partir du gabarit (src/gabarit-exercice-interactif.html).

    python3 src/construire_force_moment.py     # écrit src/exercices/force-moment-source.html
    python3 src/generer.py                     # publie force-moment.html (avec le lien de retour vers l'accueil)

Le bloc <style> et les deux scripts du gabarit (moteur de correction et moteur applicatif) sont repris tels quels :
seuls le titre, la page d'accueil, les documents, le contenu des parties et la configuration (__PARTS__, __QCFG__,
__SKCFG__) sont réécrits ici. Les figures sont dans src/images/force-moment/.
"""
import base64
import html
import json
import pathlib
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parent.parent
GABARIT = ROOT / "src" / "gabarit-exercice-interactif.html"
IMG = ROOT / "src" / "images" / "force-moment"
SORTIE = ROOT / "src" / "exercices" / "force-moment-source.html"

TITRE = "Force, moment et couple"
SOUS_TITRE = ("Neuf parties courtes pour maîtriser le moment d'une force : bras de levier, équilibre, basculement, "
              "double levier et composantes d'une force. Les réponses se saisissent au clavier, unités comprises.")

# ---------------------------------------------------------------- unités acceptées (le moteur normalise la saisie)
U_NM = {"label": "N·m", "accept": ["nm", "newtonmetre", "newtonmetres"]}
U_N = {"label": "N", "accept": ["n", "newton", "newtons"]}
U_M = {"label": "m", "accept": ["m", "metre", "metres"]}
U_DEG = {"label": "°", "accept": ["°", "deg", "degre", "degres"]}

UNITE = "Saisis la valeur <strong>avec son unité</strong> : l'unité vaut la moitié des points de la question."


def num(value, tol, unit=None, abs_=False):
    g = {"type": "num", "value": value, "absTol": tol}
    if unit:
        g["unit"] = unit
    if abs_:
        g["abs"] = True
    return g


def kw(any_, forbid=None):
    g = {"type": "kw", "any": any_}
    if forbid:
        g["forbid"] = forbid
    return g


# Basculement : « bascule » / « ne bascule pas » (les négations sont écartées de la réponse « bascule »)
BASCULE_MOTS = ["bascule", "basculera", "basculer", "basculement", "renverse", "chavire", "culbute", "tombe"]
G_BASCULE = kw([[BASCULE_MOTS], [["oui"]]], forbid=["pas", "non", "ne", "jamais"])
G_STABLE = kw([[["pas", "non", "jamais"], BASCULE_MOTS], [["stable", "equilibre", "immobile"]], [["non"]]])
G_SENS = kw([[["anti", "contre"], ["horaire"]],
             [["antihoraire", "contrehoraire", "trigonometrique", "trigo", "trigonometrie"]],
             [["inverse", "contraire", "oppose"], ["aiguilles", "aiguille", "montre"]]], forbid=["pas"])
G_FORMULE = kw([[["f"], ["d"], ["sin", "sinus"]], [["fdsin", "fdsina", "fdsinalpha", "fdsinus"]]],
               forbid=["cos", "cosinus", "tan", "tangente"])
G_EQUILIBRE = kw([[["equilibre", "statique"]]], forbid=["mouvement", "inconnue", "inconnu", "inconnus", "pas", "non"])

# ---------------------------------------------------------------- contenu : une partie par exercice d'origine
# Chaque question : (consigne, grader, réponse attendue, énoncé, démarche[, figure]) ; la figure est un fichier d'images
Q = dict


def fig(nom, alt, w):
    return Q(f=nom, alt=alt, w=w)


PARTIES = [
    Q(titre="Calcul du moment d'une force", minutes=5,
      intro="D<sub>1</sub> = 3 m ; D<sub>2</sub> = 4 m ; D<sub>3</sub> = 5 m ; F = 200 N. La force <b>F</b> est verticale, dirigée vers le bas.",
      fig=fig("f0.png", "Force F verticale vers le bas appliquée à droite du point O ; cotes D1 (hauteur), D2 (distance horizontale) et D3 (distance de O au point d'application)", 520),
      questions=[
          Q(s="Quel est le moment M de la force F par rapport au point O&nbsp;? (en N·m)",
            h=UNITE, g=num(800, 0.01, U_NM), att="M = 800 N·m",
            e="La force F étant verticale, le bras de levier est la distance <b>horizontale</b> entre O et la ligne d'action de F, c'est-à-dire D<sub>2</sub>. Donc&nbsp;: <b>M = F × D<sub>2</sub> = 200 × 4 = 800 N·m</b>.<br>Piège&nbsp;: D<sub>3</sub> = 5 m est la distance de O au point d'application, pas le bras de levier. Pour une force verticale, seule la distance horizontale compte."),
      ]),
    Q(titre="Influence du point d'application et de l'intensité", minutes=10,
      intro="Pour une force verticale, M = F × (distance horizontale). On compare chaque cas au cas de référence <b>F<sub>0</sub></b> (appliquée à 2 graduations de O).",
      questions=[
          Q(s="Intensité de F<sub>1</sub> égale à celle de F<sub>0</sub>. Le moment de F<sub>1</sub> par rapport à O<sub>1</sub> vaut X fois celui de F<sub>0</sub> par rapport à O. Trouvez X.",
            h="Réponds par le coefficient X (nombre sans unité).", g=num(2, 0.01), att="X = 2",
            e="La distance passe de 2 à 4 graduations (×2), l'intensité est inchangée. Le moment est donc multiplié par 2. <b>X = 2</b>.",
            fig=fig("f1.png", "Forces F0 (référence, 2 graduations de O) et F1 (4 graduations de O1)", 620)),
          Q(s="Intensité de F<sub>2</sub> égale à celle de F<sub>0</sub>. Le moment de F<sub>2</sub> par rapport à O<sub>2</sub> vaut X fois celui de F<sub>0</sub>. Trouvez X.",
            h="Réponds par le coefficient X (nombre sans unité).", g=num(0.5, 0.005), att="X = 0,5",
            e="La distance passe de 2 à 1 graduation (÷2), l'intensité est inchangée. Le moment est divisé par 2. <b>X = 0,5</b>.",
            fig=fig("f2.png", "Forces F0 (2 graduations de O) et F2 (1 graduation de O2)", 520)),
          Q(s="Intensité de F<sub>3</sub> égale à 2 fois celle de F<sub>0</sub>. Le moment de F<sub>3</sub> par rapport à O<sub>3</sub> vaut X fois celui de F<sub>0</sub>. Trouvez X.",
            h="Réponds par le coefficient X (nombre sans unité).", g=num(4, 0.01), att="X = 4",
            e="Distance ×2 (2 → 4 graduations) et intensité ×2. Le moment est multiplié par 2 × 2 = 4. <b>X = 4</b>.",
            fig=fig("f3.png", "Forces F0 (2 graduations de O) et F3 (4 graduations de O3)", 560)),
          Q(s="Intensité de F<sub>4</sub> égale à 2 fois celle de F<sub>0</sub>. Le moment de F<sub>4</sub> par rapport à O<sub>4</sub> vaut X fois celui de F<sub>0</sub>. Trouvez X.",
            h="Réponds par le coefficient X (nombre sans unité).", g=num(2, 0.01), att="X = 2",
            e="La distance est inchangée (2 graduations) mais l'intensité est ×2. Le moment est multiplié par 2. <b>X = 2</b>.",
            fig=fig("f4.png", "Forces F0 et F4 appliquées à 2 graduations de leur point O", 560)),
          Q(s="Intensité de F<sub>5</sub> égale à 2 fois celle de F<sub>0</sub>. Le moment de F<sub>5</sub> par rapport à O<sub>5</sub> vaut X fois celui de F<sub>0</sub>. Trouvez X.",
            h="Réponds par le coefficient X (nombre sans unité).", g=num(1, 0.01), att="X = 1",
            e="Distance ÷2 (2 → 1 graduation) et intensité ×2. Le moment est multiplié par ½ × 2 = 1 : il est <b>inchangé</b>. <b>X = 1</b>.",
            fig=fig("f5.png", "Forces F0 (2 graduations de O) et F5 (1 graduation de O5)", 620)),
      ]),
    Q(titre="Solide suspendu", minutes=5,
      intro="L = 3 m ; l = 1,5 m ; masse de la sphère = 20 kg ; g = 9,81 m/s². Le poids <b>P</b> s'applique au centre G, verticalement vers le bas.",
      fig=fig("f6.png", "Sphère suspendue à l'extrémité d'une barre horizontale de longueur L articulée en O ; poids P au centre G ; hauteur l", 380),
      questions=[
          Q(s="Quel est le moment M exercé par le poids de la sphère par rapport au point O&nbsp;? (en N·m)",
            h="Prendre g = 9,81 m/s². <b>Arrondir au dixième</b>. " + UNITE, g=num(588.6, 0.05, U_NM), att="M = 588,6 N·m",
            e="Poids&nbsp;: P = m·g = 20 × 9,81 = 196,2 N. La force est verticale&nbsp;: le bras de levier est la distance horizontale de O à la ligne d'action du poids, soit <b>L = 3 m</b> (la hauteur l = 1,5 m n'intervient pas). <b>M = P × L = 196,2 × 3 = 588,6 N·m</b>."),
      ]),
    Q(titre="Cas de plusieurs forces", minutes=7,
      intro="F<sub>1</sub> = 200 N (extrémité gauche) ; F<sub>2</sub> = 100 N (à 2,5 m de la gauche) ; O = pivot (2 m à droite de F<sub>2</sub>) ; F<sub>3</sub> = 250 N (extrémité droite, 3 m à droite de O). Les trois forces sont verticales, vers le bas.",
      fig=fig("f7.png", "Barre horizontale sur un pivot O ; trois forces verticales vers le bas F1, F2 et F3 ; cotes 2,5 m, 2 m et 3 m", 620),
      questions=[
          Q(s="Quelle est la valeur absolue du moment M résultant de ces 3 forces par rapport à O&nbsp;? (en N·m)",
            h=UNITE, g=num(350, 0.01, U_NM, abs_=True), att="|M| = 350 N·m",
            e="Distances à O&nbsp;: F<sub>1</sub> à 4,5 m (gauche), F<sub>2</sub> à 2 m (gauche), F<sub>3</sub> à 3 m (droite). En comptant le sens anti-horaire positif&nbsp;: M = +200×4,5 + 100×2 − 250×3 = 900 + 200 − 750 = <b>+350 N·m</b>. Valeur absolue&nbsp;: <b>350 N·m</b>."),
          Q(s="Dans quel sens la barre va-t-elle tourner&nbsp;?",
            h="Indique le sens (horaire ou anti-horaire).", g=G_SENS, att="Sens anti-horaire",
            e="Le moment résultant est positif (+350 N·m)&nbsp;: la barre tourne dans le <b>sens anti-horaire</b> (sens trigonométrique, inverse des aiguilles d'une montre). Le côté gauche descend."),
      ]),
    Q(titre="Recherche de l'équilibre", minutes=6,
      intro="Barre articulée à une extrémité. F<sub>1</sub> = 300 N.",
      questions=[
          Q(s="F<sub>1</sub> = 300 N est appliquée vers le haut à 2 m de l'articulation ; F<sub>2</sub> est appliquée vers le bas à 5 m de l'articulation. Quelle doit être l'intensité de F<sub>2</sub> pour que le système reste en équilibre&nbsp;? (en N)",
            h=UNITE, g=num(120, 0.01, U_N), att="F<sub>2</sub> = 120 N",
            e="Équilibre des moments à l'articulation&nbsp;: F<sub>1</sub> × 2 = F<sub>2</sub> × 5 → 300 × 2 = F<sub>2</sub> × 5 → <b>F<sub>2</sub> = 600 / 5 = 120 N</b>.",
            fig=fig("f8.png", "Barre articulée à gauche ; F1 vers le haut à 2 m de l'articulation ; F2 vers le bas à 3 m de F1", 560)),
          Q(s="Si l'intensité de F<sub>2</sub> est 100 N, à quelle distance d de F<sub>1</sub> doit se situer le point d'application de F<sub>2</sub> pour maintenir l'équilibre&nbsp;? (en m)",
            h="d est mesurée à partir de F<sub>1</sub>. " + UNITE, g=num(4, 0.01, U_M), att="d = 4 m",
            e="F<sub>2</sub> se trouve alors à (2 + d) de l'articulation. Équilibre&nbsp;: F<sub>1</sub> × 2 = F<sub>2</sub> × (2 + d) → 300 × 2 = 100 × (2 + d) → 6 = 2 + d → <b>d = 4 m</b>.",
            fig=fig("f9.png", "Barre articulée à gauche ; F1 vers le haut à 2 m de l'articulation ; F2 vers le bas à une distance d inconnue de F1", 560)),
      ]),
    Q(titre="Force non perpendiculaire au bras de levier", minutes=4,
      intro="La force <b>F</b> est appliquée en A, à l'extrémité d'un bras OA de longueur d, et fait un angle α avec ce bras.",
      fig=fig("f10.png", "Bras OA horizontal de longueur d ; force F appliquée en A, inclinée d'un angle α par rapport au bras", 520),
      questions=[
          Q(s="Donnez la formule du moment de la force F par rapport au point O.",
            h="Écris la formule. Notation&nbsp;: <code>*</code> pour multiplier, et <code>sin(…)</code>, <code>cos(…)</code> ou <code>tan(…)</code> pour une fonction trigonométrique de l'angle (exemple de syntaxe sans rapport avec l'exercice&nbsp;: <code>2*pi*r</code>).",
            g=G_FORMULE, att="M = F × d × sin(α)",
            e="Le bras de levier est la distance perpendiculaire de O à la ligne d'action de F, soit d·sin(α). D'où&nbsp;: <b>M = F × d × sin(α)</b>."),
      ]),
    Q(titre="Stabilité et basculement", minutes=14,
      intro="AB = 2 m, AC = 3 m, AD = 4 m (hauteurs au-dessus de la base A, arête de basculement). Avec F = 1000 N appliquée en C (3 m), le bloc est <b>à la limite de l'équilibre</b> : le moment de basculement maximal vaut donc 1000 × 3 = <b>3000 N·m</b>. Le bloc bascule dès que le moment de la force dépasse cette valeur.",
      fig=fig("f11.png", "Bloc parallélépipédique posé sur l'arête A ; points B, C et D à 2 m, 3 m et 4 m au-dessus de A ; force horizontale F appliquée en C", 440),
      questions=[
          Q(s="Si la force F (1000 N) est appliquée au point B, que se passe-t-il&nbsp;?", h="Réponds «&nbsp;bascule&nbsp;» ou «&nbsp;ne bascule pas&nbsp;».",
            g=G_STABLE, att="Le bloc ne bascule pas",
            e="Moment = 1000 × 2 = 2000 N·m &lt; 3000 N·m → le bloc <b>ne bascule pas</b>."),
          Q(s="Si la force F (1000 N) est appliquée au point D, que se passe-t-il&nbsp;?", h="Réponds «&nbsp;bascule&nbsp;» ou «&nbsp;ne bascule pas&nbsp;».",
            g=G_BASCULE, att="Le bloc bascule",
            e="Moment = 1000 × 4 = 4000 N·m &gt; 3000 N·m → le bloc <b>bascule</b>."),
          Q(s="Que se passe-t-il si la force F, appliquée en C, a une intensité de 1100 N&nbsp;?", h="Réponds «&nbsp;bascule&nbsp;» ou «&nbsp;ne bascule pas&nbsp;».",
            g=G_BASCULE, att="Le bloc bascule",
            e="Moment = 1100 × 3 = 3300 N·m &gt; 3000 N·m → le bloc <b>bascule</b>."),
          Q(s="Que se passe-t-il si on applique une force F de 800 N au point D&nbsp;?", h="Réponds «&nbsp;bascule&nbsp;» ou «&nbsp;ne bascule pas&nbsp;».",
            g=G_BASCULE, att="Le bloc bascule",
            e="Moment = 800 × 4 = 3200 N·m &gt; 3000 N·m → le bloc <b>bascule</b>."),
          Q(s="L'intensité maximale de la force applicable en C sans basculement est 1000 N. Quelle est l'intensité minimale de la force F' appliquée en D pour que le bloc bascule&nbsp;? (en N)",
            h=UNITE, g=num(750, 0.01, U_N), att="F' = 750 N",
            e="Basculement si F' × 4 &gt; 3000 N·m (moment restaurateur = 1000 × 3 = 3000 N·m). Donc F' &gt; 750 N → intensité minimale = <b>750 N</b>."),
          Q(s="Que se passe-t-il si on applique une force F de 800 N au point B&nbsp;?", h="Réponds «&nbsp;bascule&nbsp;» ou «&nbsp;ne bascule pas&nbsp;».",
            g=G_STABLE, att="Le bloc ne bascule pas",
            e="Moment = 800 × 2 = 1600 N·m &lt; 3000 N·m → le bloc <b>ne bascule pas</b>."),
          Q(s="Sachant que 1000 N est l'intensité maximale applicable en C sans basculement, quelle est l'intensité minimale d'une force F' appliquée en B pour que le bloc bascule&nbsp;? (en N)",
            h=UNITE, g=num(1500, 0.01, U_N), att="F' = 1500 N",
            e="Basculement si F' × 2 &gt; 3000 N·m. Donc F' &gt; 1500 N → intensité minimale = <b>1500 N</b>."),
      ]),
    Q(titre="Le coupe-boulon", minutes=7,
      intro="L<sub>1</sub> = 680 mm, L<sub>2</sub> = 44 mm, L<sub>3</sub> = 36 mm, L<sub>4</sub> = 40 mm ; F<sub>1</sub> = 50 N appliquée par l'utilisateur. Système à double levier.",
      fig=fig("f12.jpg", "Coupe-boulon à double levier avec les cotes L1 à L4 et les forces F1 (50 N), F2 et F3", 620),
      questions=[
          Q(s="Quelle est l'intensité de la force F<sub>3</sub> appliquée par la lame sur le câble à couper&nbsp;? (en N)",
            h="<b>Arrondir au centième.</b> " + UNITE, g=num(695.45, 0.05, U_N), att="F<sub>3</sub> ≈ 695,45 N",
            e="<b>1)</b> Moment de F<sub>1</sub> / 1<sup>re</sup> articulation = F<sub>1</sub> × L<sub>1</sub> = 50 × 680 = 34 000 N·mm.<br><b>2)</b> F<sub>2</sub> = 34 000 / L<sub>2</sub> = 34 000 / 44 ≈ 772,73 N. Moment de F<sub>2</sub> / 2<sup>e</sup> articulation = F<sub>2</sub> × L<sub>3</sub> ≈ 772,73 × 36 ≈ 27 818 N·mm.<br><b>3)</b> F<sub>3</sub> = (F<sub>2</sub> × L<sub>3</sub>) / L<sub>4</sub> ≈ 27 818 / 40 ≈ <b>695,45 N</b>.<br>Formule directe&nbsp;: F<sub>3</sub> = F<sub>1</sub> × (L<sub>1</sub>/L<sub>2</sub>) × (L<sub>3</sub>/L<sub>4</sub>) = 50 × (680/44) × (36/40) ≈ 695,45 N."),
      ]),
]

LECT = "Lecture graphique, précision attendue ± 0,5 N. "
PARTIE9 = Q(titre="Forces et vecteurs (géométrie)", minutes=22,
            intro="Dans tous les cas ci-dessous, les forces sont dans le plan (x, y) : la composante sur z est donc nulle.",
            blocs=[
                Q(sub="Cas A — Force F de norme 40 N, α = 69°",
                  intro="Attention : ici l'angle α = 69° est mesuré à partir de l'axe vertical (vers le bas), pas de l'axe horizontal. La force est donc presque horizontale (21° sous l'axe x).",
                  fig=fig("f13.png", "Repère (x, y) ; force F dirigée vers le bas et la droite ; angle α mesuré entre l'axe vertical descendant et F", 460),
                  questions=[
                      Q(s="Calculer la composante F<sub>x</sub> du vecteur F. (en N)", h="Arrondir au centième. " + UNITE,
                        g=num(37.34, 0.02, U_N), att="F<sub>x</sub> ≈ 37,34 N",
                        e="α est mesuré depuis la verticale descendante. La projection sur x utilise donc le sinus : <b>F<sub>x</sub> = F·sin(α) = 40 × sin(69°) ≈ 37,34 N</b> (positive, vers la droite)."),
                      Q(s="Calculer la composante F<sub>y</sub> du vecteur F. (en N)", h="Arrondir au centième. Attention au signe. " + UNITE,
                        g=num(-14.33, 0.02, U_N), att="F<sub>y</sub> ≈ −14,33 N",
                        e="F pointe vers le bas : F<sub>y</sub> est négative. <b>F<sub>y</sub> = −F·cos(α) = −40 × cos(69°) ≈ −14,33 N</b>."),
                      Q(s="Calculer la composante F<sub>z</sub> du vecteur F. (en N)", h=UNITE,
                        g=num(0, 0.001, U_N), att="F<sub>z</sub> = 0 N",
                        e="La force est dans le plan (x, y), donc <b>F<sub>z</sub> = 0 N</b>."),
                  ]),
                Q(sub="Cas B — Lecture graphique de la force F",
                  intro="Lire les coordonnées de F directement sur le quadrillage (graduations en N), puis en déduire la norme et l'angle α (mesuré depuis l'axe x).",
                  fig=fig("f14.png", "Repère (x, y) gradué en newtons ; vecteur F tracé depuis l'origine ; angle α entre l'axe x et F", 520),
                  questions=[
                      Q(s="Relever la coordonnée F<sub>x</sub>. (en N)", h=LECT + UNITE,
                        g=num(10, 0.5, U_N), att="F<sub>x</sub> = 10 N",
                        e="L'extrémité du vecteur se lit à x = 10. <b>F<sub>x</sub> = 10 N</b>."),
                      Q(s="Relever la coordonnée F<sub>y</sub>. (en N)", h=LECT + UNITE,
                        g=num(6, 0.5, U_N), att="F<sub>y</sub> = 6 N",
                        e="L'extrémité du vecteur se lit à y = 6. <b>F<sub>y</sub> = 6 N</b>."),
                      Q(s="Relever la coordonnée F<sub>z</sub>. (en N)", h=LECT + UNITE,
                        g=num(0, 0.5, U_N), att="F<sub>z</sub> = 0 N",
                        e="Force dans le plan (x, y) : <b>F<sub>z</sub> = 0 N</b>."),
                      Q(s="Calculer la norme du vecteur F, sachant que F<sub>x</sub> = 10 N et F<sub>y</sub> = 6 N. (en N)", h="Arrondir au centième. " + UNITE,
                        g=num(11.66, 0.02, U_N), att="F ≈ 11,66 N",
                        e="<b>F = √(F<sub>x</sub>² + F<sub>y</sub>²) = √(10² + 6²) = √136 ≈ 11,66 N</b>."),
                      Q(s="Calculer l'angle α (entre F et l'axe x), sachant que F<sub>x</sub> = 10 N et F<sub>y</sub> = 6 N. (en degrés)", h="Arrondir au degré. " + UNITE,
                        g=num(30.96, 0.5, U_DEG), att="α ≈ 31°",
                        e="<b>α = arctan(F<sub>y</sub>/F<sub>x</sub>) = arctan(6/10) ≈ 30,96° ≈ 31°</b>."),
                  ]),
                Q(sub="Cas C — Trois forces P, F₁ et F₂",
                  intro="Lire sur le graphique les coordonnées des trois forces, puis calculer la résultante R = P + F₁ + F₂ et sa norme. Graduations en N.",
                  fig=fig("f15.png", "Repère (x, y) gradué en newtons ; poids P vers le bas ; forces F1 vers le haut et la droite, F2 vers le haut et la gauche ; angle α", 560),
                  questions=[
                      Q(s="Coordonnée P<sub>x</sub> du poids P. (en N)", h=LECT + UNITE,
                        g=num(0, 0.5, U_N), att="P<sub>x</sub> = 0 N",
                        e="P est vertical (vers le bas) : <b>P<sub>x</sub> = 0 N</b>."),
                      Q(s="Coordonnée P<sub>y</sub> du poids P. (en N)", h=LECT + "Attention au signe. " + UNITE,
                        g=num(-12, 0.5, U_N), att="P<sub>y</sub> = −12 N",
                        e="P pointe vers le bas jusqu'à −12 : <b>P<sub>y</sub> = −12 N</b>."),
                      Q(s="Coordonnée F<sub>1x</sub>. (en N)", h=LECT + UNITE,
                        g=num(10, 0.5, U_N), att="F<sub>1x</sub> = 10 N", e="<b>F<sub>1x</sub> = 10 N</b>."),
                      Q(s="Coordonnée F<sub>1y</sub>. (en N)", h=LECT + UNITE,
                        g=num(6, 0.5, U_N), att="F<sub>1y</sub> = 6 N", e="<b>F<sub>1y</sub> = 6 N</b>."),
                      Q(s="Coordonnée F<sub>2x</sub>. (en N)", h=LECT + "Attention au signe. " + UNITE,
                        g=num(-10, 0.5, U_N), att="F<sub>2x</sub> = −10 N",
                        e="F<sub>2</sub> pointe vers la gauche : <b>F<sub>2x</sub> = −10 N</b>."),
                      Q(s="Coordonnée F<sub>2y</sub>. (en N)", h=LECT + UNITE,
                        g=num(6, 0.5, U_N), att="F<sub>2y</sub> = 6 N", e="<b>F<sub>2y</sub> = 6 N</b>."),
                      Q(s="Composante R<sub>x</sub> de la résultante. (en N)", h="Tolérance ± 0,5 N (erreurs de lecture cumulées). " + UNITE,
                        g=num(0, 0.5, U_N), att="R<sub>x</sub> = 0 N",
                        e="R<sub>x</sub> = P<sub>x</sub> + F<sub>1x</sub> + F<sub>2x</sub> = 0 + 10 + (−10) = <b>0 N</b>."),
                      Q(s="Composante R<sub>y</sub> de la résultante. (en N)", h="Tolérance ± 0,5 N (erreurs de lecture cumulées). " + UNITE,
                        g=num(0, 0.5, U_N), att="R<sub>y</sub> = 0 N",
                        e="R<sub>y</sub> = P<sub>y</sub> + F<sub>1y</sub> + F<sub>2y</sub> = −12 + 6 + 6 = <b>0 N</b>."),
                      Q(s="Composante R<sub>z</sub> de la résultante. (en N)", h=UNITE,
                        g=num(0, 0.001, U_N), att="R<sub>z</sub> = 0 N",
                        e="Tout est dans le plan (x, y) : <b>R<sub>z</sub> = 0 N</b>."),
                      Q(s="Norme de la résultante R. (en N)", h="Tolérance ± 1 N (erreurs de lecture cumulées). " + UNITE,
                        g=num(0, 1, U_N), att="R = 0 N",
                        e="<b>R = √(0² + 0² + 0²) = 0 N</b>."),
                      Q(s="Conclusion : la situation du système est inconnue, le système est en mouvement, ou le système est à l'équilibre&nbsp;?",
                        h="Réponds par&nbsp;: inconnue / en mouvement / à l'équilibre.", g=G_EQUILIBRE, att="Le système est à l'équilibre",
                        e="La résultante est nulle (R = 0 N), donc le <b>système est à l'équilibre</b>."),
                  ]),
            ])
PARTIES.append(PARTIE9)

METHODE = """<h3>Moment d'une force, équilibre et vecteurs</h3>
<ol>
<li><b>Moment d'une force par rapport à un point O</b> : M = F × d, où d est le <b>bras de levier</b>, c'est-à-dire la distance <b>perpendiculaire</b> entre O et la ligne d'action de la force. Ce n'est pas la distance entre O et le point d'application. Pour une force verticale, on mesure la distance horizontale ; pour une force horizontale, la distance verticale.</li>
<li><b>Unité</b> : le moment s'exprime en N·m quand la force est en N et la distance en m (en N·mm si la distance est en mm : convertir en fin de calcul).</li>
<li><b>Force oblique</b> : seule la partie de la force qui est perpendiculaire au bras fait tourner. Projette la force, ou cherche le bras de levier en traçant la perpendiculaire à la ligne d'action.</li>
<li><b>Plusieurs forces</b> : on fixe un sens positif (par convention le sens anti-horaire) et on additionne les moments avec leur signe. Un résultat positif tourne dans le sens choisi comme positif, un résultat négatif dans le sens contraire.</li>
<li><b>Équilibre autour d'un point</b> : la somme des moments est nulle, donc moments horaires = moments anti-horaires.</li>
<li><b>Basculement autour d'une arête</b> : on compare le moment qui renverse le solide au moment stabilisateur (celui qui maintient le solide posé). Le solide bascule dès que le premier dépasse le second.</li>
<li><b>Double levier</b> : on calcule d'abord la force transmise par le premier levier, puis on l'utilise comme donnée du second.</li>
<li><b>Composantes d'une force plane</b> : dessine le triangle rectangle formé par F et ses projections. Selon que l'angle est mesuré depuis l'axe x ou depuis l'axe y, la composante prend le cosinus ou le sinus de l'angle. Le signe se déduit du sens de la flèche sur l'axe.</li>
<li><b>Norme et angle</b> : F = √(F<sub>x</sub>² + F<sub>y</sub>² + F<sub>z</sub>²) ; l'angle avec l'axe x vérifie tan α = F<sub>y</sub> / F<sub>x</sub>.</li>
<li><b>Résultante</b> : on additionne les forces composante par composante. Si la résultante est nulle, la somme des forces est nulle.</li>
</ol>"""


# ---------------------------------------------------------------- outils
def esc(s):
    return html.escape(s, quote=True)


def data_uri(nom):
    mime = "image/jpeg" if nom.endswith(".jpg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode((IMG / nom).read_bytes()).decode()


def taille(nom):
    from struct import unpack
    d = (IMG / nom).read_bytes()
    if nom.endswith(".png"):
        return unpack(">II", d[16:24])
    i = 2
    while i < len(d):  # JPEG : cherche le marqueur SOF
        m, l = d[i + 1], int.from_bytes(d[i + 2:i + 4], "big")
        if 0xC0 <= m <= 0xC3:
            return unpack(">HH", d[i + 5:i + 9])[::-1]
        i += 2 + l
    raise ValueError(nom)


def figure(f):
    w, h = taille(f["f"])
    return (f'<figure class="q-fig" style="max-width:{f["w"]}px"><img src="{data_uri(f["f"])}" alt="{esc(f["alt"])}" '
            f'width="{w}" height="{h}"></figure>')


def fr1(x):
    return str(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)).replace(".", ",")


def duree(m):
    return f"{m} min" if m < 60 else f"{m // 60} h {m % 60:02d}"


def question(pid, n, q, cfg):
    qid, label = f"q{pid}_{n}", f"Q{pid}.{n}"
    cfg[qid] = {"label": label, "part": str(pid), "pts": 1, "grader": q["g"]}
    return f"""
        <div class="q" id="{qid}" data-q="{qid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{q["s"]}</strong></p>
          <p class="q-hint" id="h-{qid}">{q["h"]}</p>
          <div class="q-row">
            <input type="text" class="q-input" id="in-{qid}" aria-label="Réponse {label}" aria-describedby="h-{qid}" autocomplete="off" autocapitalize="off" spellcheck="false">
            <button type="button" class="btn btn-validate">Valider</button>
            <span class="q-status" aria-live="polite"></span>
            <span class="print-only pstat">Non validée : comptée fausse</span>
          </div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="q-unit-msg" hidden></p>
            <p class="q-expected"><span>Réponse attendue :</span> {q["att"]}</p>
            <div class="q-why"><p>{q["e"]}</p></div>
          </div>
        </div>"""


def partie(pid, p, total, cfg):
    blocs = p.get("blocs") or [Q(questions=p["questions"], fig=p.get("fig"))]
    nq = sum(len(b["questions"]) for b in blocs)
    pct = fr1(Decimal(p["minutes"]) * 100 / total)
    body, n = [], 0
    methode = ('<p class="only-training small">Besoin d\'un rappel ? <button type="button" class="doc-chip training-only" '
               'data-doc="METH" aria-pressed="false">Méthode</button></p>')
    body.append(f'<p>{p["intro"]}</p>')
    body.append(methode)
    for b in blocs:
        if b.get("sub"):
            body.append(f'<h3 class="sub-head">{b["sub"]}</h3><p>{b["intro"]}</p>')
        if b.get("fig"):
            body.append(figure(b["fig"]))
        for q in b["questions"]:
            n += 1
            if q.get("fig"):
                body.append(figure(q["fig"]))
            body.append(question(pid, n, q, cfg))
    return nq, f"""
  <section class="part" id="partie-{pid}" aria-labelledby="t-partie-{pid}">
    <header class="part-head"><div class="part-num" aria-hidden="true">{pid}</div>
      <div><h2 id="t-partie-{pid}"><span class="sr-only">Partie {pid} : </span>{p["titre"]}</h2>
        <div class="duree">Durée conseillée : {duree(p["minutes"])} · Barème : {nq} point{"s" if nq > 1 else ""}, soit {pct} % de la note</div></div></header>
    <div class="part-body">
      {"".join(body)}
    </div>
  </section>
"""


def construire():
    g = GABARIT.read_text(encoding="utf-8")
    total = sum(p["minutes"] for p in PARTIES)
    cfg, parts_cfg, sections, nq_total = {}, [], [], 0
    for i, p in enumerate(PARTIES, 1):
        nq, sec = partie(i, p, total, cfg)
        nq_total += nq
        sections.append(sec)
        parts_cfg.append({"num": str(i), "title": p["titre"], "minutes": p["minutes"], "duration": duree(p["minutes"]), "points": nq})
    assert nq_total == len(cfg) == 39, (nq_total, len(cfg))
    dur_totale = duree(total)

    # --- en-tête : on retire le mode d'emploi du gabarit, on garde ses règles en commentaire court
    i0, i1 = g.index("<!-- ====="), g.index("=== -->") + len("=== -->")
    g = g[:i0] + "<!-- Page construite par src/construire_force_moment.py à partir du gabarit : ne pas modifier à la main. -->" + g[i1:]
    t0, t1 = g.index("<title>"), g.index("<style>:root{")
    g = g[:t0] + (f"<title>{TITRE} — exercice interactif</title>\n"
                  '<meta name="description" content="Moment d\'une force, bras de levier, équilibre, basculement, double levier '
                  'et composantes d\'une force : neuf parties à faire en mode entraînement ou en mode examen.">\n') + g[t1:]
    # --- rail, panneau des documents, accueil
    a0, a1 = g.index("<!-- RAIL DES DOCUMENTS"), g.index('<main class="page">')
    hero = data_uri("f12.jpg")
    hw, hh = taille("f12.jpg")
    accueil = f"""<!-- RAIL DES DOCUMENTS : la méthode est une aide du mode entraînement (classe training-only) -->
<nav class="rail" aria-label="Méthode">
  <button type="button" class="tab dt meth training-only" data-doc="METH" aria-selected="false" title="Méthode (mode entraînement uniquement)">Méthode</button>
</nav>

<aside id="docpanel" aria-label="Documents du sujet" aria-hidden="true">
  <div class="dp-head">
    <h3 id="dp-title">Documents</h3>
    <button type="button" id="dp-out" aria-label="Réduire">−</button><span id="dp-zoom" class="small">100 %</span>
    <button type="button" id="dp-in" aria-label="Agrandir">+</button>
    <button type="button" id="dp-fit">Ajuster</button>
    <button type="button" id="dp-close">Fermer</button>
  </div>
  <div class="dp-tabs" role="tablist" aria-label="Choisir un document">
    <button type="button" class="training-only" data-doc="METH" aria-selected="false">Méthode</button>
  </div>
  <div class="dp-body">
    <section class="doc training-only" id="doc-METH" data-title="Méthode : moment d'une force" data-kind="Rappel de méthode · mode entraînement">
      <div class="doc-text">{METHODE}</div>
    </section>
  </div>
</aside>

<!-- PAGE D'ACCUEIL -->
<section id="home" aria-labelledby="home-title">
  <div class="home-inner">
    <header class="home-head">
      <h1 id="home-title">{TITRE}</h1>
      <p class="home-sub">{SOUS_TITRE}</p>
    </header>
    <figure class="home-hero">
      <img src="{hero}" alt="Coupe-boulon à double levier, avec ses cotes et ses forces" width="{hw}" height="{hh}">
      <figcaption>Le coupe-boulon : un double levier, étudié dans la partie 8.</figcaption>
    </figure>
    <div class="home-facts">
      <div><b>{len(PARTIES)} parties</b><span>{nq_total} questions courtes</span></div>
      <div><b>{dur_totale.replace(" h ", " h ")}</b><span>durée conseillée, qui fixe la pondération</span></div>
      <div><b>1 document</b><span>méthode, en mode entraînement</span></div>
      <div><b>0 tracé</b><span>toutes les réponses se saisissent au clavier</span></div>
    </div>
    <h2 class="home-choose">Choisis ton mode de travail</h2>
    <div class="modes">
      <article class="mode-card">
        <div class="mc-head"><span class="mc-tag">Mode 1</span><h3>Mode entraînement</h3></div>
        <p class="mc-lead">Pour apprendre en avançant, question par question.</p>
        <ul><li>Chaque question se valide isolément ; la démarche corrigée s'affiche aussitôt.</li>
          <li>La note pondérée s'actualise en continu dans le bandeau.</li>
          <li>Une fiche de méthode est consultable à tout moment, sans contrainte de temps.</li></ul>
        <button type="button" class="btn btn-mode" data-mode="training">Commencer l'entraînement</button>
      </article>
      <article class="mode-card exam">
        <div class="mc-head"><span class="mc-tag">Mode 2</span><h3>Mode examen</h3></div>
        <p class="mc-lead">Pour se placer en conditions de contrôle.</p>
        <ul><li>Aucune correction, aucune note et <b>aucun accès à la méthode</b> pendant la composition ; les réponses restent modifiables.</li>
          <li>Le chronomètre tourne, à comparer à la durée conseillée.</li>
          <li>En fin de sujet, le bouton « J'ai fini, je fais corriger ma copie » dévoile d'un coup les corrections, les notes par partie et la note globale.</li></ul>
        <button type="button" class="btn btn-mode" data-mode="exam">Composer en mode examen</button>
      </article>
    </div>
    <p class="home-note small">Le mode se choisit une seule fois : pour en changer, recharge la page. Rien n'est enregistré sur l'ordinateur.</p>
  </div>
</section>

"""
    g = g[:a0] + accueil + g[a1:]
    # --- page principale
    m0, m1 = g.index('<main class="page">'), g.index("</main>") + len("</main>")
    main = f"""<main class="page">
  <section class="print-only print-summary">
    <p>Élève : <span class="print-nom"></span> | Copie imprimée le <span class="print-date"></span></p>
    <p>Mode : <span class="print-mode"></span> | Temps de rédaction : <strong class="print-time"></strong> (durée conseillée : {dur_totale})</p>
    <p class="print-note-line">Note finale pondérée : <strong class="final-note"></strong></p>
    <p class="print-nograde">Copie non corrigée : les corrections et la note n'apparaissent qu'après la remise de la copie en mode examen.</p>
  </section>

  <header class="cartouche">
    <div class="title">
      <h1>{TITRE}</h1>
      <p>{nq_total} questions notées, réparties en {len(PARTIES)} parties pondérées par leur durée conseillée.</p></div>
    <div class="nom"><label for="nom-eleve">Nom et prénom</label><input id="nom-eleve" type="text" autocomplete="name"></div>
  </header>

  <div class="consignes">
    <p class="only-training"><strong>Mode entraînement.</strong> Réponds dans chaque champ puis clique sur « Valider » : une réponse validée est définitive et sa correction s'affiche aussitôt. La fiche « Méthode » (onglet sur le bord droit) rappelle les outils utiles.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Compose tout le sujet sans correction, sans note et sans accès à la méthode : tes réponses restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections, les notes par partie et la note globale.</p>
    <p><strong>Les unités sont notées.</strong> Pour toute question numérique portant une unité, la valeur vaut la moitié des points et l'unité l'autre moitié : une valeur juste écrite sans unité, ou avec une unité fausse, ne rapporte qu'un demi-point. Les coefficients sans unité n'en demandent pas.</p>
    <p><strong>Barème pondéré par la durée conseillée</strong> : chaque partie est notée sur 20, puis pèse au prorata de son temps. Le récapitulatif de fin de sujet donne le détail partie par partie.</p>
  </div>
{"".join(sections)}
  <section class="recap" id="recap" aria-labelledby="t-recap">
    <header class="recap-head"><h2 id="t-recap">Récapitulatif et note finale</h2>
      <p class="small">Les questions non validées comptent comme fausses. Chaque partie est ramenée sur 20, puis pondérée par sa durée conseillée.</p></header>
    <div id="exam-submit-wrap">
      <p class="es-lead">Ta copie n'est pas encore corrigée : aucune réponse n'est verrouillée, tu peux encore revenir sur les questions.</p>
      <button type="button" class="btn btn-exam" id="exam-submit">J'ai fini, je fais corriger ma copie</button>
      <p class="es-warn" id="exam-warn" role="alert"></p>
    </div>
    <div id="recap-graded">
      <div class="recap-wrap">
        <table class="t recap-table">
          <thead><tr><th>Partie</th><th>Durée</th><th>Poids</th><th>Points</th><th>Note /20</th><th>Contribution</th></tr></thead>
          <tbody id="recap-body"></tbody>
          <tfoot><tr><th colspan="4">Note globale pondérée</th><th class="final-note"></th><th></th></tr></tfoot>
        </table>
      </div>
      <p class="final-detail small"></p>
    </div>
    <div class="recap-foot" id="recap-foot"><button type="button" class="btn btn-print">Imprimer ma copie</button>
      <span class="small no-print">L'impression reprend tes réponses, les corrections et ce récapitulatif.</span></div>
  </section>
</main>"""
    g = g[:m0] + main + g[m1:]
    # --- configuration
    c0 = g.index("<script>window.__PARTS__")
    c1 = g.index("</script>", c0) + len("</script>")
    conf = ("<script>window.__PARTS__ = " + json.dumps(parts_cfg, ensure_ascii=False) + ";\n"
            "window.__QCFG__ = " + json.dumps(cfg, ensure_ascii=False) + ";\n"
            "window.__SKCFG__ = {};</script>")
    g = g[:c0] + conf + g[c1:]
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(g, encoding="utf-8")
    print(f"{SORTIE.relative_to(ROOT)} : {len(g.encode('utf-8')) / 1024:.0f} Kio, {nq_total} questions, {dur_totale}")


if __name__ == "__main__":
    construire()
