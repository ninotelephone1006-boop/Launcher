"""
Thème et constantes visuelles du launcher.
Centralise toutes les couleurs, polices et paramètres de style
pour un design cohérent et maintenable.
"""
from ..config import (
    # Ré-exportés depuis config : source unique de vérité pour les dimensions
    # partagées entre l'interface et la logique (évite les écarts de définition).
    CARD_COVER_HEIGHT,
    CARD_HEIGHT,
    CARD_WIDTH,
    COLORS,
    FONTS,
    GAME_GRID_PADDING,
    GAME_GRID_SPACING,
    SIDEBAR_WIDTH,
)

__all__ = [
    # Ré-exports de config
    "CARD_COVER_HEIGHT",
    "CARD_HEIGHT",
    "CARD_WIDTH",
    "COLORS",
    "FONTS",
    "GAME_GRID_PADDING",
    "GAME_GRID_SPACING",
    "SIDEBAR_WIDTH",
    # Palette
    "BG_PRIMARY",
    "BG_SECONDARY",
    "BG_TERTIARY",
    "BG_CARD",
    "BG_HOVER",
    "BG_SIDEBAR",
    "ACCENT",
    "ACCENT_HOVER",
    "ACCENT_PRESSED",
    "TEXT_PRIMARY",
    "TEXT_SECONDARY",
    "TEXT_MUTED",
    "BORDER",
    "DANGER",
    "DANGER_HOVER",
    "SUCCESS",
    "OVERLAY",
    # Thème CustomTkinter
    "CTK_THEME",
    # Dimensions propres à l'interface
    "SIDEBAR_PADDING",
    "SIDEBAR_BUTTON_HEIGHT",
    "SIDEBAR_BUTTON_RADIUS",
    "CARD_RADIUS",
    "CARD_BORDER_WIDTH",
    "HOVER_ANIM_MS",
    "FADE_ANIM_MS",
]

# ─── Palette de couleurs (raccourcis pratiques) ────────────────────────────

BG_PRIMARY = COLORS["bg_primary"]
BG_SECONDARY = COLORS["bg_secondary"]
BG_TERTIARY = COLORS["bg_tertiary"]
BG_CARD = COLORS["bg_card"]
BG_HOVER = COLORS["bg_hover"]
BG_SIDEBAR = COLORS["bg_sidebar"]

ACCENT = COLORS["accent_primary"]
ACCENT_HOVER = COLORS["accent_hover"]
ACCENT_PRESSED = COLORS["accent_pressed"]

TEXT_PRIMARY = COLORS["text_primary"]
TEXT_SECONDARY = COLORS["text_secondary"]
TEXT_MUTED = COLORS["text_muted"]

BORDER = COLORS["border"]
DANGER = COLORS["danger"]
DANGER_HOVER = COLORS["danger_hover"]
SUCCESS = COLORS["success"]
OVERLAY = COLORS["overlay"]

# ─── Configuration CustomTkinter ────────────────────────────────────────────

CTK_THEME = {
    "background_colors": (BG_PRIMARY, BG_PRIMARY, BG_PRIMARY),
    "text_colors": (TEXT_PRIMARY, TEXT_PRIMARY, TEXT_PRIMARY),
}

# ─── Dimensions des composants ─────────────────────────────────────────────

# SIDEBAR_WIDTH vient de launcher/config.py (source unique de vérité).
SIDEBAR_PADDING = 16
SIDEBAR_BUTTON_HEIGHT = 44
SIDEBAR_BUTTON_RADIUS = 10

# CARD_WIDTH / CARD_HEIGHT / CARD_COVER_HEIGHT viennent de launcher/config.py.
CARD_RADIUS = 12
CARD_BORDER_WIDTH = 1

# ─── Paramètres d'animation ────────────────────────────────────────────────

HOVER_ANIM_MS = 150
FADE_ANIM_MS = 200
