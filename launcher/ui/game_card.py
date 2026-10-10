"""
Carte de jeu (Game Card).
Composant visuel individuel représentant un jeu dans la bibliothèque.
Affiche la pochette, le titre et un bouton "Jouer".
"""
import os
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter
import customtkinter as ctk

from . import theme
from ..config import CARD_WIDTH, CARD_HEIGHT, CARD_COVER_HEIGHT, COVER_WIDTH, COVER_HEIGHT


def _create_default_cover() -> Image.Image:
    """
    Crée une image de couverture par défaut (dégradé violet avec manette).
    Utilisée quand aucun cover_path n'est défini.
    """
    img = Image.new("RGB", (COVER_WIDTH, COVER_HEIGHT), theme.BG_TERTIARY)
    # Dégradé subtil
    for y in range(COVER_HEIGHT):
        r = int(28 + (y / COVER_HEIGHT) * 15)
        g = int(33 + (y / COVER_HEIGHT) * 10)
        b = int(45 + (y / COVER_HEIGHT) * 20)
        for x in range(COVER_WIDTH):
            img.putpixel((x, y), (r, g, b))
    return img


class GameCard(ctk.CTkFrame):
    """
    Carte de jeu individuelle avec effet de survol animé.
    Affiche la pochette du jeu, son titre et un bouton "Jouer".
    """

    def __init__(
        self,
        parent,
        game: dict,
        on_play=None,
        on_edit=None,
        on_remove=None,
        **kwargs,
    ):
        """
        Initialise une carte de jeu.

        Args:
            parent: Widget parent.
            game: Dictionnaire contenant les données du jeu.
            on_play: Callback pour lancer le jeu.
            on_edit: Callback pour éditer le jeu.
            on_remove: Callback pour supprimer le jeu.
        """
        super().__init__(
            parent,
            fg_color=theme.BG_CARD,
            corner_radius=theme.CARD_RADIUS,
            border_width=theme.CARD_BORDER_WIDTH,
            border_color=theme.BORDER,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            **kwargs,
        )

        self.game = game
        self.on_play = on_play
        self.on_edit = on_edit
        self.on_remove = on_remove

        # État interne
        self._is_hovered = False
        self._cover_image = None
        self._ctk_image = None

        # Fixer la taille
        self.pack_propagate(False)
        self.grid_propagate(False)

        self._build_ui()
        self._bind_hover_events()

    def _build_ui(self):
        """Construit les éléments visuels de la carte."""

        # ── Zone de couverture ──────────────────────────────────────────
        self.cover_frame = ctk.CTkFrame(
            self,
            fg_color=theme.BG_TERTIARY,
            corner_radius=(theme.CARD_RADIUS, theme.CARD_RADIUS, 0, 0),
            width=CARD_WIDTH,
            height=CARD_COVER_HEIGHT,
        )
        self.cover_frame.pack(fill="x", padx=0, pady=0)
        self.cover_frame.pack_propagate(False)

        # Charger l'image de couverture
        self._load_cover()

        # ── Overlay gradient sur la couverture (effet de fondu en bas) ──
        self.overlay = ctk.CTkFrame(
            self.cover_frame,
            fg_color=theme.BG_CARD,
            corner_radius=0,
            height=60,
        )
        self.overlay.place(relx=0, rely=1.0, y=-60, relwidth=1.0, height=60)
        self.overlay.configure(fg_color=theme.BG_CARD)

        # ── Overlay au survol (boutons d'action) ────────────────────────
        self.hover_overlay = ctk.CTkFrame(
            self.cover_frame,
            fg_color=("#00000080", "#000000AA"),
            corner_radius=(theme.CARD_RADIUS, theme.CARD_RADIUS, 0, 0),
        )
        self.hover_overlay.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.hover_overlay.place_forget()  # Caché par défaut

        # Bouton Jouer (centré sur l'overlay)
        self.btn_play_overlay = ctk.CTkButton(
            self.hover_overlay,
            text="▶  JOUER",
            font=("Segoe UI", 14, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=42,
            corner_radius=10,
            border_width=0,
            command=self._handle_play,
        )
        self.btn_play_overlay.place(relx=0.5, rely=0.45, anchor="center")

        # Boutons édition/suppression (en bas de l'overlay)
        btn_frame = ctk.CTkFrame(self.hover_overlay, fg_color="transparent")
        btn_frame.place(relx=0.5, rely=0.75, anchor="center")

        self.btn_edit = ctk.CTkButton(
            btn_frame,
            text="✏️",
            font=("Segoe UI Emoji", 14),
            fg_color=theme.BG_TERTIARY,
            hover_color=theme.BG_HOVER,
            text_color=theme.TEXT_PRIMARY,
            width=36,
            height=32,
            corner_radius=8,
            border_width=0,
            command=self._handle_edit,
        )
        self.btn_edit.pack(side="left", padx=4)

        self.btn_remove = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            font=("Segoe UI Emoji", 14),
            fg_color=theme.BG_TERTIARY,
            hover_color=theme.DANGER,
            text_color=theme.TEXT_PRIMARY,
            width=36,
            height=32,
            corner_radius=8,
            border_width=0,
            command=self._handle_remove,
        )
        self.btn_remove.pack(side="left", padx=4)

        # ── Zone inférieure : Titre + bouton jouer ──────────────────────
        self.info_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=CARD_HEIGHT - CARD_COVER_HEIGHT,
        )
        self.info_frame.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.info_frame.pack_propagate(False)

        # Titre du jeu
        self.title_label = ctk.CTkLabel(
            self.info_frame,
            text=self.game.get("name", "Jeu inconnu"),
            font=("Segoe UI", 12, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
            wraplength=CARD_WIDTH - 24,
            justify="left",
        )
        self.title_label.pack(fill="x", padx=4, pady=(4, 0))

        # Bouton Jouer (en bas de la carte)
        self.btn_play = ctk.CTkButton(
            self.info_frame,
            text="▶  Jouer",
            font=("Segoe UI", 12, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=32,
            corner_radius=8,
            border_width=0,
            command=self._handle_play,
        )
        self.btn_play.pack(fill="x", padx=4, pady=(4, 4), side="bottom")

    def _load_cover(self):
        """Charge et affiche l'image de couverture du jeu."""
        cover_path = self.game.get("cover_path", "")

        try:
            if cover_path and Path(cover_path).exists():
                img = Image.open(cover_path)
            else:
                img = _create_default_cover()

            # Redimensionner pour remplir la zone de couverture
            img = img.resize(
                (COVER_WIDTH, COVER_HEIGHT),
                Image.Resampling.LANCZOS,
            )

            self._cover_image = img
            self._ctk_image = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(COVER_WIDTH, COVER_HEIGHT),
            )

            self.cover_label = ctk.CTkLabel(
                self.cover_frame,
                text="",
                image=self._ctk_image,
            )
            self.cover_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        except Exception as e:
            # En cas d'erreur, afficher la couverture par défaut
            img = _create_default_cover()
            self._cover_image = img
            self._ctk_image = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(COVER_WIDTH, COVER_HEIGHT),
            )
            self.cover_label = ctk.CTkLabel(
                self.cover_frame,
                text="",
                image=self._ctk_image,
            )
            self.cover_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    def _bind_hover_events(self):
        """Attache les événements de survol à la carte et ses enfants."""
        # Liste de tous les widgets qui doivent déclencher le survol
        widgets = [
            self, self.cover_frame, self.info_frame,
            self.title_label, self.btn_play,
        ]

        # Ajouter le cover_label s'il existe
        if hasattr(self, 'cover_label'):
            widgets.append(self.cover_label)

        for widget in widgets:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        """Effet de survol : afficher l'overlay avec les boutons d'action."""
        if self._is_hovered:
            return
        self._is_hovered = True

        # Changer la bordure de la carte
        self.configure(border_color=theme.ACCENT)

        # Afficher l'overlay
        self.hover_overlay.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # Légère mise en valeur du titre
        self.title_label.configure(text_color=theme.ACCENT_HOVER)

    def _on_leave(self, event=None):
        """Effet de sortie : masquer l'overlay."""
        self._is_hovered = False

        # Restaurer la bordure
        self.configure(border_color=theme.BORDER)

        # Masquer l'overlay
        self.hover_overlay.place_forget()

        # Restaurer la couleur du titre
        self.title_label.configure(text_color=theme.TEXT_PRIMARY)

    def _handle_play(self):
        """Appelle le callback de lancement du jeu."""
        if self.on_play:
            self.on_play(self.game)

    def _handle_edit(self):
        """Appelle le callback d'édition du jeu."""
        if self.on_edit:
            self.on_edit(self.game)

    def _handle_remove(self):
        """Appelle le callback de suppression du jeu."""
        if self.on_remove:
            self.on_remove(self.game)

    def update_game(self, game: dict):
        """Met à jour les données et l'affichage de la carte."""
        self.game = game
        self.title_label.configure(text=game.get("name", "Jeu inconnu"))
        self._load_cover()
