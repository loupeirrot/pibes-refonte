#!/usr/bin/env python3
"""Fabrique les images web depuis medias/originaux/ (ARCHITECTURE.md §10).

  python3 optimiser.py

- WebP en 480, 960 et 1600 px de large, qualité 78, nommés <nom>-<largeur>.webp,
  écrits dans statique/assets/img/. Une image n'est jamais agrandie : si l'original
  est plus étroit qu'une largeur, cette largeur est ignorée ; si l'original est
  compris entre 960 et 1600 px, une version à sa largeur d'origine est produite.
- Aucun fichier de plus de 300 Ko : la qualité baisse par pas de 4, jusqu'à 60 au plus bas ;
  au-delà, cette largeur n'est pas produite (le navigateur prend la largeur inférieure).
- Écrit aussi assets/img/partage.jpg (1200 × 630, JPEG) depuis medias/partage-source.jpg
  s'il existe, sinon depuis optima-atelier.jpg (recadrage centré).
- Ne supprime rien. Réécrit seulement les fichiers dont l'original est plus récent.
"""
import os
import sys
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ICI, "medias", "originaux")
SORTIE = os.path.join(ICI, "statique", "assets", "img")
LARGEURS = (480, 960, 1600)
QUALITE = 78
MAX_OCTETS = 300_000
IGNORES = {"sigle-pb.png"}  # le sigle est un SVG dans le site


QUALITE_MIN = 60


def enregistrer(img, chemin, fmt, qualite):
    """Écrit l'image sous 300 Ko en baissant la qualité jusqu'à 60.
    Si elle reste trop lourde, rien n'est écrit et la fonction renvoie None :
    la largeur est alors laissée de côté (images très détaillées)."""
    import io
    while True:
        tampon = io.BytesIO()
        if fmt == "WEBP":
            img.save(tampon, "WEBP", quality=qualite, method=6)
        else:
            img.save(tampon, "JPEG", quality=qualite, optimize=True, progressive=True)
        if tampon.tell() <= MAX_OCTETS:
            with open(chemin, "wb") as f:
                f.write(tampon.getvalue())
            return qualite
        if qualite <= QUALITE_MIN:
            return None
        qualite -= 4


def main():
    os.makedirs(SORTIE, exist_ok=True)
    faits = 0
    for nom in sorted(os.listdir(ORIG)):
        base, ext = os.path.splitext(nom)
        if ext.lower() not in (".jpg", ".jpeg", ".png") or nom in IGNORES:
            continue
        src = os.path.join(ORIG, nom)
        img = Image.open(src)
        largeur, hauteur = img.size
        img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") and "A" in img.getbands() else "RGB")
        if img.mode == "RGBA":
            fond = Image.new("RGB", img.size, (0, 0, 0))
            fond.paste(img, mask=img.split()[3])
            img = fond
        cibles = [w for w in LARGEURS if w <= largeur]
        if 960 < largeur < 1600:
            cibles.append(largeur)
        for w in sorted(set(cibles)):
            sortie = os.path.join(SORTIE, f"{base}-{w}.webp")
            if os.path.exists(sortie) and os.path.getmtime(sortie) >= os.path.getmtime(src):
                continue
            h = round(hauteur * w / largeur)
            redim = img if w == largeur else img.resize((w, h), Image.LANCZOS)
            q = enregistrer(redim, sortie, "WEBP", QUALITE)
            if q is None:
                print(f"{os.path.basename(sortie)} laissée de côté : plus de 300 Ko même en qualité {QUALITE_MIN}")
                continue
            print(f"{os.path.basename(sortie)} {w}x{h} {os.path.getsize(sortie)//1024} Ko (q{q})")
            faits += 1
    # image de partage
    source = os.path.join(ICI, "medias", "partage-source.jpg")
    if not os.path.exists(source):
        source = os.path.join(ORIG, "optima-atelier.jpg")
    if os.path.exists(source):
        im = Image.open(source).convert("RGB")
        w, h = im.size
        cible = 1200 / 630
        if w / h > cible:
            nw = round(h * cible)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = round(w / cible)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im = im.resize((1200, 630), Image.LANCZOS)
        sortie = os.path.join(SORTIE, "partage.jpg")
        q = enregistrer(im, sortie, "JPEG", 82)
        print(f"partage.jpg 1200x630 {os.path.getsize(sortie)//1024} Ko (q{q})")
    print(f"{faits} image(s) écrite(s)")


if __name__ == "__main__":
    sys.exit(main())
