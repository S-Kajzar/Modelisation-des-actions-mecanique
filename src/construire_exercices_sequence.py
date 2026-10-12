#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercices de la séquence « Modélisation des actions mécaniques : force, couple, torseur », construits sur le gabarit.

    python3 src/construire_exercices_sequence.py   # écrit src/exercices/{projections,couples-moments,torseurs}-source.html
    python3 src/generer.py                          # publie les pages avec le lien de retour vers l'accueil

  - Exercice 1.2 (niveau 1) : exercices 1 à 4 de la séquence (projections) ;
  - Exercice 2.1 (niveau 2) : exercices 5 à 9 (couples et moments) ;
  - Exercice 2.2 (niveau 2) : exercices 10 à 14 (torseurs, les bases).

Les figures viennent de src/images/sequence/ (outils/extraire_figures.py). Chaque résultat est recalculé ici :
les valeurs attendues sont écrites en clair, les démarches dans « e ».
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commun import (NO, Q, ROOT, UNITE, U_DAN, U_DANM, U_DANMM, U_DEG, U_KG, U_N, U_NM, U_NMM,  # noqa: E402,F401
                    CONSIGNE_COLONNE, H_VEC, VEC, VI, VQ, cn, construire_exercice, expr, fig as _fig, nb, num)

IMG = "sequence/"
SRC = ROOT / "src" / "exercices"


def fig(nom, alt, w, cap=""):
    return _fig(IMG + nom, alt, w, cap)


H_C = "Arrondir au centième. " + UNITE
H_C_SIGNE = "Arrondir au centième. Attention au signe. " + UNITE
H_U = "Arrondir à l'unité. " + UNITE
H_EX = "Valeur exacte. " + UNITE
NOMS = {"f": "f", "α": "alpha", "alpha": "alpha", "a": "alpha", "β": "beta", "beta": "beta", "b": "beta"}
H_LIT = ("Expression littérale en fonction de F et de α (écris α, alpha ou a), avec <code>*</code> pour multiplier et "
         "<code>sin(…)</code>, <code>cos(…)</code>. Le signe compte.")
H_LIT2 = ("Expression littérale en fonction de F, α et β (écris α ou alpha, β ou beta), avec <code>*</code> pour "
          "multiplier et <code>sin(…)</code>, <code>cos(…)</code>. Le signe compte.")
H_TORSEUR = ("Remplis les six cases, zéros compris. Résultante (X, Y, Z) en {r}, moment (L, M, N) en {m}. "
             "Arrondir au centième.")


def lit(expected, angles):
    """Formule littérale : F et les angles prennent trois jeux de valeurs (le premier est celui de l'énoncé)."""
    v = {"f": [1000, 650, 1300]}
    v.update(angles)
    return expr(expected, v, NOMS)


def vec(*c):
    return "(" + " ; ".join(c) + ")"


# =====================================================================================================================
# EXERCICE 1.2 — PROJECTIONS (niveau 1) : exercices 1 à 4
# =====================================================================================================================
def cas_support(lettre, titre, image, alt, expected_x, expected_y, angles, vx, vy, ex, ey, en, h_lit=H_LIT):
    """Un cas : le vecteur F écrit en colonne, d'abord en fonction de F et des angles, puis pour F = 1 000 N."""
    def membre(s):
        return s.split(" = ", 1)[1]
    return Q(sub=f"Cas {lettre} — {titre}", fig=fig(image, alt, 300), questions=[
        VQ(f"Cas {lettre} : écrire le vecteur F en colonne, d'abord en fonction de F et des angles, puis en newtons "
           f"pour F = 1 000 N.",
           f"{ex[1]} {ey[1]}<br>{en[0]} {en[1]}",
           VI(VEC("F"), [("x", lit(expected_x, angles), membre(ex[0])), ("y", lit(expected_y, angles), membre(ey[0]))],
              lit=True),
           VI(VEC("F"), [cn("x", round(vx, 2)), cn("y", round(vy, 2))], "N"),
           h=h_lit + " Puis les valeurs en newtons, arrondies au centième, signe compris."),
    ])


