#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recadre les figures de la séquence « Force, couple, torseur » dans le rendu du PDF à 300 dpi.

    pdftoppm -r 300 -png sequence.pdf h          # pages h-01.png … h-10.png
    python3 outils/extraire_figures.py DOSSIER_DES_PAGES

Les coordonnées sont mesurées sur un rendu à 110 dpi (plus simple à lire) et converties à 300 dpi.
Sorties : src/images/sequence/originaux/*.png (recadrage brut) et src/images/sequence/*.{png,jpg} (optimisées).
"""
import pathlib
import sys

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "images" / "sequence"
K = 300 / 110
LARGEUR_MAX = 900

# nom : (page, x0, y0, x1, y1, format) ; « jpg » pour les illustrations en couleurs dégradées
FIGURES = {
    "e01-engrenage": (4, 72, 172, 362, 372, "jpg"),
    "e02-a": (4, 155, 482, 294, 674, "jpg"),
    "e02-b": (4, 309, 482, 461, 674, "jpg"),
    "e02-c": (4, 462, 482, 601, 674, "jpg"),
    "e02-d": (4, 603, 482, 750, 674, "jpg"),
    "e03-support": (4, 542, 702, 838, 938, "jpg"),
    "e04-gousset": (4, 72, 962, 363, 1193, "jpg"),
    "e05-engrenage": (7, 72, 177, 393, 383, "png"),
    "e06-poulie": (7, 572, 452, 853, 628, "jpg"),
    "e07-balance": (7, 187, 767, 718, 1008, "jpg"),
    "e08-chargeur": (8, 197, 292, 713, 588, "jpg"),
    "e09-ecran": (8, 72, 647, 403, 913, "jpg"),
    "e10-agrafeuse": (9, 512, 642, 843, 893, "png"),
    "e11-roue": (9, 517, 952, 843, 1188, "jpg"),
    "e12-courroie": (10, 527, 142, 858, 388, "jpg"),
    "e13-barre": (10, 77, 437, 423, 668, "jpg"),
    "e14-cliquet": (10, 492, 737, 843, 923, "jpg"),
    "c-moment": (5, 257, 592, 678, 773, "png"),
    "c-cle": (5, 467, 897, 828, 1033, "png"),
    "c-roue-helicoidale": (6, 72, 512, 313, 713, "jpg"),
}

# vignettes des cartes de l'accueil (480 × 270) : source (figure ci-dessus ou recadrage de page), marge
VIGNETTES = {
    "carte-cours-projection.jpg": ((2, 527, 487, 840, 640), 14),
    "carte-cours-couple-moment.jpg": ("c-cle", 10),
    "carte-cours-torseur.jpg": ("c-roue-helicoidale", 8),
    "carte-exercice-projections.jpg": ("e04-gousset", 8),
    "carte-exercice-couples-moments.jpg": ("e08-chargeur", 6),
    "carte-exercice-torseurs.jpg": ("e14-cliquet", 8),
}


def vignette(im, marge):
    """Image entière posée sur un fond blanc de 480 × 270, centrée."""
    W, H = 480, 270
    s = min((W - 2 * marge) / im.width, (H - 2 * marge) / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    fond = Image.new("RGB", (W, H), "white")
    fond.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    return fond


def blanchir(im):
    """Fond légèrement gris du scan ramené au blanc, sans toucher aux traits."""
    return im.point(lambda v: 255 if v > 236 else v)


def main(pages):
    pages = pathlib.Path(pages)
    (OUT / "originaux").mkdir(parents=True, exist_ok=True)
    total = 0
    for nom, (p, x0, y0, x1, y1, fmt) in FIGURES.items():
        im = Image.open(pages / f"h-{p:02d}.png").convert("RGB")
        c = im.crop(tuple(int(v * K) for v in (x0, y0, x1, y1)))
        c.save(OUT / "originaux" / f"{nom}.png")
        c = blanchir(c)
        if c.width > LARGEUR_MAX:
            c = c.resize((LARGEUR_MAX, round(c.height * LARGEUR_MAX / c.width)), Image.LANCZOS)
        if fmt == "jpg":
            dest = OUT / f"{nom}.jpg"
            c.save(dest, quality=80, optimize=True, progressive=True)
        else:
            dest = OUT / f"{nom}.png"
            ImageOps.posterize(c, 8).quantize(colors=48, method=Image.Quantize.MEDIANCUT,
                                              dither=Image.Dither.NONE).save(dest, optimize=True)
        total += dest.stat().st_size
        print(f"{dest.name:28} {c.width}×{c.height}  {dest.stat().st_size / 1024:.0f} Kio")
    print(f"total : {total / 1024:.0f} Kio")
    for nom, (src, marge) in VIGNETTES.items():
        if isinstance(src, tuple):
            p, x0, y0, x1, y1 = src
            im = blanchir(Image.open(pages / f"h-{p:02d}.png").convert("RGB").crop(tuple(int(v * K) for v in (x0, y0, x1, y1))))
        else:
            im = blanchir(Image.open(OUT / "originaux" / f"{src}.png").convert("RGB"))
        dest = ROOT / "src" / "images" / nom
        vignette(im, marge).save(dest, quality=82, optimize=True)
        print(f"{nom:36} {dest.stat().st_size / 1024:.0f} Kio")


if __name__ == "__main__":
    main(sys.argv[1])
