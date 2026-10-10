"""
Gestionnaire de jeux — CRUD et persistance.
Gère l'ajout, la modification, la suppression et le chargement des jeux
depuis un fichier JSON local.
"""
import json
import shutil
import uuid
from pathlib import Path
from typing import Optional

from .config import GAMES_FILE, COVERS_DIR


def _ensure_covers_dir():
    """Crée le dossier des covers s'il n'existe pas."""
    COVERS_DIR.mkdir(parents=True, exist_ok=True)


def _load_raw() -> list[dict]:
    """Charge la liste brute des jeux depuis le fichier JSON."""
    if not GAMES_FILE.exists():
        return []
    try:
        with open(GAMES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []


def _save_raw(games: list[dict]):
    """Sauvegarde la liste des jeux dans le fichier JSON."""
    GAMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)


# ─── Opérations publiques ──────────────────────────────────────────────────


def load_games() -> list[dict]:
    """
    Charge et retourne la liste de tous les jeux enregistrés.
    Chaque jeu est un dictionnaire contenant:
      - id: identifiant unique
      - name: nom du jeu
      - exe_path: chemin vers l'exécutable
      - cover_path: chemin vers l'image de couverture (ou chaîne vide)
      - last_played: timestamp de la dernière session (ou None)
    """
    return _load_raw()


def add_game(name: str, exe_path: str, cover_path: str = "") -> dict:
    """
    Ajoute un nouveau jeu à la bibliothèque.

    Args:
        name: Nom affiché du jeu.
        exe_path: Chemin absolu vers l'exécutable.
        cover_path: Chemin vers une image de couverture (optionnel).

    Returns:
        Le dictionnaire du jeu nouvellement créé.
    """
    _ensure_covers_dir()

    game_id = str(uuid.uuid4())[:8]

    # Si une couverture est fournie, on la copie dans le dossier covers
    saved_cover = ""
    if cover_path and Path(cover_path).exists():
        ext = Path(cover_path).suffix.lower()
        if not ext:
            ext = ".png"
        dest = COVERS_DIR / f"{game_id}{ext}"
        shutil.copy2(cover_path, dest)
        saved_cover = str(dest)

    game = {
        "id": game_id,
        "name": name,
        "exe_path": exe_path,
        "cover_path": saved_cover,
        "last_played": None,
    }

    games = _load_raw()
    games.append(game)
    _save_raw(games)

    return game


def update_game(game_id: str, **kwargs) -> Optional[dict]:
    """
    Met à jour les informations d'un jeu existant.

    Args:
        game_id: Identifiant du jeu à modifier.
        **kwargs: Champs à mettre à jour (name, exe_path, cover_path).

    Returns:
        Le dictionnaire mis à jour, ou None si le jeu n'existe pas.
    """
    _ensure_covers_dir()
    games = _load_raw()

    for i, game in enumerate(games):
        if game["id"] == game_id:
            # Mise à jour du nom
            if "name" in kwargs:
                games[i]["name"] = kwargs["name"]

            # Mise à jour du chemin de l'exécutable
            if "exe_path" in kwargs:
                games[i]["exe_path"] = kwargs["exe_path"]

            # Mise à jour de la couverture
            if "cover_path" in kwargs and kwargs["cover_path"]:
                new_cover = kwargs["cover_path"]
                if Path(new_cover).exists():
                    ext = Path(new_cover).suffix.lower()
                    if not ext:
                        ext = ".png"
                    dest = COVERS_DIR / f"{game_id}{ext}"
                    # Supprimer l'ancienne couverture si différente
                    old_cover = games[i].get("cover_path", "")
                    if old_cover and Path(old_cover).exists() and Path(old_cover) != dest:
                        try:
                            Path(old_cover).unlink()
                        except OSError:
                            pass
                    shutil.copy2(new_cover, dest)
                    games[i]["cover_path"] = str(dest)

            _save_raw(games)
            return games[i]

    return None


def remove_game(game_id: str) -> bool:
    """
    Supprime un jeu de la bibliothèque.

    Args:
        game_id: Identifiant du jeu à supprimer.

    Returns:
        True si le jeu a été trouvé et supprimé, False sinon.
    """
    games = _load_raw()
    new_games = [g for g in games if g["id"] != game_id]

    if len(new_games) == len(games):
        return False  # Jeu non trouvé

    # Supprimer la couverture associée
    for game in games:
        if game["id"] == game_id:
            cover = game.get("cover_path", "")
            if cover and Path(cover).exists():
                try:
                    Path(cover).unlink()
                except OSError:
                    pass
            break

    _save_raw(new_games)
    return True


def record_play(game_id: str):
    """
    Enregistre l'horodatage de la dernière session de jeu.
    """
    from datetime import datetime
    games = _load_raw()
    for i, game in enumerate(games):
        if game["id"] == game_id:
            games[i]["last_played"] = datetime.now().isoformat()
            break
    _save_raw(games)


def get_game(game_id: str) -> Optional[dict]:
    """Retourne les données d'un jeu spécifique par son ID."""
    for game in _load_raw():
        if game["id"] == game_id:
            return game
    return None
