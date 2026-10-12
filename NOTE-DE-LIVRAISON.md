# Note de livraison — séquence « Force, couple, torseur »

Sources : *Séquence : Modélisation des actions mécaniques* (10 pages) ; chapitres « Forces et actions mécaniques » et
« Moments et couples » d'un cours de mécanique (cours 1 et enrichissement du cours 3). Toutes les valeurs attendues ont été recalculées ;
les figures ont été lues sur un rendu à 300 dpi.

## Organisation retenue

| Carte | Niveau | Pages du PDF | Contenu |
|---|---|---|---|
| Cours 1 — Modélisation des actions mécaniques | 1 | chapitre « Forces » | vecteur-force, composantes, poids, actions de contact, pression |
| Cours 2 — Projection d'une force | 1 | 1 et 2 | rappels : coordonnées, norme, trigonométrie, projection |
| Exercice 1.2 — Projections d'une force | 1 | 4 | exercices 1 à 4 |
| Cours 3 — Moments et couples | 1 | 5 et 6 + chapitre « Moments et couples » | moment, Varignon, vecteur-moment, moment / axe, couple |
| Exercice 2.1 — Couples et moments | 2 | 7 et 8 | exercices 5 à 9 |
| Cours 4 — Torseur d'action mécanique | 2 | 9 | torseur, point de réduction |
| Exercice 2.2 — Torseurs : les bases | 2 | 9 et 10 | exercices 10 à 14 |

- **Niveau du cours 3** : non précisé dans la demande ; placé en **niveau 1**, car il contient les bases du moment
  utilisées par l'exercice 1.1 ; sa partie « produit vectoriel » prépare le niveau 2.
- **QCM de la page 3** : non repris (la demande vise les pages 1-2 pour le cours) ; il pourrait compléter le quiz du cours 2.
- **Numérotation** : chaque exercice du PDF devient une partie de la carte. Exercice 1.2 : parties 1 à 4 = exercices 1 à 4 ;
  exercice 2.1 : parties 1 à 5 = exercices 5 à 9 ; exercice 2.2 : parties 1 à 5 = exercices 10 à 14.

## Erreurs corrigées dans le document source