PROJECTIONS = [
    Q(titre="Composantes d'une action sur une dent", minutes=6,
      intro="L'action <b>F</b> exercée en I sur une dent de la roue a pour intensité F = 1 000 N ; elle est inclinée de "
            "l'angle de pression α = 20° sur l'axe x. On cherche sa composante tangentielle F<sub>t</sub> (sur x), "
            "qui fait tourner la roue, et sa composante radiale F<sub>r</sub> (sur y), dirigée vers le centre.",
      fig=fig("e01-engrenage.jpg", "Roue dentée ; au point I, la force F inclinée de α sur l'axe x, avec ses "
                                   "composantes Ft sur x et Fr sur y", 440),
      questions=[
          Q(s="Déterminer la composante tangentielle F<sub>t</sub>.", h=H_C, g=num(939.69, 0.01, U_N),
            att="F<sub>t</sub> = F × cos α ≈ 939,69 N",
            e="Dans le triangle rectangle formé par F (l'hypoténuse), F<sub>t</sub> et F<sub>r</sub>, F<sub>t</sub> est "
              "le côté <b>adjacent</b> à l'angle α : F<sub>t</sub> = F × cos α = 1 000 × cos 20° ≈ <b>939,69 N</b>."),
          Q(s="Déterminer la composante radiale F<sub>r</sub>.", h=H_C, g=num(342.02, 0.01, U_N),
            att="F<sub>r</sub> = F × sin α ≈ 342,02 N",
            e="F<sub>r</sub> est le côté <b>opposé</b> à l'angle α : F<sub>r</sub> = F × sin α = 1 000 × sin 20° ≈ "
              "<b>342,02 N</b>. Vérification : √(939,69² + 342,02²) ≈ 1 000 N, l'intensité de F."),
      ]),
    Q(titre="Supports inclinés : quatre repères", minutes=24,
      intro="Pour chacun des quatre supports, le repère R (x, y) est lié au support : il n'est pas toujours horizontal. "
            "Exprime d'abord les coordonnées de F en fonction de son intensité F et des angles donnés, puis fais "
            "l'application numérique pour F = 1 000 N.",
      blocs=[
          cas_support("a", "α = 30°", "e02-a.jpg", "Cas a : support vertical, x dirigé vers le bas le long du support, "
                      "F inclinée de α = 30° sur l'axe x", "f*cos(alpha)", "f*sin(alpha)", {"alpha": [30, 37, 61]},
                      866.03, 500.0,
                      ("F<sub>x</sub> = F × cos α",
                       "α = 30° est mesuré entre F et l'axe x : la projection sur x est le côté <b>adjacent</b>. F pointe "
                       "du côté des x positifs : <b>F<sub>x</sub> = F cos α</b>."),
                      ("F<sub>y</sub> = F × sin α",
                       "La projection sur y est le côté <b>opposé</b> à α, du côté des y positifs : "
                       "<b>F<sub>y</sub> = F sin α</b>."),
                      ("F<sub>x</sub> = 1 000 × cos 30° ≈ <b>866,03 N</b>.", "F<sub>y</sub> = 1 000 × sin 30° = <b>500 N</b>.")),
          cas_support("b", "α = 45°", "e02-b.jpg", "Cas b : support incliné, y le long du support vers le haut, F "
                      "dirigée vers le bas, à α = 45° de l'axe y", "-f*sin(alpha)", "-f*cos(alpha)",
                      {"alpha": [45, 37, 61]}, -707.11, -707.11,
                      ("F<sub>x</sub> = −F × sin α",
                       "α = 45° est mesuré entre la droite d'action de F et l'axe y. F pointe vers le bas du support et "
                       "vers les x négatifs. Sa projection sur x est le côté <b>opposé</b> à α : "
                       "<b>F<sub>x</sub> = −F sin α</b>."),
                      ("F<sub>y</sub> = −F × cos α",
                       "La projection sur y est le côté <b>adjacent</b> à α, du côté des y négatifs : "
                       "<b>F<sub>y</sub> = −F cos α</b>."),
                      ("F<sub>x</sub> = −1 000 × sin 45° ≈ <b>−707,11 N</b>.",
                       "F<sub>y</sub> = −1 000 × cos 45° ≈ <b>−707,11 N</b> : avec 45°, les deux coordonnées ont la même "
                       "valeur absolue.")),
          cas_support("c", "α = 120°", "e02-c.jpg", "Cas c : support incliné, F dirigée vers le bas et vers la gauche, "
                      "à α = 120° de l'axe y", "-f*sin(alpha)", "f*cos(alpha)", {"alpha": [120, 110, 134]},
                      -866.03, -500.0,
                      ("F<sub>x</sub> = −F × sin α",
                       "α = 120° est l'angle entre l'axe y et le vecteur F. F pointe vers les x négatifs : "
                       "<b>F<sub>x</sub> = −F sin α</b> (sin 120° = sin 60° ≈ 0,866). Écriture équivalente avec l'angle "
                       "aigu 180° − α = 60° : F<sub>x</sub> = −F sin(180° − α)."),
                      ("F<sub>y</sub> = F × cos α",
                       "Avec l'angle mesuré depuis l'axe y, même obtus, <b>F<sub>y</sub> = F cos α</b> donne directement "
                       "le signe : cos 120° = −0,5. Écriture équivalente : F<sub>y</sub> = −F cos(180° − α)."),
                      ("F<sub>x</sub> = −1 000 × sin 120° ≈ <b>−866,03 N</b>.",
                       "F<sub>y</sub> = 1 000 × cos 120° = <b>−500 N</b>.")),
          cas_support("d", "α = 75° et β = 30°", "e02-d.jpg", "Cas d : support coudé incliné de α = 75° sur l'axe x "
                      "horizontal ; F inclinée de β = 30° sur l'axe du support, vers x", "f*cos(alpha-beta)",
                      "f*sin(alpha-beta)", {"alpha": [75, 64, 82], "beta": [30, 21, 27]}, 707.11, 707.11,
                      ("F<sub>x</sub> = F × cos(α − β)",
                       "Le support fait α = 75° avec x et F est inclinée de β = 30° sur l'axe du support, du côté de x : "
                       "F fait donc l'angle α − β = 45° avec l'axe x. <b>F<sub>x</sub> = F cos(α − β)</b>."),
                      ("F<sub>y</sub> = F × sin(α − β)", "<b>F<sub>y</sub> = F sin(α − β)</b>, positive."),
                      ("F<sub>x</sub> = 1 000 × cos 45° ≈ <b>707,11 N</b>.", "F<sub>y</sub> = 1 000 × sin 45° ≈ <b>707,11 N</b>."),
                      h_lit=H_LIT2),
      ]),
    Q(titre="Changement de repère", minutes=10,
      intro="Le support est fixé sur un plan incliné de 30°. La force <b>F</b> (200 N) fait un angle de 40° avec l'axe "
            "horizontal x. R(x, y) est le repère horizontal ; R'(x', y') est lié au support : x' suit le plan incliné "
            "(vers le haut, à gauche) et y' lui est perpendiculaire.",
      fig=fig("e03-support.jpg", "Support sur un plan incliné de 30° ; force F de 200 N à 40° de l'axe x ; repères "
                                 "R (x, y) horizontal et R' (x', y') lié au support", 440),
      questions=[
          VQ("Écrire le vecteur F dans le repère R (x, y), coordonnées arrondies au centième.",
             "F fait 40° avec x : F<sub>x</sub> = F cos 40° = 200 × cos 40° ≈ <b>153,21 N</b> ; F<sub>y</sub> = F sin 40° = "
             "200 × sin 40° ≈ <b>128,56 N</b>.",
             VI(VEC("F"), [cn("x", 153.21), cn("y", 128.56)], "N")),
          VQ("Écrire le vecteur F dans le repère R' (x', y'), coordonnées arrondies au centième.",
             "Le repère R' est tourné de 30° : y' fait 90° − 30° = 60° avec x, donc F (à 40° de x) fait 20° avec y'. L'axe "
             "x' fait 90° de plus que y', soit 110° avec F : F<sub>x'</sub> = F cos 110° = −F sin 20° ≈ <b>−68,40 N</b> "
             "(F pointe du côté opposé à x') ; F<sub>y'</sub> = F cos 20° ≈ <b>187,94 N</b>. Vérification : √(68,40² + "
             "187,94²) ≈ 200 N : changer de repère change les coordonnées, pas l'intensité.",
             VI(VEC("F"), [cn("x'", -68.40), cn("y'", 187.94)], "N"), h=H_VEC + " Attention au signe."),
      ]),
    Q(titre="Gousset : trois barres soudées", minutes=12,
      intro="Trois barres soudées sur un gousset transmettent les tensions T<sub>1</sub> (200 daN, à 45° au-dessus de "
            "l'axe x), T<sub>2</sub> (horizontale) et T<sub>3</sub> (à 30° sous l'axe x).",
      fig=fig("e04-gousset.jpg", "Gousset soudé sur un poteau ; barre 1 à 45° au-dessus de x tendue par T1 (200 daN), "
                                 "barre 2 horizontale avec T2, barre 3 à 30° sous x avec T3", 440),
      questions=[
          VQ("Écrire le vecteur T<sub>1</sub> dans le repère (x, y), coordonnées arrondies au centième.",
             "T<sub>1</sub> fait 45° avec x : T<sub>1x</sub> = 200 × cos 45° ≈ <b>141,42 daN</b> et T<sub>1y</sub> = 200 × "
             "sin 45° ≈ <b>141,42 daN</b> : à 45°, les deux coordonnées sont égales.",
             VI(VEC("T") + "<sub>1</sub>", [cn("x", 141.42), cn("y", 141.42)], "daN")),
          Q(s="T<sub>3</sub> tire vers le bas, sa coordonnée verticale vaut T<sub>3y</sub> = −100 daN. Déterminer "
              "l'intensité T<sub>3</sub>.", h=H_C, g=num(200, 0.01, U_DAN, variants=[(2000, 0.1, U_N)]),
            att="T<sub>3</sub> = 200 daN",
            e="T<sub>3</sub> fait 30° avec x : |T<sub>3y</sub>| = T<sub>3</sub> × sin 30°, donc T<sub>3</sub> = 100 / "
              "sin 30° = 100 / 0,5 = <b>200 daN</b>."),
          Q(s="Déterminer la coordonnée T<sub>3x</sub>.", h=H_C, g=num(173.21, 0.01, U_DAN, variants=[(1732.05, 0.1, U_N)]),
            att="T<sub>3x</sub> ≈ 173,21 daN",
            e="T<sub>3x</sub> = T<sub>3</sub> × cos 30° = 200 × 0,866 ≈ <b>173,21 daN</b>, positive : T<sub>3</sub> "
              "tire vers les x positifs."),
          Q(s="Déterminer l'intensité de T<sub>2</sub>, sachant que T<sub>1x</sub> + T<sub>2x</sub> + T<sub>3x</sub> = 0.",
            h=H_C, g=num(314.63, 0.01, U_DAN, abs_=True, variants=[(3146.26, 0.1, U_N)]), att="T<sub>2</sub> ≈ 314,63 daN",
            e="T<sub>2x</sub> = −(T<sub>1x</sub> + T<sub>3x</sub>) = −(141,42 + 173,21) = −314,63 daN : T<sub>2</sub> est "
              "horizontale, dirigée vers les x négatifs, d'intensité <b>314,63 daN</b>."),
      ]),
]

