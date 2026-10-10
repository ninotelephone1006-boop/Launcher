"""
Génération et chargement des images de couverture.

Ce module n'utilise que Pillow (aucune dépendance à Tk / CustomTkinter) :
la logique d'image est donc testable sans affichage graphique.
"""
from PIL import Image

from .config import COVER_HEIGHT, COVER_WIDTH

# Dégradé vertical de la couverture par défaut :
# couleur du haut, puis variation appliquée sur toute la hauteur.
_DEFAULT_COVER_BASE = (28, 33, 45)
_DEFAULT_COVER_RANGE = (15, 10, 20)


def create_default_cover(
    width: int = COVER_WIDTH,
    height: int = COVER_HEIGHT,
) -> Image.Image:
    """
    Crée la couverture par défaut (dégradé vertical sombre, bleu-violet).

    Un dégradé d'un pixel de large est étiré à la largeur demandée : cela évite
    de calculer les (width x height) pixels un par un, ce qui ralentissait
    nettement l'affichage d'une grande bibliothèque.

    Args:
        width: Largeur de l'image.
        height: Hauteur de l'image.

    Returns:
        Une image PIL au format RGB.
    """
    height = max(1, height)
    gradient = Image.new("RGB", (1, height))
    gradient.putdata([
        tuple(
            int(base + variation * (y / height))
            for base, variation in zip(_DEFAULT_COVER_BASE, _DEFAULT_COVER_RANGE)
        )
        for y in range(height)
    ])

    if width == 1:
        return gradient
    return gradient.resize((max(1, width), height), Image.Resampling.NEAREST)


def load_cover_image(
    cover_path: str = "",
    size: tuple = (COVER_WIDTH, COVER_HEIGHT),
) -> Image.Image:
    """
    Ouvre la couverture d'un jeu et la redimensionne aux dimensions d'affichage.

    Aucune exception ne remonte à l'interface : si le chemin est vide,
    introuvable ou illisible, la couverture par défaut est renvoyée.

    Args:
        cover_path: Chemin du fichier image (peut être vide).
        size: Taille cible (largeur, hauteur).

    Returns:
        Une image PIL prête à être affichée.
    """
    if cover_path:
        try:
            with Image.open(cover_path) as source:
                return source.resize(size, Image.Resampling.LANCZOS)
        except (OSError, ValueError, SyntaxError):
            # Fichier absent, verrouillé ou non reconnu par Pillow.
            pass

    return create_default_cover(*size)
