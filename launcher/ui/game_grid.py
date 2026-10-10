"""
Grille de jeux (Game Grid).
Affiche les cartes de jeux dans une grille scrollable et responsive.
"""
import customtkinter as ctk
from . import theme
from .game_card import GameCard
from ..config import CARD_WIDTH, GAME_GRID_PADDING, GAME_GRID_SPACING


class GameGrid(ctk.CTkScrollableFrame):
    """
    Grille scrollable affichant les cartes de jeux.
    S'adapte automatiquement à la largeur disponible.
    """

    def __init__(
        self,
        parent,
        games: list = None,
        on_play=None,
        on_edit=None,
        on_remove=None,
        **kwargs,
    ):
        """
        Initialise la grille de jeux.

        Args:
            parent: Widget parent.
            games: Liste des jeux à afficher.
            on_play: Callback pour lancer un jeu.
            on_edit: Callback pour éditer un jeu.
            on_remove: Callback pour supprimer un jeu.
        """
        super().__init__(
            parent,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            scrollbar_button_color=theme.BG_TERTIARY,
            scrollbar_button_hover_color=theme.BG_HOVER,
            **kwargs,
        )

        self.on_play = on_play
        self.on_edit = on_edit
        self.on_remove = on_remove
        self.cards: list[GameCard] = []
        self._games = games or []
        self._empty_state = None

        # Variables pour le layout en grille
        self._columns = 4
        self._rows_per_page = 3

        # Construire la grille
        self._build_grid()

        # Lier le redimensionnement pour un layout responsive
        self.bind("<Configure>", self._on_resize)

    def _clear_grid(self):
        """
        Détruit les cartes et l'état vide.

        Les deux sont gérés avec grid : utiliser pack pour l'un et grid pour
        l'autre dans le même conteneur provoque une TclError
        (« cannot use geometry manager grid ... already has slaves managed by pack »).
        """
        for card in self.cards:
            card.destroy()
        self.cards.clear()

        self._destroy_empty_state()

    def _destroy_empty_state(self):
        """Détruit le message « bibliothèque vide » s'il est affiché."""
        if self._empty_state is not None:
            if self._empty_state.winfo_exists():
                self._empty_state.destroy()
            self._empty_state = None

    def _build_grid(self):
        """Construit ou reconstruit la grille complète."""
        self._clear_grid()

        if not self._games:
            self._show_empty_state()
            return

        # Créer une carte pour chaque jeu
        for game in self._games:
            card = GameCard(
                self,
                game=game,
                on_play=self.on_play,
                on_edit=self.on_edit,
                on_remove=self.on_remove,
            )
            self.cards.append(card)

        # Appliquer le layout en grille
        self._arrange_grid()

    def _arrange_grid(self):
        """Dispose les cartes en grille responsive."""
        # Calculer le nombre de colonnes en fonction de la largeur
        available_width = self.winfo_width() or 800
        padding = GAME_GRID_PADDING * 2
        spacing = GAME_GRID_SPACING
        usable = available_width - padding
        cols = max(1, int((usable + spacing) / (CARD_WIDTH + spacing)))
        cols = min(cols, 6)  # Maximum 6 colonnes
        self._columns = cols

        for i, card in enumerate(self.cards):
            row = i // cols
            col = i % cols
            card.grid(
                row=row,
                column=col,
                padx=(GAME_GRID_SPACING // 2, GAME_GRID_SPACING // 2),
                pady=(GAME_GRID_SPACING // 2, GAME_GRID_SPACING // 2),
                sticky="nsew",
            )

        # Configurer les colonnes pour qu'elles s'étendent également
        for c in range(cols):
            self.grid_columnconfigure(c, weight=1, minsize=CARD_WIDTH)

    def _show_empty_state(self):
        """Affiche un message quand la bibliothèque est vide."""
        # Même gestionnaire de placement que les cartes (grid), sinon le retour
        # à une liste non vide lève une TclError.
        self.grid_columnconfigure(0, weight=1)
        self._empty_state = ctk.CTkFrame(self, fg_color="transparent")
        empty_frame = self._empty_state
        empty_frame.grid(row=0, column=0, sticky="nsew", pady=100)

        # Emoji
        emoji = ctk.CTkLabel(
            empty_frame,
            text="🎮",
            font=("Segoe UI Emoji", 64),
        )
        emoji.pack(pady=(0, 16))

        # Titre
        title = ctk.CTkLabel(
            empty_frame,
            text="Votre bibliothèque est vide",
            font=("Segoe UI", 20, "bold"),
            text_color=theme.TEXT_PRIMARY,
        )
        title.pack(pady=(0, 8))

        # Sous-titre
        subtitle = ctk.CTkLabel(
            empty_frame,
            text="Cliquez sur « Ajouter un jeu » pour commencer",
            font=("Segoe UI", 14),
            text_color=theme.TEXT_SECONDARY,
        )
        subtitle.pack(pady=(0, 24))

        # Bouton d'action
        btn = ctk.CTkButton(
            empty_frame,
            text="＋  Ajouter votre premier jeu",
            font=("Segoe UI", 14, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=44,
            corner_radius=12,
            command=lambda: (
                # Appeler on_play avec None pour déclencher l'ajout
                self.on_play({"_action": "add"})
                if self.on_play else None
            ),
        )
        btn.pack(pady=0)

    def _on_resize(self, event=None):
        """Recalcule le layout quand la fenêtre est redimensionnée."""
        if self.cards:
            self._arrange_grid()

    def refresh(self, games: list = None):
        """
        Rafraîchit la grille avec une nouvelle liste de jeux.

        Args:
            games: Nouvelle liste de jeux (remplace l'actuelle).
        """
        if games is not None:
            self._games = games
        self._build_grid()

    def add_card(self, game: dict):
        """Ajoute une carte pour un nouveau jeu sans tout reconstruire."""
        self._games.append(game)

        # Retirer le message « bibliothèque vide » s'il est affiché
        self._destroy_empty_state()

        card = GameCard(
            self,
            game=game,
            on_play=self.on_play,
            on_edit=self.on_edit,
            on_remove=self.on_remove,
        )
        self.cards.append(card)
        self._arrange_grid()

    def remove_card(self, game_id: str):
        """Supprime une carte par son ID."""
        for card in self.cards[:]:
            if card.game.get("id") == game_id:
                card.destroy()
                self.cards.remove(card)
                break

        self._games = [g for g in self._games if g.get("id") != game_id]

        if not self.cards:
            self._build_grid()  # Ré-afficher l'état vide
        else:
            self._arrange_grid()

    def update_card(self, game: dict):
        """Met à jour une carte existante."""
        game_id = game.get("id")
        for i, g in enumerate(self._games):
            if g.get("id") == game_id:
                self._games[i] = game
                break

        for card in self.cards:
            if card.game.get("id") == game_id:
                card.update_game(game)
                break