METHODE_PROJECTIONS = """<h3>Projeter une force sur les axes d'un repère</h3>
<ol>
<li><b>Repère l'angle</b> donné : entre F et quel axe ? (x, y, ou l'axe d'un support).</li>
<li><b>Trace le triangle rectangle</b> formé par F (l'hypoténuse) et ses deux projections.</li>
<li><b>Côté adjacent</b> à l'angle : × cos ; <b>côté opposé</b> : × sin. Angle mesuré depuis x : F<sub>x</sub> = F cos α et F<sub>y</sub> = F sin α. Angle mesuré depuis y : sinus et cosinus s'échangent.</li>
<li><b>Le signe</b> : + si la projection pointe dans le sens de l'axe, − sinon. Avec un angle mesuré depuis le sens positif d'un axe, même obtus, F cos α donne directement le signe.</li>
<li><b>Vérifie</b> : F<sub>x</sub>² + F<sub>y</sub>² = F².</li>
<li><b>Repère incliné</b> : cherche l'angle entre F et chaque axe du nouveau repère, puis projette de la même façon.</li>
<li><b>Nœud en équilibre</b> : la somme des coordonnées des forces sur chaque axe est nulle.</li>
</ol>"""


# =====================================================================================================================
# EXERCICE 2.1 — COUPLES ET MOMENTS (niveau 2) : exercices 5 à 9
# =====================================================================================================================
COUPLES = [
    Q(titre="Couples dans un engrenage", minutes=8,
      intro="Un engrenage est constitué d'un pignon 1 (Ø 50 mm), lié à l'arbre d'un moteur, de centre O<sub>1</sub>, et "
            "d'une roue dentée 2 (Ø 124 mm), liée à l'arbre d'un récepteur, de centre O<sub>2</sub>. L'engrenage étant "
            "normalisé, la force F<sub>1/2</sub> de 20 N exercée par une dent du pignon 1 sur une dent de la roue 2 au "
            "point A est inclinée de l'angle de pression α = 20° sur la tangente commune.",
      fig=fig("e05-engrenage.png", "Pignon 1 de centre O1 au-dessus de la roue 2 de "
              "centre O2 ; au point de contact A, la force F1/2 inclinée de α sous la tangente horizontale", 460),
      questions=[
          Q(s="Déterminer le couple au point O<sub>1</sub> de la force F<sub>1/2</sub> (valeur absolue).", h=H_C,
            g=num(0.47, 0.005, U_NM, abs_=True, variants=[(469.85, 0.5, U_NMM)]), att="C<sub>O1</sub> ≈ 0,47 N·m",
            e="Le bras de levier est la distance de O<sub>1</sub> à la droite d'action de F<sub>1/2</sub>, pas le rayon : "
              "la force est inclinée de α sur la tangente en A. d<sub>1</sub> = r<sub>1</sub> × cos α = 25 × cos 20° ≈ "
              "23,49 mm, donc C<sub>O1</sub> = F × d<sub>1</sub> = 20 × 0,023 49 ≈ <b>0,47 N·m</b>. Autre lecture : "
              "seule la composante tangentielle F cos α ≈ 18,79 N fait tourner, la composante radiale passe par "
              "O<sub>1</sub>. Le moment est positif (sens trigonométrique)."),
          Q(s="Déterminer le couple au point O<sub>2</sub> de la force F<sub>1/2</sub> (valeur absolue).", h=H_C,
            g=num(1.17, 0.005, U_NM, abs_=True, variants=[(1165.22, 0.5, U_NMM)]), att="C<sub>O2</sub> ≈ 1,17 N·m",
            e="Même raisonnement avec r<sub>2</sub> = 62 mm : C<sub>O2</sub> = F × r<sub>2</sub> × cos α = 20 × 0,062 × "
              "cos 20° ≈ <b>1,17 N·m</b>, dans le sens horaire (négatif). Le rapport des couples, 1,17 / 0,47 = 124 / 50 "
              "≈ 2,48, est celui des diamètres : la roue tourne moins vite mais transmet un couple plus grand."),
      ]),
    Q(titre="Poulie et courroie", minutes=10,
      intro="Le rayon d'enroulement de la courroie sur la poulie est R = 100 mm. <b>T</b> (120 daN, brin tendu) et "
            "<b>t</b> (40 daN, brin mou) schématisent les efforts de tension. Repère : x vers la droite, y vers le "
            "haut, z vers toi ; le sens trigonométrique est positif.",
      fig=fig("e06-poulie.jpg", "Poulie de rayon R = 100 mm et de centre A ; brin tendu en haut tiré par T (120 daN), "
                                "brin mou en bas tiré par t (40 daN), inclinés de 10° et 15°", 440),
      questions=[
          Q(s="Calculer la norme du moment au point A de la tension T.", h=H_C,
            g=num(120, 0.01, U_NM, abs_=True, variants=[(12, 0.001, U_DANM), (120000, 1, U_NMM), (12000, 0.1, U_DANMM)]),
            att="‖M<sub>A</sub>(T)‖ = 120 N·m (12 daN·m)",
            e="Le brin est tangent à la poulie : la distance de A à la droite d'action de T est le rayon R, quel que soit "
              "l'angle de 10°. ‖M<sub>A</sub>(T)‖ = T × R = 1 200 N × 0,1 m = <b>120 N·m</b> (12 daN·m)."),
          VQ("Écrire le vecteur moment au point A de la tension T.",
             "T, en haut de la poulie, tire vers la droite : il fait tourner la poulie dans le sens horaire, négatif. Le "
             "moment est porté par z, perpendiculaire au plan de la figure : <b>M<sub>A</sub>(T) = (0 ; 0 ; −120) N·m</b>.",
             VI(VEC("M") + "<sub>A</sub>(" + VEC("T") + ")", [cn("x", 0, 0.001), cn("y", 0, 0.001), cn("z", -120)], "N·m"),
             h=H_VEC + " Attention au signe."),
          Q(s="Calculer la norme du moment au point A de la tension t.", h=H_C,
            g=num(40, 0.01, U_NM, abs_=True, variants=[(4, 0.001, U_DANM), (40000, 1, U_NMM), (4000, 0.1, U_DANMM)]),
            att="‖M<sub>A</sub>(t)‖ = 40 N·m (4 daN·m)",
            e="Même raisonnement : ‖M<sub>A</sub>(t)‖ = t × R = 400 N × 0,1 m = <b>40 N·m</b>."),
          VQ("Écrire le vecteur moment au point A de la tension t.",
             "t, en bas de la poulie, tire vers la droite : il fait tourner la poulie dans le sens trigonométrique, "
             "positif. <b>M<sub>A</sub>(t) = (0 ; 0 ; 40) N·m</b>.",
             VI(VEC("M") + "<sub>A</sub>(" + VEC("t") + ")", [cn("x", 0, 0.001), cn("y", 0, 0.001), cn("z", 40)], "N·m"),
             h=H_VEC + " Attention au signe."),
          Q(s="En déduire le couple disponible sur l'arbre de transmission (valeur absolue).", h=H_C,
            g=num(80, 0.01, U_NM, abs_=True, variants=[(8, 0.001, U_DANM), (80000, 1, U_NMM)]), att="C = 80 N·m (8 daN·m)",
            e="C = M<sub>A</sub>(T) + M<sub>A</sub>(t) = −120 + 40 = −80 N·m : <b>80 N·m</b> dans le sens horaire, celui "
              "de la flèche du dessin. Le couple transmis vient de la différence de tension entre les deux brins."),
      ]),
    Q(titre="Balance romaine", minutes=10,
      intro="Une balance romaine se compose d'un balancier (2) articulé en B avec un anneau de suspension (1) et d'un "
            "contrepoids d'équilibrage (3) dont la position est réglable sur le balancier. La charge à peser (4) est "
            "accrochée en O. La pesée est effectuée en déplaçant le contrepoids q (5 daN).",
      fig=fig("e07-balance.jpg", "Balance romaine : objet de poids P accroché en O, articulation B à la distance b de O, "
                                 "contrepoids q (5 daN) à la distance a de B", 640),
      questions=[
          Q(s="Au moment de la pesée, le balancier est en équilibre horizontal : M<sub>B</sub>(P) + M<sub>B</sub>(q) = 0. "
              "Exprimer littéralement P en fonction de q, a et b.",
            h="Écris P = … avec <code>*</code> pour multiplier et <code>/</code> pour diviser.",
            g=expr("q*a/b", {"q": [5, 3, 7], "a": [700, 450, 820], "b": [100, 130, 90]}, {"q": "q", "a": "a", "b": "b"}),
            att="P = q × a / b",
            e="Autour de B, P (à gauche, à la distance b) fait tourner le balancier dans le sens trigonométrique : "
              "M<sub>B</sub>(P) = +P × b. q (à droite, à la distance a) le fait tourner dans le sens horaire : "
              "M<sub>B</sub>(q) = −q × a. L'équilibre donne P × b − q × a = 0, soit <b>P = q × a / b</b>. La force F de "
              "l'anneau passe par B : son moment en B est nul."),
          Q(s="Calculer le poids P de l'objet si a = 700 mm et b = 100 mm.", h=H_EX,
            g=num(35, 0.01, U_DAN, variants=[(350, 0.1, U_N)]), att="P = 35 daN (350 N)",
            e="P = q × a / b = 5 × 700 / 100 = <b>35 daN</b>, soit 350 N. Le contrepoids, sept fois plus loin de B que "
              "l'objet, équilibre un poids sept fois plus grand."),
          Q(s="En déduire la masse de l'objet (g = 9,81 m/s²).", h=H_C, g=num(35.68, 0.01, U_KG), att="m ≈ 35,68 kg",
            e="m = P / g = 350 / 9,81 ≈ <b>35,68 kg</b>. Avec g ≈ 10 m/s², on retrouve l'équivalence courante "
              "1 daN ≈ 1 kg (35 kg)."),
      ]),
    Q(titre="Chargeur sur pneus", minutes=12,
      intro="Le chargeur se compose d'un châssis 1 (poids P<sub>1</sub> de 25 000 daN en G<sub>1</sub>), d'un godet 2 "
            "rempli de matériaux (poids P<sub>2</sub> de 11 500 daN en G<sub>2</sub>) et d'un ensemble flèche 3 "
            "articulé avec les vérins (poids P<sub>3</sub> de 10 000 daN en G<sub>3</sub>). L'ensemble est à l'arrêt. "
            "Repère : x vers l'avant (à droite), y vers le haut ; le sens trigonométrique est positif.",
      fig=fig("e08-chargeur.jpg", "Chargeur sur pneus : roues B (arrière) et A (avant) ; poids P1 à 3 m derrière A, P3 à "
                                  "2,2 m devant A, P2 à 4,2 m devant A", 680),
      questions=[
          Q(s="Déterminer le moment résultant en A des trois poids P<sub>1</sub>, P<sub>2</sub>, P<sub>3</sub> "
              "(coordonnée sur z, avec son signe).", h="Valeur exacte. Respecte la convention de signe. " + UNITE,
            g=num(4700, 0.5, U_DANM, variants=[(47000, 5, U_NM)]), att="M<sub>A</sub> = +4 700 daN·m (47 000 N·m)",
            e="Seules comptent les distances horizontales à A, les poids étant verticaux : G<sub>1</sub> est à 3 m en "
              "arrière, G<sub>3</sub> à 2,2 m et G<sub>2</sub> à 2,2 + 2 = 4,2 m en avant. M<sub>A</sub> = +25 000 × 3 "
              "− 10 000 × 2,2 − 11 500 × 4,2 = 75 000 − 22 000 − 48 300 = <b>+4 700 daN·m</b>. Les hauteurs (1,8 m, "
              "3,3 m, 4 m) n'interviennent pas."),
          Q(s="Le chargeur risque-t-il de basculer vers l'avant ?", h="Commence ta réponse par « oui » ou « non ».", g=NO,
            att="Non",
            e="Le moment résultant est positif : il tend à faire tourner le chargeur autour de A dans le sens "
              "trigonométrique, donc à appuyer la roue arrière B sur le sol. Le châssis (75 000 daN·m) l'emporte sur la "
              "flèche et le godet (70 300 daN·m) : <b>pas de basculement</b>."),
          Q(s="À partir de quelle valeur de P<sub>2</sub> y a-t-il risque de basculement ?", h=H_U,
            g=num(12619.05, 1, U_DAN, variants=[(126190.5, 10, U_N)]), att="P<sub>2</sub> &gt; 12 619 daN",
            e="Le chargeur bascule dès que le moment résultant devient négatif : 75 000 − 22 000 − 4,2 × P<sub>2</sub> "
              "&lt; 0, soit P<sub>2</sub> &gt; 53 000 / 4,2 ≈ <b>12 619 daN</b>. Le godet ne peut donc recevoir qu'environ "
              "1 119 daN de plus."),
      ]),
    Q(titre="Écran d'affichage", minutes=18,
      intro="Un panneau d'informations à écran (3) de poids <b>P</b> (500 N) est fixé à un poteau (2) encastré dans le sol "
            "(1). La force <b>F</b> (1 000 N), contenue dans un plan parallèle à (O, x, y), schématise la résultante des "
            "actions du vent sur le panneau. Données : α = 60°, β = 30°, a = 6 m et b = 8 m ; A a pour coordonnées "
            "(a ; 0 ; b).",
      fig=fig("e09-ecran.jpg", "Panneau d'affichage au bout d'un bras horizontal porté par un poteau vertical de hauteur "
                               "b ; en A, le poids P vers le bas et la force du vent F, horizontale, à α de l'axe du bras "
                               "et β de la direction y", 520),
      questions=[
          VQ("Écrire le vecteur F dans le repère (O, x, y, z), coordonnées arrondies au centième.",
             "F est horizontale (F<sub>z</sub> = 0) et fait α = 60° avec l'axe du bras, dirigé de A vers le poteau, "
             "c'est-à-dire vers les x négatifs ; elle fait β = 30° avec y. F<sub>x</sub> = −F cos α = −1 000 × cos 60° = "
             "<b>−500 N</b> ; F<sub>y</sub> = F cos β = 1 000 × cos 30° ≈ <b>866,03 N</b>.",
             VI(VEC("F"), [cn("x", -500), cn("y", 866.03), cn("z", 0, 0.001)], "N"), h=H_VEC + " Attention au signe."),
          VQ("Écrire le vecteur poids P dans le repère (O, x, y, z).",
             "Le poids est vertical, vers le bas : <b>P = (0 ; 0 ; −500) N</b>.",
             VI(VEC("P"), [cn("x", 0, 0.001), cn("y", 0, 0.001), cn("z", -500)], "N"), h=H_VEC + " Attention au signe."),
          VQ("Écrire le vecteur moment au point O de la force F : M<sub>O</sub>(F) = OA ∧ F.",
             "OA = (6 ; 0 ; 8) m. Sur x : y<sub>A</sub>F<sub>z</sub> − z<sub>A</sub>F<sub>y</sub> = 0 × 0 − 8 × 866,03 ≈ "
             "<b>−6 928,20 N·m</b> ; sur y : z<sub>A</sub>F<sub>x</sub> − x<sub>A</sub>F<sub>z</sub> = 8 × (−500) − 6 × 0 = "
             "<b>−4 000 N·m</b> ; sur z : x<sub>A</sub>F<sub>y</sub> − y<sub>A</sub>F<sub>x</sub> = 6 × 866,03 − 0 × (−500) ≈ "
             "<b>5 196,15 N·m</b>. La composante sur z tord le poteau, les deux autres le fléchissent.",
             VI(VEC("M") + "<sub>O</sub>(" + VEC("F") + ")", [cn("x", -6928.20, 0.05), cn("y", -4000, 0.05),
                                                              cn("z", 5196.15, 0.05)], "N·m"),
             h=H_VEC + " Arrondir au centième, attention aux signes."),
          VQ("Écrire le vecteur moment au point O du poids P.",
             "M<sub>O</sub>(P) = OA ∧ P : sur x, 0 × (−500) − 8 × 0 = 0 ; sur y, 8 × 0 − 6 × (−500) = <b>3 000 N·m</b> ; "
             "sur z, 6 × 0 − 0 × 0 = 0. Le poids, en porte-à-faux de 6 m, fléchit le poteau autour de y.",
             VI(VEC("M") + "<sub>O</sub>(" + VEC("P") + ")", [cn("x", 0, 0.001), cn("y", 3000, 0.05), cn("z", 0, 0.001)],
                "N·m")),
      ]),
]

