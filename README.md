# Modélisation des actions mécaniques : cours et exercices interactifs

Dépôt créé en dupliquant le gabarit du dépôt « Chaîne fonctionnelle » (même charte, mêmes pastilles Niveau 1 / Niveau 2,
même accueil en cartes illustrées). Publié par GitHub Pages depuis `index.html`. Chaque page est un fichier HTML
autonome, sans dépendance externe, utilisable hors ligne.

| Adresse | Contenu |
|---|---|
| `index.html` | accueil : Les cours, Le formulaire, Les exercices, Études de cas |
| `cours-projection.html` | Cours 1 (Niveau 1) — Projection d'une force : carte des disciplines, repère interactif, triangle, simulateur de projection, quiz |
| `cours-couple-moment.html` | Cours 2 (Niveau 1) — Couple et moment : texte à trous, cartes, simulateur de clé, produit vectoriel pas à pas, quiz |
| `cours-torseur.html` | Cours 3 (Niveau 2) — Torseur d'action mécanique : torseur à explorer, simulateur de transport du moment, exemple pas à pas, quiz |
| `force-moment.html` | Exercice 1.1 (Niveau 1) — Force, moment et couple : 9 parties, 39 questions, 1 h 20 |
| `exercice-projections.html` | Exercice 1.2 (Niveau 1) — Projections d'une force : 4 parties, 27 questions, 52 min |
| `exercice-couples-moments.html` | Exercice 2.1 (Niveau 2) — Couples et moments : 5 parties, 20 questions, 58 min |
| `exercice-torseurs.html` | Exercice 2.2 (Niveau 2) — Torseurs, les bases : 5 parties, 22 questions dont 16 torseurs, 1 h 04 |

Les cours et les exercices 1.2, 2.1 et 2.2 viennent de la séquence « Modélisation des actions mécaniques : force,
couple, torseur » (pages 1-2, 5-6 et 9 pour les cours ; exercices 1 à 4, 5 à 9 et 10 à 14). Corrections et
décisions : [`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md). Le formulaire et l'étude de cas restent « En cours d'édition ».

## Régénérer les pages

```sh
pdftoppm -r 300 -png sequence.pdf DOSSIER/h          # seulement si les figures changent
python3 outils/extraire_figures.py DOSSIER           # figures et vignettes (src/images/sequence/, src/images/carte-*.jpg)
python3 src/construire_force_moment.py               # gabarit + contenu -> src/exercices/force-moment-source.html
python3 src/construire_exercices_sequence.py         # -> src/exercices/{projections,couples-moments,torseurs}-source.html
python3 src/construire_cours.py                      # -> src/cours/{projection,couple-moment,torseur}-source.html
python3 src/generer.py                               # écrit index.html et publie toutes les pages
```

- `src/gabarit-exercice-interactif.html` : gabarit de référence, commun à tous les exercices (charte, modes, chronomètre,
  notation pondérée, impression). Son bloc de style d'origine ne change pas ; les extensions sont dans un second bloc
  `<style>` additif.
- `src/commun.py` : assemblage d'une page d'exercice sur le gabarit, questions simples et torseurs, unités, correcteurs.
- `src/construire_force_moment.py`, `src/construire_exercices_sequence.py` : contenu des exercices (parties, questions,
  correcteurs, démarches, méthode).
- `src/construire_cours.py`, `src/cours/cours.css`, `src/cours/cours.js` : cours interactifs (construction reprise des
  cours du dépôt RDM : sections numérotées, formules, réponses « À toi », simulateurs et défis, textes à trous, cartes à
  retourner, vérifications rapides, exemples pas à pas, quiz).
- `src/generer.py` : cartes de l'accueil (`EXERCICES` pour les contenus, `ENCOURS` pour les cartes en cours d'édition)
  et copie des pages avec lien de retour vers l'accueil.
- `src/images/` : vignettes des cartes (480 × 270) ; `src/images/force-moment/`, `src/images/sequence/` : figures.

### Ajouts au gabarit

- **Méthode réservée au mode entraînement** : tout élément portant la classe `training-only` (onglet du rail, onglet du
  panneau, puce « Méthode », bouton « Documents », section `doc` de la méthode) est masqué en mode examen, et le moteur
  refuse d'y ouvrir le document. Le mode examen ne donne accès à aucune méthode, avant comme après la remise.
- **Correcteur `expr`** (formules littérales) : la saisie (« Fx = −F × sin α », « P = q*a/b »…) est évaluée pour plusieurs
  jeux de valeurs et comparée à l'expression attendue ; toute écriture équivalente est acceptée, une valeur numérique
  isolée ne l'est pas.
- **Torseurs** : six cases X, Y, Z / L, M, N validées d'un bloc (mécanique « fast-q » du moteur), une coche par case.
- Durée conseillée du chronomètre déduite des parties ; bouton « Documents » ouvert sur le premier document disponible.

## Tester

```sh
node --test tests/correction.test.js                          # moteur de correction : réponses justes, fausses et limites
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, entraînement et examen de chaque exercice
```

`tests/reponses.js` déduit de la configuration une réponse juste par question : un sujet entièrement juste doit donner
20/20, en entraînement comme en examen, sans erreur JavaScript.
