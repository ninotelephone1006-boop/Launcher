"""
Barre latérale de navigation (sidebar).
Contient le logo, les boutons de navigation et le bouton d'ajout de jeu.
"""
import customtkinter as ctk
from . import theme


class Sidebar(ctk.CTkFrame):
    """
    Sidebar de navigation à gauche de l'application.
    Style sombre premium inspiré de Steam / Epic Games.
    """

    def __init__(self, parent, on_add_game, on_view="library", **kwargs):
        """
        Initialise la sidebar.

        Args:
            parent: Widget parent.
            on_add_game: Callback appelé quand l'utilisateur clique sur "Ajouter".
            on_view: Vue active initiale ("library" ou "recent").
        """
        super().__init__(
            parent,
            fg_color=theme.BG_SIDEBAR,
            corner_radius=0,
            border_width=0,
            width=theme.SIDEBAR_WIDTH,
            **kwargs,
        )

        self.on_add_game = on_add_game
        self.active_buttons = {}
        self._view = on_view

        # Empêcher le redimensionnement horizontal
        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build_ui()

    def _build_ui(self):
        """Construit tous les éléments de la sidebar."""

        # ── En-tête : Logo / Titre ──────────────────────────────────────
        header = ctk.CTkFrame(
            self, fg_color="transparent", height=70
        )
        header.pack(fill="x", padx=0, pady=(20, 10))
        header.pack_propagate(False)

        # Icône de manette (emoji)
        logo_label = ctk.CTkLabel(
            header,
            text="🎮",
            font=("Segoe UI Emoji", 28),
            text_color=theme.ACCENT,
        )
        logo_label.pack(side="left", padx=(20, 8), pady=10)

        # Nom de l'application
        title_label = ctk.CTkLabel(
            header,
            text="NiLauncher",
            font=("Segoe UI", 20, "bold"),
            text_color=theme.TEXT_PRIMARY,
        )
        title_label.pack(side="left", padx=0, pady=10)

        # ── Séparateur ──────────────────────────────────────────────────
        sep = ctk.CTkFrame(self, fg_color=theme.BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=(0, 15))

        # ── Section : Navigation ────────────────────────────────────────
        nav_label = ctk.CTkLabel(
            self,
            text="  BIBLIOTHÈQUE",
            font=("Segoe UI", 11, "bold"),
            text_color=theme.TEXT_MUTED,
            anchor="w",
        )
        nav_label.pack(fill="x", padx=24, pady=(10, 8))

        # Bouton Bibliothèque
        self.btn_library = self._create_nav_button(
            icon="📚",
            text="Ma Bibliothèque",
            command=lambda: self._on_nav("library"),
            active=(self._view == "library"),
        )

        # Bouton Récents
        self.btn_recent = self._create_nav_button(
            icon="🕐",
            text="Récemment joués",
            command=lambda: self._on_nav("recent"),
            active=(self._view == "recent"),
        )

        # Bouton Favoris
        self.btn_favorites = self._create_nav_button(
            icon="⭐",
            text="Favoris",
            command=lambda: self._on_nav("favorites"),
            active=(self._view == "favorites"),
        )

        # ── Espace flexible ─────────────────────────────────────────────
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # ── Séparateur bas ──────────────────────────────────────────────
        sep2 = ctk.CTkFrame(self, fg_color=theme.BORDER, height=1)
        sep2.pack(fill="x", padx=20, pady=(0, 15))

        # ── Bouton Ajouter un jeu (principal) ───────────────────────────
        self.btn_add = ctk.CTkButton(
            self,
            text="＋  Ajouter un jeu",
            font=("Segoe UI", 14, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=48,
            corner_radius=12,
            border_width=0,
            command=self.on_add_game,
        )
        self.btn_add.pack(fill="x", padx=20, pady=(0, 8))

        # ── Paramètres ──────────────────────────────────────────────────
        self.btn_settings = ctk.CTkButton(
            self,
            text="⚙  Paramètres",
            font=("Segoe UI", 13),
            fg_color="transparent",
            hover_color=theme.BG_TERTIARY,
            text_color=theme.TEXT_SECONDARY,
            height=40,
            corner_radius=10,
            border_width=0,
            anchor="w",
            command=lambda: self._on_nav("settings"),
        )
        self.btn_settings.pack(fill="x", padx=20, pady=(0, 20))

        # ── Version en bas ──────────────────────────────────────────────
        version_label = ctk.CTkLabel(
            self,
            text="v1.0.0",
            font=("Segoe UI", 10),
            text_color=theme.TEXT_MUTED,
        )
        version_label.pack(side="bottom", pady=(0, 10))

    def _create_nav_button(self, icon: str, text: str, command, active: bool = False):
        """
        Crée un bouton de navigation dans la sidebar.

        Args:
            icon: Emoji ou caractère pour l'icône.
            text: Texte du bouton.
            command: Callback au clic.
            active: Si True, le bouton est marqué comme actif.

        Returns:
            Le bouton créé.
        """
        if active:
            fg = theme.BG_TERTIARY
            tc = theme.TEXT_PRIMARY
        else:
            fg = "transparent"
            tc = theme.TEXT_SECONDARY

        btn = ctk.CTkButton(
            self,
            text=f"  {icon}  {text}",
            font=("Segoe UI", 13),
            fg_color=fg,
            hover_color=theme.BG_TERTIARY,
            text_color=tc,
            height=theme.SIDEBAR_BUTTON_HEIGHT,
            corner_radius=theme.SIDEBAR_BUTTON_RADIUS,
            border_width=0,
            anchor="w",
            command=command,
        )
        btn.pack(fill="x", padx=16, pady=2)
        return btn

    def _on_nav(self, view: str):
        """Met à jour la vue active visuellement."""
        self._view = view
        # Réinitialiser tous les boutons
        for btn in [self.btn_library, self.btn_recent, self.btn_favorites]:
            btn.configure(fg_color="transparent", text_color=theme.TEXT_SECONDARY)

        # Activer le bon bouton
        active_btn = {
            "library": self.btn_library,
            "recent": self.btn_recent,
            "favorites": self.btn_favorites,
        }.get(view)

        if active_btn:
            active_btn.configure(
                fg_color=theme.BG_TERTIARY,
                text_color=theme.TEXT_PRIMARY,
            )

    def set_view(self, view: str):
        """Change la vue active programmatiquement."""
        self._on_nav(view)