METHODE_COUPLES = """<h3>Calculer un moment ou un couple</h3>
<ol>
<li><b>Moment d'une force</b> par rapport à un point : M = F × d, où d est la distance du point à la droite d'action (le bras de levier). Si F fait l'angle α avec OA : M = OA × F × sin α.</li>
<li><b>Sens</b> : positif dans le sens trigonométrique, négatif dans le sens horaire.</li>
<li>Une force dont la droite d'action passe par le point a un <b>moment nul</b> en ce point. Un brin de courroie tangent à une poulie a pour bras de levier le rayon.</li>
<li><b>Équilibre</b> autour d'un axe : la somme des moments est nulle.</li>
<li><b>Basculement</b> : on calcule les moments autour de l'appui sur lequel le solide pivoterait et on regarde le signe du moment résultant.</li>
<li><b>Produit vectoriel</b> (3D) : M<sub>O</sub>(F) = OA ∧ F = (y<sub>A</sub>F<sub>z</sub> − z<sub>A</sub>F<sub>y</sub> ; z<sub>A</sub>F<sub>x</sub> − x<sub>A</sub>F<sub>z</sub> ; x<sub>A</sub>F<sub>y</sub> − y<sub>A</sub>F<sub>x</sub>).</li>
<li><b>Unités</b> : N × m = N·m ; N × mm = N·mm (1 N·m = 1 000 N·mm) ; 1 daN = 10 N.</li>
</ol>"""


