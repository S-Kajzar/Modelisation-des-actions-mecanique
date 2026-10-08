# Modélisation des actions mécaniques : cours et exercices interactifs

Dépôt créé en dupliquant le gabarit du dépôt « Chaîne fonctionnelle » (même charte, mêmes pastilles Niveau 1 / Niveau 2,
même accueil en cartes illustrées). Publié par GitHub Pages depuis `index.html`.

| Adresse | Contenu |
|---|---|
| `index.html` | accueil : Les cours, Le formulaire, Les exercices, Études de cas |
| `force-moment.html` | Exercice 1.1 (Niveau 1) — Force, moment et couple, construit sur le gabarit (9 parties, 39 questions, 1 h 20) |

Les autres cartes (cours 1 et 2, formulaire, exercice 2.1, étude de cas) sont légèrement transparentes et annoncées « En cours d'édition ».

## Régénérer les pages

```sh
python3 src/construire_force_moment.py   # gabarit + contenu -> src/exercices/force-moment-source.html
python3 src/generer.py                   # écrit index.html et force-moment.html
```

- `src/gabarit-exercice-interactif.html` : gabarit de référence, commun à tous les exercices (charte, modes, chronomètre, notation pondérée, impression). Son bloc de style et ses moteurs ne se modifient pas ; les extensions sont dans un second bloc `<style>` additif.
- `src/construire_force_moment.py` : contenu de l'exercice (parties, questions, correcteurs, méthode) injecté dans le gabarit. Un nouvel exercice se construit de la même façon.
- `src/generer.py` : cartes de l'accueil (`EXERCICES` pour les contenus, `ENCOURS` pour les cartes en cours d'édition) et copie des pages d'exercices avec lien de retour vers l'accueil.
- `src/images/` : vignettes des cartes (480 × 270) ; `src/images/force-moment/` : figures de l'exercice.

### Méthode : réservée au mode entraînement

Tout élément portant la classe `training-only` (onglet du rail, onglet du panneau, puce « Méthode » d'une partie, bouton « Documents » du bandeau, section `doc` de la méthode) est masqué en **mode examen**, et le moteur refuse d'y ouvrir le document correspondant. Le mode examen ne donne donc accès à aucune méthode, avant comme après la remise de la copie.

**Remplacer une carte « en cours d'édition »** : déposer la page dans `src/exercices/`, la vignette dans `src/images/`, ajouter l'entrée dans `EXERCICES` et retirer la ligne correspondante de `ENCOURS`.
