"""
Boîte de dialogue d'édition de jeu.
Permet de modifier le nom, l'exécutable et la couverture d'un jeu existant.
"""
from tkinter import filedialog
from pathlib import Path

import customtkinter as ctk

from . import theme
from ..config import ACCEPTED_EXECUTABLES, ACCEPTED_IMAGES


class EditGameDialog(ctk.CTkToplevel):
    """
    Fenêtre de dialogue modale pour éditer un jeu existant.
    """

    def __init__(self, parent, game: dict, on_confirm=None):
        """
        Initialise le dialogue d'édition.

        Args:
            parent: Widget parent.
            game: Données actuelles du jeu.
            on_confirm: Callback avec les nouvelles données après validation.
        """
        super().__init__(parent)

        self.game = game
        self.on_confirm = on_confirm
        self.result = None

        # Chemins
        self._exe_path = game.get("exe_path", "")
        self._cover_path = ""  # Vide = pas de changement
        self._cover_changed = False

        # ── Configuration de la fenêtre ─────────────────────────────────
        self.title(f"Modifier — {game.get('name', 'Jeu')}")
        self.geometry("520x600")
        self.resizable(False, False)
        self.configure(fg_color=theme.BG_SECONDARY)

        self.transient(parent)
        self.grab_set()

        self.after(10, self._center_on_parent)
        self._build_ui()

    def _center_on_parent(self):
        """Centre le dialogue sur la fenêtre parente."""
        self.update_idletasks()
        pw = self.master.winfo_width()
        ph = self.master.winfo_height()
        px = self.master.winfo_x()
        py = self.master.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        """Construit l'interface du dialogue d'édition."""

        # ── Titre ───────────────────────────────────────────────────────
        title = ctk.CTkLabel(
            self,
            text="Modifier le jeu",
            font=("Segoe UI", 22, "bold"),
            text_color=theme.TEXT_PRIMARY,
        )
        title.pack(pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self,
            text=f"Modification de : {self.game.get('name', '')}",
            font=("Segoe UI", 13),
            text_color=theme.TEXT_SECONDARY,
        )
        subtitle.pack(pady=(0, 20))

        # ── Contenu ─────────────────────────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32, pady=0)

        # ── Nom du jeu ──────────────────────────────────────────────────
        name_label = ctk.CTkLabel(
            content,
            text="Nom du jeu",
            font=("Segoe UI", 12, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        name_label.pack(fill="x", pady=(0, 6))

        self.name_entry = ctk.CTkEntry(
            content,
            placeholder_text="Nom du jeu...",
            font=("Segoe UI", 13),
            height=40,
            corner_radius=8,
            fg_color=theme.BG_TERTIARY,
            border_color=theme.BORDER,
            text_color=theme.TEXT_PRIMARY,
        )
        self.name_entry.pack(fill="x", pady=(0, 16))
        self.name_entry.insert(0, self.game.get("name", ""))

        # ── Exécutable ──────────────────────────────────────────────────
        exe_label = ctk.CTkLabel(
            content,
            text="Fichier exécutable",
            font=("Segoe UI", 12, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        exe_label.pack(fill="x", pady=(0, 6))

        exe_row = ctk.CTkFrame(content, fg_color="transparent")
        exe_row.pack(fill="x", pady=(0, 16))

        self.exe_entry = ctk.CTkEntry(
            exe_row,
            placeholder_text="Chemin vers l'exécutable...",
            font=("Segoe UI", 12),
            height=38,
            corner_radius=8,
            fg_color=theme.BG_TERTIARY,
            border_color=theme.BORDER,
            text_color=theme.TEXT_SECONDARY,
        )
        self.exe_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.exe_entry.insert(0, self.game.get("exe_path", ""))

        self.btn_browse_exe = ctk.CTkButton(
            exe_row,
            text="Parcourir",
            font=("Segoe UI", 12, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            width=90,
            height=38,
            corner_radius=8,
            command=self._browse_exe,
        )
        self.btn_browse_exe.pack(side="right")

        # ── Image de couverture ─────────────────────────────────────────
        cover_label = ctk.CTkLabel(
            content,
            text="Image de couverture",
            font=("Segoe UI", 12, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        cover_label.pack(fill="x", pady=(0, 6))

        cover_row = ctk.CTkFrame(content, fg_color="transparent")
        cover_row.pack(fill="x", pady=(0, 8))

        cover_text = self.game.get("cover_path", "")
        display_text = Path(cover_text).name if cover_text else "Aucune image"

        self.cover_entry = ctk.CTkEntry(
            cover_row,
            placeholder_text="Aucune image sélectionnée",
            font=("Segoe UI", 12),
            height=38,
            corner_radius=8,
            fg_color=theme.BG_TERTIARY,
            border_color=theme.BORDER,
            text_color=theme.TEXT_SECONDARY,
        )
        self.cover_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.cover_entry.insert(0, display_text)

        self.btn_browse_cover = ctk.CTkButton(
            cover_row,
            text="Changer",
            font=("Segoe UI", 12, "bold"),
            fg_color=theme.BG_TERTIARY,
            hover_color=theme.BG_HOVER,
            text_color=theme.TEXT_PRIMARY,
            width=90,
            height=38,
            corner_radius=8,
            border_width=1,
            border_color=theme.BORDER,
            command=self._browse_cover,
        )
        self.btn_browse_cover.pack(side="right")

        # Aperçu
        self.cover_preview_frame = ctk.CTkFrame(
            content,
            fg_color=theme.BG_TERTIARY,
            corner_radius=8,
            height=120,
        )
        self.cover_preview_frame.pack(fill="x", pady=(0, 16))

        self.cover_preview_label = ctk.CTkLabel(
            self.cover_preview_frame,
            text="Aperçu",
            font=("Segoe UI", 12),
            text_color=theme.TEXT_MUTED,
        )
        self.cover_preview_label.pack(expand=True)

        # Charger l'aperçu actuel
        if cover_text and Path(cover_text).exists():
            self._update_cover_preview(cover_text)

        # ── Boutons d'action ────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(8, 24))

        # Bouton Supprimer
        self.btn_delete = ctk.CTkButton(
            btn_frame,
            text="🗑️ Supprimer",
            font=("Segoe UI", 13, "bold"),
            fg_color="transparent",
            hover_color=theme.DANGER,
            text_color=theme.DANGER,
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=theme.DANGER,
            command=self._delete,
        )
        self.btn_delete.pack(side="left")

        self.btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            font=("Segoe UI", 13, "bold"),
            fg_color=theme.BG_TERTIARY,
            hover_color=theme.BG_HOVER,
            text_color=theme.TEXT_PRIMARY,
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=theme.BORDER,
            command=self._cancel,
        )
        self.btn_cancel.pack(side="right", padx=(8, 0), expand=True)

        self.btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Sauvegarder",
            font=("Segoe UI", 13, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=40,
            corner_radius=10,
            command=self._confirm,
        )
        self.btn_confirm.pack(side="right", padx=(0, 8), expand=True)

    def _browse_exe(self):
        """Ouvre le sélecteur de fichier pour l'exécutable."""
        path = filedialog.askopenfilename(
            title="Sélectionner le nouvel exécutable",
            filetypes=ACCEPTED_EXECUTABLES,
        )
        if path:
            self._exe_path = path
            self.exe_entry.delete(0, "end")
            self.exe_entry.insert(0, path)

    def _browse_cover(self):
        """Ouvre le sélecteur de fichier pour la couverture."""
        path = filedialog.askopenfilename(
            title="Sélectionner une nouvelle couverture",
            filetypes=ACCEPTED_IMAGES,
        )
        if path:
            self._cover_path = path
            self._cover_changed = True
            self.cover_entry.delete(0, "end")
            self.cover_entry.insert(0, Path(path).name)
            self._update_cover_preview(path)

    def _update_cover_preview(self, path: str):
        """Met à jour l'aperçu de la couverture."""
        try:
            from PIL import Image
            img = Image.open(path)
            img.thumbnail((200, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.cover_preview_label.configure(image=ctk_img, text="")
            self.cover_preview_label._ctk_image = ctk_img
        except Exception:
            self.cover_preview_label.configure(image=None, text="Erreur de chargement")

    def _confirm(self):
        """Valide et applique les modifications."""
        name = self.name_entry.get().strip()
        exe_path = self._exe_path or self.exe_entry.get().strip()

        if not name:
            self._show_error("Le nom du jeu ne peut pas être vide.")
            return

        if not exe_path or not Path(exe_path).exists():
            self._show_error("Le fichier exécutable est introuvable.")
            return

        self.result = {
            "id": self.game["id"],
            "name": name,
            "exe_path": exe_path,
        }

        # Inclure la couverture uniquement si elle a changé
        if self._cover_changed and self._cover_path:
            self.result["cover_path"] = self._cover_path

        if self.on_confirm:
            self.on_confirm(self.result)

        self.destroy()

    def _delete(self):
        """Supprime le jeu après confirmation."""
        self.result = {"_action": "delete", "id": self.game["id"]}
        if self.on_confirm:
            self.on_confirm(self.result)
        self.destroy()

    def _cancel(self):
        """Annule et ferme le dialogue."""
        self.destroy()

    def _show_error(self, message: str):
        """Affiche un message d'erreur temporaire."""
        error_label = ctk.CTkLabel(
            self,
            text=f"⚠  {message}",
            font=("Segoe UI", 12),
            text_color=theme.DANGER,
        )
        error_label.pack(pady=(0, 4))
        self.after(3000, error_label.destroy)