# =====================================================================================================================
# EXERCICE 2.2 — TORSEURS : LES BASES (niveau 2) : exercices 10 à 14
# =====================================================================================================================
def T(nom):
    return "{<i>T</i><sub>" + nom + "</sub>}"


TORSEURS = [
    Q(titre="Agrafeuse automatique", minutes=14,
      intro="Dans une agrafeuse automatique, un levier tourne autour de l'axe situé en O. Sur ce levier, deux tiges "
            "exercent deux forces : <b>F</b>, de support incliné de 20° sur la verticale et de norme 22,7 N, appliquée "
            "en A ; <b>G</b>, de support horizontal et de norme 16 N, appliquée en B. Cotes en mm.",
      fig=fig("e10-agrafeuse.png", "Levier d'agrafeuse articulé en O ; A à 30 mm à droite de O ; B à 20 mm à droite et "
                                   "40 mm au-dessus de O ; F en A inclinée de 20° sur la verticale, G en B horizontale", 440),
      questions=[
          VQ("Écrire le vecteur F dans le repère (O, x, y, z), coordonnées arrondies au centième.",
             "F est inclinée de 20° sur la verticale, vers la gauche : F<sub>x</sub> = −22,7 × sin 20° ≈ <b>−7,76 N</b> ; "
             "F<sub>y</sub> = 22,7 × cos 20° ≈ <b>21,33 N</b> ; F<sub>z</sub> = 0. G = (16 ; 0 ; 0) N, horizontale vers la droite.",
             VI(VEC("F"), [cn("x", -7.76), cn("y", 21.33), cn("z", 0, 0.001)], "N"), h=H_VEC + " Attention au signe."),
          VQ("Écrire le vecteur moment au point O de la force F, en N·mm.",
             "OA = (30 ; 0 ; 0) mm. M<sub>O</sub>(F) = OA ∧ F : sur z, x<sub>A</sub>F<sub>y</sub> − y<sub>A</sub>F<sub>x</sub> = "
             "30 × 21,33 − 0 ≈ <b>639,93 N·mm</b> (0,64 N·m) ; les coordonnées sur x et y sont nulles, F et OA étant dans "
             "le plan (x, y).",
             VI(VEC("M") + "<sub>O</sub>(" + VEC("F") + ")", [cn("x", 0, 0.001), cn("y", 0, 0.001), cn("z", 639.93, 0.05)],
                "N·mm")),
          VQ("Écrire le vecteur moment au point O de la force G, en N·mm.",
             "OB = (20 ; 40 ; 0) mm. Sur z : x<sub>B</sub>G<sub>y</sub> − y<sub>B</sub>G<sub>x</sub> = 20 × 0 − 40 × 16 = "
             "<b>−640 N·mm</b>. Les deux moments s'équilibrent presque : le levier est en équilibre.",
             VI(VEC("M") + "<sub>O</sub>(" + VEC("G") + ")", [cn("x", 0, 0.001), cn("y", 0, 0.001), cn("z", -640, 0.05)],
                "N·mm"), h=H_VEC + " Attention au signe."),
          Q(type="torseur", s="Modéliser la force F par son torseur au point A.", h=H_TORSEUR.format(r="N", m="N·mm"),
            nom=T("F"), point="A", vals=[-7.76, 0, 21.33, 0, 0, 0], tol=[0.01, 0.001, 0.01, 0.001, 0.001, 0.001],
            e="Au point d'application, le moment d'une force est nul : la résultante porte les coordonnées de F, les "
              "trois coordonnées du moment valent 0."),
          Q(type="torseur", s="Modéliser la force G par son torseur au point B.", h=H_TORSEUR.format(r="N", m="N·mm"),
            nom=T("G"), point="B", vals=[16, 0, 0, 0, 0, 0], tol=0.001,
            e="G = (16 ; 0 ; 0) N, appliquée en B : moment nul en B."),
          Q(type="torseur", s="Écrire le torseur {T<sub>F</sub>} au point O.", h=H_TORSEUR.format(r="N", m="N·mm"),
            nom=T("F"), point="O", vals=[-7.76, 0, 21.33, 0, 0, 639.93], tol=[0.01, 0.001, 0.01, 0.001, 0.001, 0.05],
            e="En changeant de point de réduction, la résultante ne change pas ; le moment devient M<sub>O</sub>(F) = "
              "(0 ; 0 ; 639,93) N·mm."),
          Q(type="torseur", s="Écrire le torseur {T<sub>G</sub>} au point O.", h=H_TORSEUR.format(r="N", m="N·mm"),
            nom=T("G"), point="O", vals=[16, 0, 0, 0, 0, -640], tol=[0.001, 0.001, 0.001, 0.001, 0.001, 0.05],
            e="Résultante inchangée (16 ; 0 ; 0) N ; moment M<sub>O</sub>(G) = (0 ; 0 ; −640) N·mm."),
      ]),
    Q(titre="Roue à denture hélicoïdale", minutes=12,
      intro="Une roue dentée à denture hélicoïdale reçoit au point A, d'une autre roue dentée, une action dont les "
            "composantes sont F<sub>A</sub> (200 daN, charge axiale), F<sub>R</sub> (100 daN, charge radiale) et "
            "F<sub>T</sub> (400 daN, charge tangentielle). A est sur l'axe z à 100 mm de O ; B est sur l'axe y à 100 mm "
            "de O.",
      fig=fig("e11-roue.jpg", "Roue hélicoïdale de centre O sur un arbre d'axe y ; au sommet A de la roue, les "
                              "composantes FT (selon x), FA (selon −y) et FR (selon −z)", 460),
      questions=[
          Q(type="torseur", s="Écrire le torseur de cette action au point A.", h=H_TORSEUR.format(r="daN", m="daN·m"),
            nom="{<i>T</i>}", point="A", vals=[400, 0, -200, 0, -100, 0], tol=0.001,
            e="F<sub>T</sub> est tangente à la roue en A, parallèle à x et orientée vers les x positifs ; F<sub>A</sub> "
              "est axiale, orientée vers les y négatifs ; F<sub>R</sub> est radiale, dirigée vers le centre : vers les z "
              "négatifs. R = (400 ; −200 ; −100) daN, moment nul en A."),
          Q(type="torseur", s="Écrire ce torseur au point O.", h=H_TORSEUR.format(r="daN", m="daN·m"),
            nom="{<i>T</i>}", point="O", vals=[400, 20, -200, 40, -100, 0], tol=0.01,
            e="OA = (0 ; 0 ; 0,1) m. M<sub>O</sub> = OA ∧ R : sur x, 0 × (−100) − 0,1 × (−200) = 20 ; sur y, 0,1 × 400 − 0 "
              "× (−100) = 40 ; sur z, 0 × (−200) − 0 × 400 = 0. M<sub>O</sub> = (20 ; 40 ; 0) daN·m."),
          Q(type="torseur", s="Écrire ce torseur au point B.", h=H_TORSEUR.format(r="daN", m="daN·m"),
            nom="{<i>T</i>}", point="B", vals=[400, 30, -200, 40, -100, 40], tol=0.01,
            e="Transport du moment : M<sub>B</sub> = M<sub>O</sub> + BO ∧ R, avec BO = (0 ; −0,1 ; 0) m. BO ∧ R = "
              "(−0,1 × (−100) − 0 ; 0 − 0 ; 0 − (−0,1) × 400) = (10 ; 0 ; 40). M<sub>B</sub> = (30 ; 40 ; 40) daN·m. "
              "Même résultat directement avec BA = (0 ; −0,1 ; 0,1) m : M<sub>B</sub> = BA ∧ R."),
      ]),
    Q(titre="Transmission par courroies", minutes=16,
      intro="Une transmission se compose d'une poulie entraînée par trois courroies trapézoïdales. Le plan (O, y, z) est "
            "le plan de symétrie de l'ensemble et (O, x) l'axe de rotation (x vers toi). Le diamètre d'enroulement des "
            "courroies est de 400 mm. Chaque courroie supporte les tensions T (1 500 N, brin tendu) et t (300 N, brin "
            "mou). Les brins, inclinés de 10° sur y, quittent la poulie en A et en B (rayon OA perpendiculaire au brin).",
      fig=fig("e12-courroie.jpg", "Poulie réceptrice de diamètre 400 mm, centre O ; brin tendu 3T partant de A à droite et "
                                  "brin mou 3t partant de B à gauche, inclinés de 10° sur l'axe y ; z vers la gauche", 520),
      questions=[
          Q(type="torseur", s="Écrire les trois tensions T sous forme d'un même torseur agissant en A.",
            h=H_TORSEUR.format(r="N", m="N·m"), nom=T("3T"), point="A", vals=[0, 0, 4431.63, 0, 781.42, 0],
            tol=[0.001, 0.001, 0.02, 0.001, 0.02, 0.001],
            e="3T = 4 500 N, incliné de 10° sur y, vers le centre de la figure, donc vers les z positifs (z pointe à "
              "gauche) : Y = 4 500 cos 10° ≈ 4 431,63 N ; Z = 4 500 sin 10° ≈ 781,42 N. Moment nul en A."),
          Q(type="torseur", s="Écrire les trois tensions t sous forme d'un même torseur agissant en B.",
            h=H_TORSEUR.format(r="N", m="N·m"), nom=T("3t"), point="B", vals=[0, 0, 886.33, 0, -156.28, 0],
            tol=[0.001, 0.001, 0.02, 0.001, 0.02, 0.001],
            e="3t = 900 N, incliné de 10° sur y vers les z négatifs : Y = 900 cos 10° ≈ 886,33 N ; Z = −900 sin 10° ≈ "
              "−156,28 N."),
          Q(type="torseur", s="Écrire le torseur {T<sub>3T</sub>} au centre O de la liaison.",
            h=H_TORSEUR.format(r="N", m="N·m"), nom=T("3T"), point="O", vals=[0, 900, 4431.63, 0, 781.42, 0],
            tol=[0.001, 0.5, 0.02, 0.5, 0.02, 0.5],
            e="Le brin est tangent à la poulie : son bras de levier par rapport à O est le rayon, 0,2 m. Le moment est "
              "porté par l'axe x : L = 4 500 × 0,2 = 900 N·m, positif car 3T fait tourner la poulie dans le sens "
              "trigonométrique vu depuis x. Par le calcul : OA = (0 ; 34,73 ; −196,96) mm et OA ∧ 3T = (900 ; 0 ; 0) N·m."),
          Q(type="torseur", s="Écrire le torseur {T<sub>3t</sub>} au centre O de la liaison.",
            h=H_TORSEUR.format(r="N", m="N·m"), nom=T("3t"), point="O", vals=[0, -180, 886.33, 0, -156.28, 0],
            tol=[0.001, 0.5, 0.02, 0.5, 0.02, 0.5],
            e="L = −900 × 0,2 = −180 N·m : 3t, à gauche, fait tourner la poulie dans l'autre sens."),
          Q(type="torseur", s="En déduire le torseur résultant au point O.", h=H_TORSEUR.format(r="N", m="N·m"),
            nom="{<i>T</i>}", point="O", vals=[0, 720, 5317.96, 0, 625.13, 0], tol=[0.001, 0.5, 0.05, 0.5, 0.05, 0.5],
            e="Les deux torseurs sont réduits au même point : on additionne résultantes et moments. R = (0 ; 4 431,63 + "
              "886,33 ; 781,42 − 156,28) = (0 ; 5 317,96 ; 625,13) N ; M<sub>O</sub> = (900 − 180 ; 0 ; 0) = (720 ; 0 ; 0) "
              "N·m. Le couple de 720 N·m entraîne la poulie ; la résultante charge les paliers."),
      ]),
    Q(titre="Barre coudée encastrée", minutes=10,
      intro="Une barre coudée 2 est encastrée en O dans une paroi fixe 1. La force <b>F</b>, 1 000 N, appliquée en A, est "
            "parallèle au plan (O, x, y) ; sa direction est définie par α = 60° (avec −x) et β = 30° (avec y). Données : "
            "a = 1 000 mm, b = 600 mm et c = 400 mm : A a pour coordonnées (a ; b ; −c).",
      fig=fig("e13-barre.jpg", "Barre coudée encastrée en O : tronçon OC de longueur a selon x, CB de longueur b selon y, "
                               "BA de longueur c vers le bas ; F en A horizontale, à α de −x et β de y", 520),
      questions=[
          Q(type="torseur", s="Écrire le torseur de F au point A.", h=H_TORSEUR.format(r="N", m="N·m"), nom=T("F"),
            point="A", vals=[-500, 0, 866.03, 0, 0, 0], tol=[0.01, 0.001, 0.01, 0.001, 0.001, 0.001],
            e="F = (−F cos α ; F cos β ; 0) = (−500 ; 866,03 ; 0) N ; moment nul en A."),
          Q(type="torseur", s="Écrire le torseur de F au point O.", h=H_TORSEUR.format(r="N", m="N·m"), nom=T("F"),
            point="O", vals=[-500, 346.41, 866.03, 200, 0, 1166.03], tol=[0.01, 0.05, 0.01, 0.05, 0.001, 0.05],
            e="OA = (1 ; 0,6 ; −0,4) m. M<sub>O</sub> = OA ∧ F : sur x, 0,6 × 0 − (−0,4) × 866,03 ≈ 346,41 ; sur y, "
              "(−0,4) × (−500) − 1 × 0 = 200 ; sur z, 1 × 866,03 − 0,6 × (−500) ≈ 1 166,03. M<sub>O</sub> ≈ (346,41 ; "
              "200 ; 1 166,03) N·m : c'est ce que l'encastrement doit reprendre."),
      ]),
    Q(titre="Clé à cliquet", minutes=12,
      intro="La force <b>F</b> en A schématise l'action de la main de l'opérateur sur la clé à cliquet (2) au moment du "
            "desserrage de la vis 3. Le manche BA, de 200 mm, est horizontal, dans une direction u à 20° de l'axe y ; "
            "B est à 70 mm au-dessus de O. ‖F‖ = 170 N ; F est horizontale et perpendiculaire à u.",
      fig=fig("e14-cliquet.jpg", "Clé à cliquet : axe vertical en O, tête B à 70 mm au-dessus de O, manche BA de 200 mm "
                                 "selon u à 20° de y ; F en A perpendiculaire au manche", 560),
      questions=[
          VQ("Écrire le vecteur F dans le repère (O, x, y, z), coordonnées arrondies au centième.",
             "u = (sin 20° ; cos 20° ; 0). F est horizontale, perpendiculaire à u, et tire le manche vers les x négatifs "
             "et les y positifs : F = 170 × (−cos 20° ; sin 20° ; 0). F<sub>x</sub> = −170 × cos 20° ≈ <b>−159,75 N</b> ; "
             "F<sub>y</sub> = 170 × sin 20° ≈ <b>58,14 N</b> ; F<sub>z</sub> = 0. Vérification : F · u = −159,75 × 0,342 + "
             "58,14 × 0,940 ≈ 0, F est bien perpendiculaire au manche.",
             VI(VEC("F"), [cn("x", -159.75), cn("y", 58.14), cn("z", 0, 0.001)], "N"), h=H_VEC + " Attention au signe."),
          Q(type="torseur", s="Écrire le torseur de F au point A.", h=H_TORSEUR.format(r="N", m="N·m"), nom=T("F"),
            point="A", vals=[-159.75, 0, 58.14, 0, 0, 0], tol=[0.01, 0.001, 0.01, 0.001, 0.001, 0.001],
            e="Résultante F = (−159,75 ; 58,14 ; 0) N, moment nul en A."),
          Q(type="torseur", s="Écrire le torseur de F au point O.", h=H_TORSEUR.format(r="N", m="N·m"), nom=T("F"),
            point="O", vals=[-159.75, -4.07, 58.14, -11.18, 0, 34], tol=[0.01, 0.01, 0.01, 0.01, 0.001, 0.01],
            e="A = B + 200 u = (200 sin 20° ; 200 cos 20° ; 70) ≈ (68,40 ; 187,94 ; 70) mm. M<sub>O</sub> = OA ∧ F : sur x, "
              "187,94 × 0 − 70 × 58,14 ≈ −4 070 N·mm ; sur y, 70 × (−159,75) − 68,40 × 0 ≈ −11 182 N·mm ; sur z, "
              "68,40 × 58,14 − 187,94 × (−159,75) = 34 000 N·mm. M<sub>O</sub> ≈ (−4,07 ; −11,18 ; 34) N·m. La "
              "composante sur z, 170 × 0,2 = 34 N·m, est le couple de desserrage de la vis ; les deux autres fléchissent "
              "la tige."),
      ]),
]

