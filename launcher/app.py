"""
Application principale du launcher.
Orchestre tous les composants : sidebar, grille de jeux, dialogues.
Gère le cycle de vie de l'application.
"""
import subprocess
import sys
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

from . import game_manager
from .ui import theme
from .ui.sidebar import Sidebar
from .ui.game_grid import GameGrid
from .ui.add_game_dialog import AddGameDialog
from .ui.edit_game_dialog import EditGameDialog
from .config import (
    APP_NAME, APP_VERSION,
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
)


class LauncherApp(ctk.CTk):
    """
    Fenêtre principale du launcher de jeux vidéo.
    Architecture : Sidebar (gauche) + GameGrid (centre-droit).
    """

    def __init__(self):
        super().__init__()

        # ── Configuration de la fenêtre principale ──────────────────────
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Thème sombre personnalisé
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Couleur de fond de la fenêtre
        self.configure(fg_color=theme.BG_PRIMARY)

        # Icône de la fenêtre (optionnel, ignoré si non disponible)
        try:
            if sys.platform == "win32":
                icon_path = Path(__file__).parent / "assets" / "icon.ico"
                if icon_path.exists():
                    self.iconbitmap(str(icon_path))
        except Exception:
            pass

        # ── Chargement des jeux ─────────────────────────────────────────
        self.games = game_manager.load_games()

        # ── Construction de l'interface ─────────────────────────────────
        self._build_layout()

        # ── État de l'application ───────────────────────────────────────
        self._current_view = "library"

    def _build_layout(self):
        """Construit la mise en page principale."""

        # Layout principal : 2 colonnes (sidebar + contenu)
        self.grid_columnconfigure(0, weight=0, minsize=theme.SIDEBAR_WIDTH)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar (colonne gauche) ────────────────────────────────────
        self.sidebar = Sidebar(
            self,
            on_add_game=self._open_add_dialog,
            on_view="library",
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # ── Zone de contenu principal (colonne droite) ──────────────────
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=theme.BG_PRIMARY,
            corner_radius=0,
            border_width=0,
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # ── Barre de titre du contenu ───────────────────────────────────
        self._build_header()

        # ── Grille de jeux ──────────────────────────────────────────────
        self._build_game_grid()

    def _build_header(self):
        """Construit la barre de titre/en-tête de la zone de contenu."""

        header = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=70)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(16, 0))
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        # Titre principal
        self.header_title = ctk.CTkLabel(
            header,
            text="📚  Ma Bibliothèque",
            font=("Segoe UI", 22, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        self.header_title.grid(row=0, column=0, sticky="w")

        # Compteur de jeux
        count_text = f"{len(self.games)} jeu{'x' if len(self.games) != 1 else ''}"
        self.header_count = ctk.CTkLabel(
            header,
            text=count_text,
            font=("Segoe UI", 13),
            text_color=theme.TEXT_SECONDARY,
            anchor="e",
        )
        self.header_count.grid(row=0, column=1, sticky="e", padx=(0, 8))

        # Barre de recherche
        self.search_entry = ctk.CTkEntry(
            header,
            placeholder_text="🔍  Rechercher un jeu...",
            font=("Segoe UI", 13),
            width=240,
            height=36,
            corner_radius=8,
            fg_color=theme.BG_TERTIARY,
            border_color=theme.BORDER,
            text_color=theme.TEXT_PRIMARY,
        )
        self.search_entry.grid(row=0, column=2, sticky="e")
        self.search_entry.bind("<KeyRelease>", self._on_search)

    def _build_game_grid(self):
        """Crée ou recrée la grille de jeux."""
        # Supprimer l'ancienne grille si elle existe
        if hasattr(self, 'game_grid') and self.game_grid:
            self.game_grid.destroy()

        self.game_grid = GameGrid(
            self.content_frame,
            games=self.games,
            on_play=self._on_game_action,
            on_edit=self._open_edit_dialog,
            on_remove=self._remove_game,
        )
        self.game_grid.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

    def _update_header(self):
        """Met à jour l'en-tête (titre, compteur)."""
        count = len(self.games)
        titles = {
            "library": "📚  Ma Bibliothèque",
            "recent": "🕐  Récemment joués",
            "favorites": "⭐  Favoris",
        }
        self.header_title.configure(text=titles.get(self._current_view, "📚  Ma Bibliothèque"))
        self.header_count.configure(
            text=f"{count} jeu{'x' if count != 1 else ''}"
        )

    # ─── Callbacks de navigation ───────────────────────────────────────────

    def _on_game_action(self, game: dict):
        """
        Gère les actions sur les jeux depuis la grille.
        Si _action == 'add', ouvre le dialogue d'ajout.
        Sinon, lance le jeu.
        """
        if game.get("_action") == "add":
            self._open_add_dialog()
            return

        self._launch_game(game)

    def _launch_game(self, game: dict):
        """
        Lance un jeu en démarrant son exécutable.
        Enregistre l'horodatage de la session.
        """
        exe_path = game.get("exe_path", "")
        if not exe_path or not Path(exe_path).exists():
            messagebox.showerror(
                "Erreur",
                f"L'exécutable est introuvable :\n{exe_path}\n\n"
                "Veuillez vérifier le chemin dans les paramètres du jeu."
            )
            return

        try:
            # Lancer le jeu en processus séparé
            subprocess.Popen(
                [exe_path],
                cwd=str(Path(exe_path).parent),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
            )

            # Enregistrer la session
            game_manager.record_play(game["id"])

            # Rafraîchir la liste
            self.games = game_manager.load_games()
            self.game_grid.refresh(self.games)

        except Exception as e:
            messagebox.showerror(
                "Erreur de lancement",
                f"Impossible de lancer le jeu :\n{str(e)}"
            )

    def _open_add_dialog(self):
        """Ouvre le dialogue d'ajout de jeu."""
        # Référence conservée sur l'application : la fenêtre reste en vie
        # jusqu'à sa fermeture explicite.
        self.add_dialog = AddGameDialog(
            self,
            on_confirm=self._handle_add_game,
        )

    def _handle_add_game(self, data: dict):
        """
        Traite les données du formulaire d'ajout.
        Crée le jeu et rafraîchit l'interface.
        """
        game = game_manager.add_game(
            name=data["name"],
            exe_path=data["exe_path"],
            cover_path=data.get("cover_path", ""),
        )

        # Mettre à jour la liste locale et l'interface
        self.games.append(game)
        self.game_grid.add_card(game)
        self._update_header()

    def _open_edit_dialog(self, game: dict):
        """Ouvre le dialogue d'édition pour un jeu."""
        self.edit_dialog = EditGameDialog(
            self,
            game=game,
            on_confirm=self._handle_edit_game,
        )

    def _handle_edit_game(self, data: dict):
        """
        Traite les données du formulaire d'édition.
        Met à jour le jeu et rafraîchit l'interface.
        """
        if data.get("_action") == "delete":
            # Supprimer le jeu
            self._remove_game_by_id(data["id"])
            return

        game_id = data["id"]
        kwargs = {}
        if "name" in data:
            kwargs["name"] = data["name"]
        if "exe_path" in data:
            kwargs["exe_path"] = data["exe_path"]
        if "cover_path" in data:
            kwargs["cover_path"] = data["cover_path"]

        updated = game_manager.update_game(game_id, **kwargs)
        if updated:
            # Mettre à jour la liste locale
            for i, g in enumerate(self.games):
                if g["id"] == game_id:
                    self.games[i] = updated
                    break
            self.game_grid.update_card(updated)
            self._update_header()

    def _remove_game(self, game: dict):
        """
        Demande confirmation puis supprime un jeu.
        Appelé depuis le bouton supprimer de la carte.
        """
        game_id = game.get("id", "")
        game_name = game.get("name", "ce jeu")

        confirm = messagebox.askyesno(
            "Supprimer le jeu",
            f"Êtes-vous sûr de vouloir supprimer « {game_name } » de votre bibliothèque ?\n\n"
            "Le jeu ne sera pas désinstallé de votre PC, il sera simplement retiré du launcher."
        )

        if confirm:
            self._remove_game_by_id(game_id)

    def _remove_game_by_id(self, game_id: str):
        """Supprime un jeu par son ID et met à jour l'interface."""
        if game_manager.remove_game(game_id):
            self.games = [g for g in self.games if g.get("id") != game_id]
            self.game_grid.remove_card(game_id)
            self._update_header()

    def _on_search(self, event=None):
        """Filtre les jeux en fonction du texte de recherche."""
        query = self.search_entry.get().strip().lower()

        if not query:
            # Afficher tous les jeux
            self.game_grid.refresh(self.games)
            return

        # Filtrer les jeux par nom
        filtered = [
            g for g in self.games
            if query in g.get("name", "").lower()
        ]
        self.game_grid.refresh(filtered)
