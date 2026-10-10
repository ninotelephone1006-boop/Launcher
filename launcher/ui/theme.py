"""
Thème et constantes visuelles du launcher.
Centralise toutes les couleurs, polices et paramètres de style
pour un design cohérent et maintenable.
"""
from ..config import (
    COLORS,
    FONTS,
    # Ré-exportés depuis config : source unique de vérité pour la grille.
    GAME_GRID_PADDING,
    GAME_GRID_SPACING,
)

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

SIDEBAR_WIDTH = 260
SIDEBAR_PADDING = 16
SIDEBAR_BUTTON_HEIGHT = 44
SIDEBAR_BUTTON_RADIUS = 10

CARD_WIDTH = 220
CARD_HEIGHT = 310
CARD_COVER_HEIGHT = 280
CARD_RADIUS = 12
CARD_BORDER_WIDTH = 1

# GAME_GRID_PADDING / GAME_GRID_SPACING : voir launcher/config.py

# ─── Paramètres d'animation ────────────────────────────────────────────────

HOVER_ANIM_MS = 150
FADE_ANIM_MS = 200