METHODE_TORSEURS = """<h3>Écrire et transporter un torseur</h3>
<ol>
<li><b>Torseur d'une force</b> F appliquée en A, réduit en A : {T}<sub>A</sub> = {X 0 ; Y 0 ; Z 0}<sub>A</sub>. La résultante porte les coordonnées de F ; le moment est nul au point d'application.</li>
<li><b>Changer de point de réduction</b> : la résultante ne change pas ; le moment devient M<sub>B</sub> = BA ∧ F (plus généralement M<sub>B</sub> = M<sub>A</sub> + BA ∧ R).</li>
<li><b>Produit vectoriel</b> : U ∧ V = (U<sub>y</sub>V<sub>z</sub> − U<sub>z</sub>V<sub>y</sub> ; U<sub>z</sub>V<sub>x</sub> − U<sub>x</sub>V<sub>z</sub> ; U<sub>x</sub>V<sub>y</sub> − U<sub>y</sub>V<sub>x</sub>).</li>
<li><b>Plusieurs actions</b> : réduis chaque torseur au même point, puis additionne résultantes et moments.</li>
<li><b>Lecture</b> : le moment autour de l'axe de rotation est le couple transmis ; les autres composantes chargent les appuis.</li>
<li><b>Unités</b> : résultante en N (ou daN), moment en N·m (ou N·mm, daN·m) ; garde les longueurs en m pour obtenir des N·m.</li>
</ol>"""