- **Page 5** : « la norme du moment par rapport au point **B** » → point **O** (la clé serre l'écrou en O).
- **Exercice 4, Q4.2** : « T3y = 100 daN » → T3 tire vers le bas, donc **T3y = −100 daN** ; l'intensité T3 = 200 daN.
- **Exercice 3** : le repère R'(x', y') dessiné est indirect (x' vers le haut à gauche, y' vers le haut à droite) ; il est
  gardé tel quel, les coordonnées étant calculées par projection sur chaque axe.

## Précisions ajoutées aux énoncés (lues sur les figures)

- **Exercices 9 et 13** : α est mesuré depuis l'axe −x (bras orienté vers le poteau, ou vers O) et β depuis y : F = (−500 ; 866,03 ; 0) N.
- **Exercice 10** : A (30 ; 0) mm et B (20 ; 40) mm d'après les cotes ; F est inclinée de 20° sur la verticale, vers la gauche.
- **Exercice 11** : A sur z à 100 mm, B sur y à 100 mm ; F<sub>T</sub> selon +x, F<sub>A</sub> selon −y, F<sub>R</sub> selon −z.
- **Exercice 12** : x vers l'observateur, z vers la gauche ; A et B sont les points où les brins quittent la poulie
  (angles droits de la figure), les brins convergent vers la poulie motrice.
- **Exercice 14** : « F est perpendiculaire à u » → **« F est horizontale et perpendiculaire à u »** ; sans cette précision
  deux directions sont possibles. La figure montre une force horizontale tirant vers −x et +y.
- **Exercice 6** : repère ajouté (x vers la droite, y vers le haut, z vers l'élève) pour écrire les coordonnées des moments.
- **Exercice 8** : x vers l'avant ; le moment est demandé avec son signe (sens trigonométrique positif).

## Décisions d'interprétation et de tolérance

- **Durées conseillées** (absentes du PDF), qui fixent la pondération : exercice 1.2 = 6 + 24 + 10 + 12 = 52 min ;
  exercice 2.1 = 8 + 10 + 10 + 12 + 18 = 58 min ; exercice 2.2 = 14 + 12 + 16 + 10 + 12 = 64 min.
- **Arrondi au centième** par défaut, tolérance ± 0,01 ; ± 0,05 quand le résultat se calcule à partir de valeurs déjà
  arrondies (produits vectoriels, moments de l'agrafeuse) ; à l'unité, ± 1 daN, pour la limite de basculement (12 619 daN).
- **Unités** : demi-point. Les autres unités cohérentes sont acceptées (N·mm, daN·m, N…) à condition d'être écrites ;
  « 12 N·m » ne vaut rien quand on attend 120 N·m ou 12 daN·m.
- **Exercice 5** : couples demandés en valeur absolue (0,47 N·m et 1,17 N·m) ; le sens est commenté dans la démarche.
- **Exercice 7** : g = 9,81 m/s² (absent du PDF) : P = 35 daN, m ≈ 35,68 kg.
- **Formules littérales** (exercice 2, Q7.1 de la balance) : nouveau correcteur `expr`, qui accepte toute écriture
  équivalente (« −F sin α », « −F cos(90° − α) », « F·sin(−α) »…) et refuse une valeur numérique isolée.
- **Torseurs** : saisis en six cases, un demi-point par case ; unités données dans la consigne : N et N·mm pour l'agrafeuse
  (cotes en mm), daN et daN·m pour la roue hélicoïdale, N et N·m ailleurs.

## Questions reformulées, découpées ou ajoutées

- Exercice 2 : Q2.1 (littéral) et Q2.2 (numérique) regroupées **par cas** : Fx et Fy littéraux, puis numériques (16 questions).
- Exercice 4 : Q4.1 → T1x et T1y ; Q4.2 → T3 et T3x.
- Exercice 6 : chaque question « norme et coordonnées » → deux questions ; couple disponible en valeur absolue.
- Exercice 7 : **question ajoutée** « poids P » entre la relation littérale (écrite P = …) et la masse.
- Exercice 8 : Q8.1 → moment résultant signé, puis « risque de basculement : oui ou non ».
- Exercice 9 : Q9.1 → Fx, Fy, Pz ; Q9.2 → trois coordonnées de M<sub>O</sub>(F) et la coordonnée non nulle de M<sub>O</sub>(P).
- Exercice 10 : Q10.1 → Fx et Fy (G = (16 ; 0 ; 0) N dans la démarche) ; moments demandés par leur coordonnée sur z.
- Exercice 12 : Q12.1 et Q12.2 → un torseur par groupe de brins.
- Exercice 14 : Q14.1 → Fx et Fy.

## Exercice 1.1 et saisie en colonne

- **Exercice 1.1 — Les quatre quadrants** (anciennement 1.3, passé en premier) : refait sur le modèle de l'exercice
  « Déplacer un torseur » du dépôt Statique. Page plein écran en trois colonnes (données et figure | réponse | correction
  pas à pas), séries de 5, 10, 15 ou 20 questions tirées parmi les situations cochées (angle mesuré depuis l'axe
  horizontal ou vertical, quadrants 1 à 4, répartition équilibrée), vecteur F écrit en colonne en fonction de F et α,
  puis en newtons. Une question n'est réussie que si les quatre cases sont justes à la première vérification ; la
  correction trace les projections sur la figure ; note sur 20 en fin de série. « Force, moment et couple » devient
  l'exercice 1.3.
- **Exercices 1.2, 1.3, 2.1 et 2.2** : les coordonnées d'un même vecteur, demandées jusque-là une par une, se
  saisissent désormais dans un vecteur en colonne (F, T<sub>1</sub>, P, F<sub>1</sub>, F<sub>2</sub>, R, moments M<sub>O</sub>
  et M<sub>A</sub>), et les torseurs en deux colonnes avec le nom de chaque case au-dessus. Dans un vecteur, l'unité est
  donnée à droite : chaque case juste vaut son point (l'unité n'y est plus notée). Les cas a à d de l'exercice 1.2
  donnent deux vecteurs côte à côte : l'expression littérale, puis les valeurs.

## Compléments apportés aux cours

- Les cadres à compléter du PDF (norme, rapports trigonométriques, projections, formule du couple, produit vectoriel,
  notation du torseur) deviennent des réponses « À toi » à dévoiler, des textes à trous ou des listes à choisir.
- Cours 3 : les quatre puces vides « Un couple se représente par un vecteur » sont complétées (point d'application,
  direction, sens par la règle du tire-bouchon, intensité) ; l'exemple de la roue hélicoïdale est résolu :
  M<sub>O</sub>(F) = (−200 ; −100 ; 0) N·m.
- Cours 4 : **ajout** de la formule de transport M<sub>B</sub> = M<sub>A</sub> + BA ∧ R et de l'addition de torseurs au
  même point, absentes de la page 9 mais nécessaires aux exercices 11 à 14 ; exemple du couple pur.
- Simulateurs, défis, exemples résolus et quiz (8, 8, 10 et 7 questions) sont rédigés pour ces cours.
- Cours 1 : les figures du chapitre (câble, ballon, bille, cylindre, cube, vérin) sont **redessinées en SVG** au lieu
  d'être reprises du scan ; les deux exemples de schématisation ont un bouton « Schématiser » qui fait apparaître
  le modèle (repère, droite d'action, vecteurs) sur le système réel.
- Cours 1 (nouveau) : vecteur-force et schématisation (câble, ballon), composantes (simulateur du parallélogramme),
  coordonnées, poids P = m g (Terre, Lune, Mars, altitude), deux jeux de classement (à distance / de contact ;
  concentrée / linéique / surfacique), charge linéique R = q L, pression R = p S et vérin (R = 7 854 daN à 100 bars
  pour d = 10 cm).
- Cours 3 (enrichi) : navette spatiale (translation seule ou translation + rotation), convention de signe, exemple
  F<sub>2</sub> = 200 N, clé à molette (20 sin α N·m), théorème de Varignon (M<sub>A</sub> = 88,6 N·m), vecteur-moment
  et règle des trois doigts, poutre encastrée (−283 N·m), moment par rapport à un axe (roue hélicoïdale :
  M<sub>u</sub> = −200 N·m), couple de deux forces (simulateur : M = F d quel que soit O), couples équivalents, clé à
  bougie (40 N·m dans les quatre positions), moment résultant. La balance romaine et le chargeur ne sont pas repris dans
  le cours : ce sont des questions de l'exercice 2.1.

## Points signalés sans modification

- Exercice 2, cas d : la figure n'est pas à l'échelle (F semble à 35° de x alors que α − β = 45°).
- Exercice 5 : F<sub>1/2</sub> = 20 N donne des couples très faibles (0,47 et 1,17 N·m) ; valeurs gardées.
- Exercice 8 : les hauteurs des centres de gravité (1,8 m, 3,3 m, 4 m) n'interviennent pas ; la démarche le signale.
