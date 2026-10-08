# Modélisation des actions mécaniques : cours et exercices interactifs

Dépôt créé en dupliquant le gabarit du dépôt « Chaîne fonctionnelle » (même charte, mêmes pastilles Niveau 1 / Niveau 2,
même accueil en cartes illustrées). Publié par GitHub Pages depuis `index.html`.

| Adresse | Contenu |
|---|---|
| `index.html` | accueil : Les cours, Le formulaire, Les exercices, Études de cas |
| `force-moment.html` | Exercice 1.1 (Niveau 1) — Force, moment et couple (repris du dépôt `force-moment`) |

Les autres cartes (cours 1 et 2, formulaire, exercice 2.1, étude de cas) sont légèrement transparentes et annoncées « En cours d'édition ».

## Régénérer les pages

```sh
python3 src/generer.py   # écrit index.html et force-moment.html
```

- `src/gabarit-exercice-interactif.html` : gabarit de référence (seul son bloc de style sert à l'accueil).
- `src/generer.py` : cartes de l'accueil (`EXERCICES` pour les contenus, `ENCOURS` pour les cartes en cours d'édition).
- `src/exercices/force-moment-source.html` : page de l'exercice telle que publiée dans `force-moment` ; le générateur la copie en `force-moment.html` en ajoutant un lien de retour vers l'accueil.
- `src/images/` : vignettes des cartes (480 × 270).

**Remplacer une carte « en cours d'édition »** : déposer la page dans `src/exercices/`, la vignette dans `src/images/`, ajouter l'entrée dans `EXERCICES` et retirer la ligne correspondante de `ENCOURS`.