TORSEUR_CONSIGNE = ("<p><strong>Les torseurs s'écrivent en deux colonnes, dans six cases</strong> (X, Y, Z pour la "
                    "résultante ; L, M, N pour le moment), et se valident d'un bloc. Chaque case juste rapporte un demi-point ; les unités sont "
                    "données dans la consigne, inutile de les saisir.</p>")
CONSIGNE_UNITES = ("<p><strong>Les unités sont notées.</strong> Pour toute question numérique portant une unité, la valeur "
                   "vaut la moitié des points et l'unité l'autre moitié : une valeur juste écrite sans unité, ou avec une "
                   "unité fausse, ne rapporte qu'un demi-point.</p>")
CONSIGNE_LIT = ("<p><strong>Les expressions littérales</strong> s'écrivent avec les lettres de l'énoncé : par exemple "
                "<code>F*cos(α)</code>. Toute écriture équivalente est acceptée.</p>")


def construire():
    construire_exercice(
        titre="Projections d'une force", script="construire_exercices_sequence.py",
        sortie=SRC / "projections-source.html", parties=PROJECTIONS, nq_attendu=12,
        description="Coordonnées d'une force dans un repère : composantes, supports inclinés, changement de repère et "
                    "équilibre d'un gousset. Quatre parties à faire en mode entraînement ou en mode examen.",
        sous_titre="Quatre situations pour projeter une force sur les axes d'un repère : une dent d'engrenage, quatre "
                   "supports inclinés, un changement de repère et un gousset de barres soudées.",
        methode_titre="projeter une force", methode=METHODE_PROJECTIONS, consignes=(CONSIGNE_UNITES, CONSIGNE_COLONNE, CONSIGNE_LIT),
        hero=Q(f=IMG + "e03-support.jpg", alt="Support fixé sur un plan incliné ; force F de 200 N à 40° de l'axe x, "
                                              "repères R et R'",
               cap="La même force n'a pas les mêmes coordonnées dans R et dans R' : c'est l'objet de la partie 3."),
        facts=[("4 parties", "12 questions, dont 7 vecteurs en colonne"), ("52 min", "durée conseillée, qui fixe la pondération"),
               ("1 document", "méthode, en mode entraînement"), ("0 tracé", "toutes les réponses se saisissent au clavier")])
    construire_exercice(
        titre="Couples et moments", script="construire_exercices_sequence.py",
        sortie=SRC / "couples-moments-source.html", parties=COUPLES, nq_attendu=17,
        description="Couples et moments sur cinq systèmes réels : engrenage, poulie et courroie, balance romaine, chargeur "
                    "sur pneus et écran d'affichage (produit vectoriel).",
        sous_titre="Cinq systèmes réels pour calculer des couples et des moments : engrenage, poulie et courroie, balance "
                   "romaine, chargeur sur pneus et écran d'affichage, jusqu'au produit vectoriel.",
        methode_titre="moment et couple", methode=METHODE_COUPLES, consignes=(CONSIGNE_UNITES, CONSIGNE_COLONNE, CONSIGNE_LIT),
        hero=Q(f=IMG + "e08-chargeur.jpg", alt="Chargeur sur pneus avec les poids du châssis, de la flèche et du godet",
               cap="Le chargeur sur pneus : bascule-t-il vers l'avant ? (partie 4)"),
        facts=[("5 parties", "17 questions, dont 6 vecteurs en colonne"), ("58 min", "durée conseillée, qui fixe la pondération"),
               ("1 document", "méthode, en mode entraînement"), ("0 tracé", "toutes les réponses se saisissent au clavier")])
    construire_exercice(
        titre="Torseurs : les bases", script="construire_exercices_sequence.py",
        sortie=SRC / "torseurs-source.html", parties=TORSEURS, nq_attendu=20,
        description="Écrire le torseur d'une action mécanique en un point et le transporter : agrafeuse, roue hélicoïdale, "
                    "transmission par courroies, barre coudée et clé à cliquet.",
        sous_titre="Cinq systèmes pour écrire le torseur d'une action mécanique en un point, puis le transporter en un "
                   "autre point : agrafeuse, roue hélicoïdale, courroies, barre coudée et clé à cliquet.",
        methode_titre="torseur d'une action", methode=METHODE_TORSEURS, consignes=(CONSIGNE_UNITES, CONSIGNE_COLONNE, TORSEUR_CONSIGNE),
        cartouche="20 questions notées, dont 16 torseurs et 4 vecteurs saisis case par case, réparties en 5 parties pondérées par leur "
                  "durée conseillée.",
        hero=Q(f=IMG + "e14-cliquet.jpg", alt="Clé à cliquet : manche BA de 200 mm, force F perpendiculaire au manche",
               cap="La clé à cliquet : quel couple de desserrage, et quels efforts parasites ? (partie 5)"),
        facts=[("5 parties", "20 questions, dont 16 torseurs"), ("1 h 04", "durée conseillée, qui fixe la pondération"),
               ("1 document", "méthode, en mode entraînement"), ("0 tracé", "toutes les réponses se saisissent au clavier")])


if __name__ == "__main__":
    construire()
