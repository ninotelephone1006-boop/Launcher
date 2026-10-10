"""
Boîte de dialogue d'ajout de jeu.
Permet de sélectionner un exécutable, nommer le jeu et choisir une couverture.
"""
from tkinter import filedialog
from pathlib import Path

import customtkinter as ctk

from . import theme
from ..config import ACCEPTED_EXECUTABLES, ACCEPTED_IMAGES


class AddGameDialog(ctk.CTkToplevel):
    """
    Fenêtre de dialogue modale pour ajouter un nouveau jeu à la bibliothèque.
    """

    def __init__(self, parent, on_confirm=None):
        """
        Initialise le dialogue d'ajout.

        Args:
            parent: Widget parent (fenêtre principale).
            on_confirm: Callback appelé avec les données du jeu après validation.
        """
        super().__init__(parent)

        self.on_confirm = on_confirm
        self.result = None

        # Chemins sélectionnés
        self._exe_path = ""
        self._cover_path = ""

        # ── Configuration de la fenêtre ─────────────────────────────────
        self.title("Ajouter un jeu")
        self.geometry("520x580")
        self.resizable(False, False)
        self.configure(fg_color=theme.BG_SECONDARY)

        # Rester au-dessus du parent
        self.transient(parent)
        self.grab_set()

        # Centrer par rapport au parent
        self.after(10, self._center_on_parent)

        self._build_ui()

    def _center_on_parent(self):
        """Centre le dialogue par rapport à la fenêtre parente."""
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
        """Construit l'interface du dialogue."""

        # ── Titre ───────────────────────────────────────────────────────
        title = ctk.CTkLabel(
            self,
            text="Ajouter un jeu",
            font=("Segoe UI", 22, "bold"),
            text_color=theme.TEXT_PRIMARY,
        )
        title.pack(pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Sélectionnez l'exécutable de votre jeu",
            font=("Segoe UI", 13),
            text_color=theme.TEXT_SECONDARY,
        )
        subtitle.pack(pady=(0, 20))

        # ── Zone de contenu avec padding ────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32, pady=0)

        # ── Champ : Nom du jeu ──────────────────────────────────────────
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
            placeholder_text="Ex: The Witcher 3",
            font=("Segoe UI", 13),
            height=40,
            corner_radius=8,
            fg_color=theme.BG_TERTIARY,
            border_color=theme.BORDER,
            text_color=theme.TEXT_PRIMARY,
        )
        self.name_entry.pack(fill="x", pady=(0, 16))

        # ── Champ : Exécutable ──────────────────────────────────────────
        exe_label = ctk.CTkLabel(
            content,
            text="Fichier exécutable (.exe)",
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

        # ── Champ : Image de couverture ─────────────────────────────────
        cover_label = ctk.CTkLabel(
            content,
            text="Image de couverture (optionnel)",
            font=("Segoe UI", 12, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        cover_label.pack(fill="x", pady=(0, 6))

        cover_row = ctk.CTkFrame(content, fg_color="transparent")
        cover_row.pack(fill="x", pady=(0, 8))

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

        self.btn_browse_cover = ctk.CTkButton(
            cover_row,
            text="Parcourir",
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

        # Aperçu de la couverture
        self.cover_preview_frame = ctk.CTkFrame(
            content,
            fg_color=theme.BG_TERTIARY,
            corner_radius=8,
            height=120,
        )
        self.cover_preview_frame.pack(fill="x", pady=(0, 16))

        self.cover_preview_label = ctk.CTkLabel(
            self.cover_preview_frame,
            text="Aperçu de la couverture",
            font=("Segoe UI", 12),
            text_color=theme.TEXT_MUTED,
        )
        self.cover_preview_label.pack(expand=True)

        # ── Boutons d'action ────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(8, 24))

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
        self.btn_cancel.pack(side="left", expand=True, padx=(0, 8))

        self.btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Ajouter",
            font=("Segoe UI", 13, "bold"),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="white",
            height=40,
            corner_radius=10,
            command=self._confirm,
        )
        self.btn_confirm.pack(side="right", expand=True, padx=(8, 0))

    def _browse_exe(self):
        """Ouvre le sélecteur de fichier pour choisir un exécutable."""
        path = filedialog.askopenfilename(
            title="Sélectionner l'exécutable du jeu",
            filetypes=ACCEPTED_EXECUTABLES,
        )
        if path:
            self._exe_path = path
            self.exe_entry.delete(0, "end")
            self.exe_entry.insert(0, path)

            # Auto-remplir le nom si vide
            if not self.name_entry.get():
                name = Path(path).stem
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, name)

    def _browse_cover(self):
        """Ouvre le sélecteur de fichier pour choisir une image."""
        path = filedialog.askopenfilename(
            title="Sélectionner une image de couverture",
            filetypes=ACCEPTED_IMAGES,
        )
        if path:
            self._cover_path = path
            self.cover_entry.delete(0, "end")
            self.cover_entry.insert(0, path)
            self._update_cover_preview(path)

    def _update_cover_preview(self, path: str):
        """Met à jour l'aperçu de la couverture."""
        try:
            from PIL import Image
            img = Image.open(path)
            # Redimensionner pour l'aperçu
            img.thumbnail((200, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.cover_preview_label.configure(image=ctk_img, text="")
            self.cover_preview_label._ctk_image = ctk_img  # Garde une référence
        except Exception:
            self.cover_preview_label.configure(image=None, text="Impossible de charger l'aperçu")

    def _confirm(self):
        """Valide le formulaire et appelle le callback."""
        name = self.name_entry.get().strip()
        exe_path = self._exe_path or self.exe_entry.get().strip()

        # Validation
        if not name:
            self._show_error("Veuillez entrer un nom pour le jeu.")
            return

        if not exe_path or not Path(exe_path).exists():
            self._show_error("Veuillez sélectionner un fichier exécutable valide.")
            return

        # Construire les données du jeu
        self.result = {
            "name": name,
            "exe_path": exe_path,
            "cover_path": self._cover_path or self.cover_entry.get().strip(),
        }

        if self.on_confirm:
            self.on_confirm(self.result)

        self.destroy()

    def _cancel(self):
        """Annule et ferme le dialogue."""
        self.destroy()

    def _show_error(self, message: str):
        """Affiche un message d'erreur dans le dialogue."""
        error_label = ctk.CTkLabel(
            self,
            text=f"⚠  {message}",
            font=("Segoe UI", 12),
            text_color=theme.DANGER,
        )
        error_label.pack(pady=(0, 4))
        # Auto-suppression après 3 secondes
        self.after(3000, error_label.destroy)
