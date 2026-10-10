"""
Configuration globale du launcher.
Définit les chemins, constantes et paramètres de l'application.
"""
import sys
from pathlib import Path


def get_app_dir() -> Path:
    """
    Retourne le répertoire de l'application.
    Fonction aussi bien en mode développement qu'en mode packagé (.exe).
    """
    if getattr(sys, 'frozen', False):
        # Si packagé avec PyInstaller, les données sont à côté de l'exe
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


# Répertoire principal de l'application
APP_DIR = get_app_dir()

# Fichier de sauvegarde des jeux
GAMES_FILE = APP_DIR / "games.json"

# Dossier des assets
ASSETS_DIR = APP_DIR / "launcher" / "assets"

# Dossier pour stocker les images de couverture copiées
COVERS_DIR = APP_DIR / "covers"

# Nom de l'application
APP_NAME = "NiLauncher"
APP_VERSION = "1.0.0"

# Dimensions de la fenêtre principale
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 960
WINDOW_MIN_HEIGHT = 600

# Dimensions de la sidebar
SIDEBAR_WIDTH = 260

# Dimensions des cartes de jeux
CARD_WIDTH = 220
CARD_HEIGHT = 310
CARD_COVER_HEIGHT = 280

# Dimensions des images de couverture
COVER_WIDTH = 220
COVER_HEIGHT = 280

# Grille de jeux (marges et espacement entre les cartes)
GAME_GRID_PADDING = 20
GAME_GRID_SPACING = 20

# Couleurs du thème
COLORS = {
    "bg_primary": "#0d1117",        # Fond principal très sombre
    "bg_secondary": "#161b22",      # Fond secondaire (sidebar, cards)
    "bg_tertiary": "#21262d",       # Fond tertiaire (hover)
    "bg_card": "#1c2128",           # Fond des cartes
    "bg_hover": "#292e36",          # Fond au survol
    "bg_sidebar": "#0d1117",        # Fond de la sidebar
    "accent_primary": "#6366f1",    # Bleu-violet principal
    "accent_hover": "#818cf8",      # Bleu-violet au survol
    "accent_pressed": "#4f46e5",    # Bleu-violet pressé
    "text_primary": "#e6edf3",      # Texte principal
    "text_secondary": "#8b949e",    # Texte secondaire
    "text_muted": "#484f58",        # Texte atténué
    "border": "#30363d",            # Bordures
    "danger": "#f85149",            # Rouge pour suppression
    "danger_hover": "#ff6b6b",      # Rouge au survol
    "success": "#3fb950",           # Vert pour confirmation
    "overlay": "#000000",           # Couleur d'overlay
}

# Polices
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "subtitle": ("Segoe UI", 18, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 13),
    "body_bold": ("Segoe UI", 13, "bold"),
    "small": ("Segoe UI", 11),
    "button": ("Segoe UI", 13, "bold"),
    "card_title": ("Segoe UI", 12, "bold"),
}

# Durée des animations (ms)
ANIMATIONS = {
    "hover_duration": 150,
    "fade_duration": 200,
    "slide_duration": 300,
}

# Extensions de fichiers acceptées
ACCEPTED_EXECUTABLES = [
    ("Exécutables Windows", "*.exe"),
    ("Fichiers batch", "*.bat"),
    ("Raccourcis", "*.lnk"),
    ("Tous les fichiers", "*.*"),
]

# Extensions d'images acceptées
ACCEPTED_IMAGES = [
    ("Images", "*.png *.jpg *.jpeg *.bmp *.webp *.gif"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("Tous les fichiers", "*.*"),
]
