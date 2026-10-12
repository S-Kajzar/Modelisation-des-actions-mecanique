#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit l'exercice « Force, moment et couple » à partir du gabarit (src/gabarit-exercice-interactif.html).

    python3 src/construire_force_moment.py     # écrit src/exercices/force-moment-source.html
    python3 src/generer.py                     # publie force-moment.html (avec le lien de retour vers l'accueil)

Le bloc <style> et les deux scripts du gabarit (moteur de correction et moteur applicatif) sont repris tels quels :
seuls le titre, la page d'accueil, les documents, le contenu des parties et la configuration (__PARTS__, __QCFG__,
__SKCFG__) sont réécrits ici. Les figures sont dans src/images/force-moment/.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commun import (Q, UNITE, U_DEG, U_M, U_N, U_NM, CONSIGNE_COLONNE, H_VEC, IMAGES, ROOT, VEC, VI, VQ, cn,  # noqa: E402
                    construire_exercice, fig as _fig, kw, num)

IMG = IMAGES / "force-moment"
SORTIE = ROOT / "src" / "exercices" / "force-moment-source.html"

TITRE = "Force, moment et couple"
SOUS_TITRE = ("Neuf parties courtes pour maîtriser le moment d'une force : bras de levier, équilibre, basculement, "
              "double levier et composantes d'une force. Les réponses se saisissent au clavier, unités comprises.")

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
# Chaque question : énoncé s, consigne h, correcteur g, réponse attendue att, démarche e[, figure fig]
def fig(nom, alt, w):
    return _fig(IMG / nom, alt, w)


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
                      VQ("Écrire le vecteur F dans le repère (x, y, z), composantes arrondies au centième.",
                         "α est mesuré depuis la verticale descendante : la projection sur x utilise le sinus, celle sur y "
                         "le cosinus. <b>F<sub>x</sub> = F·sin(α) = 40 × sin(69°) ≈ 37,34 N</b>, positive (vers la droite). "
                         "F pointe vers le bas : <b>F<sub>y</sub> = −F·cos(α) = −40 × cos(69°) ≈ −14,33 N</b>. La force est "
                         "dans le plan (x, y) : <b>F<sub>z</sub> = 0</b>.",
                         VI(VEC("F"), [cn("x", 37.34, 0.02), cn("y", -14.33, 0.02), cn("z", 0, 0.001)], "N")),
                  ]),
                Q(sub="Cas B — Lecture graphique de la force F",
                  intro="Lire les coordonnées de F directement sur le quadrillage (graduations en N), puis en déduire la norme et l'angle α (mesuré depuis l'axe x).",
                  fig=fig("f14.png", "Repère (x, y) gradué en newtons ; vecteur F tracé depuis l'origine ; angle α entre l'axe x et F", 520),
                  questions=[
                      VQ("Relever les coordonnées du vecteur F.",
                         "L'extrémité du vecteur se lit à x = 10 et y = 6 ; la force est dans le plan (x, y). <b>F = (10 ; 6 ; 0) N</b>.",
                         VI(VEC("F"), [cn("x", 10, 0.5, 0), cn("y", 6, 0.5, 0), cn("z", 0, 0.5, 0)], "N"), h=LECT + H_VEC),
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
                      VQ("Relever les coordonnées des trois forces P, F<sub>1</sub> et F<sub>2</sub>.",
                         "P est vertical, vers le bas jusqu'à −12 : <b>P = (0 ; −12) N</b>. <b>F<sub>1</sub> = (10 ; 6) N</b>. "
                         "F<sub>2</sub> pointe vers la gauche : <b>F<sub>2</sub> = (−10 ; 6) N</b>.",
                         VI(VEC("P"), [cn("x", 0, 0.5, 0), cn("y", -12, 0.5, 0)], "N"),
                         VI(VEC("F") + "<sub>1</sub>", [cn("x", 10, 0.5, 0), cn("y", 6, 0.5, 0)], "N"),
                         VI(VEC("F") + "<sub>2</sub>", [cn("x", -10, 0.5, 0), cn("y", 6, 0.5, 0)], "N"),
                         h=LECT + "Attention aux signes. " + H_VEC),
                      VQ("Écrire la résultante R = P + F<sub>1</sub> + F<sub>2</sub> dans le repère (x, y, z).",
                         "On additionne composante par composante : R<sub>x</sub> = 0 + 10 + (−10) = <b>0</b> ; R<sub>y</sub> = "
                         "−12 + 6 + 6 = <b>0</b> ; tout est dans le plan (x, y) : R<sub>z</sub> = <b>0</b>. <b>R = (0 ; 0 ; 0) N</b>.",
                         VI(VEC("R"), [cn("x", 0, 0.5, 0), cn("y", 0, 0.5, 0), cn("z", 0, 0.001, 0)], "N"),
                         h="Tolérance ± 0,5 N (erreurs de lecture cumulées). " + H_VEC),
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


CONSIGNES = ("<p><strong>Les unités sont notées.</strong> Pour toute question numérique portant une unité, la valeur vaut "
             "la moitié des points et l'unité l'autre moitié : une valeur juste écrite sans unité, ou avec une unité fausse, "
             "ne rapporte qu'un demi-point. Les coefficients sans unité n'en demandent pas.</p>", CONSIGNE_COLONNE)


def construire():
    construire_exercice(
        titre=TITRE, sous_titre=SOUS_TITRE, parties=PARTIES, sortie=SORTIE, script="construire_force_moment.py",
        description=("Moment d'une force, bras de levier, équilibre, basculement, double levier et composantes d'une "
                     "force : neuf parties à faire en mode entraînement ou en mode examen."),
        methode_titre="moment d'une force", methode=METHODE, consignes=CONSIGNES, nq_attendu=28,
        hero=Q(f=IMG / "f12.jpg", alt="Coupe-boulon à double levier, avec ses cotes et ses forces",
               cap="Le coupe-boulon : un double levier, étudié dans la partie 8."),
        facts=[("9 parties", "28 questions, dont 4 vecteurs en colonne"), ("1 h 20", "durée conseillée, qui fixe la pondération"),
               ("1 document", "méthode, en mode entraînement"), ("0 tracé", "toutes les réponses se saisissent au clavier")])


if __name__ == "__main__":
    construire()
