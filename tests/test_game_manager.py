"""
Tests de launcher/game_manager.py (CRUD + persistance JSON).

Les chemins de sauvegarde sont redirigés vers un dossier temporaire : aucun
test n'écrit dans le games.json réel de l'utilisateur.
"""
import json
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from launcher import game_manager


class GameManagerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        base = Path(self._tmp.name)

        self._saved_paths = (game_manager.GAMES_FILE, game_manager.COVERS_DIR)
        game_manager.GAMES_FILE = base / "games.json"
        game_manager.COVERS_DIR = base / "covers"

    def tearDown(self):
        game_manager.GAMES_FILE, game_manager.COVERS_DIR = self._saved_paths
        self._tmp.cleanup()

    def _make_image(self, name: str = "source.png", color=(10, 20, 30)) -> Path:
        path = Path(self._tmp.name) / name
        Image.new("RGB", (300, 400), color).save(path)
        return path

    # ─── Chargement ────────────────────────────────────────────────────

    def test_bibliotheque_vide_par_defaut(self):
        self.assertEqual(game_manager.load_games(), [])

    def test_json_corrompu_ne_plante_pas(self):
        game_manager.GAMES_FILE.write_text("{ ce n'est pas du json", encoding="utf-8")
        self.assertEqual(game_manager.load_games(), [])

    def test_json_non_liste_ne_plante_pas(self):
        game_manager.GAMES_FILE.write_text('{"jeu": 1}', encoding="utf-8")
        self.assertEqual(game_manager.load_games(), [])

    # ─── Ajout ─────────────────────────────────────────────────────────

    def test_add_game_persiste_le_jeu(self):
        game = game_manager.add_game(name="Witcher 3", exe_path="C:/Games/w3.exe")

        self.assertEqual(game["name"], "Witcher 3")
        self.assertEqual(game["exe_path"], "C:/Games/w3.exe")
        self.assertEqual(game["cover_path"], "")
        self.assertIsNone(game["last_played"])
        self.assertTrue(game_manager.GAMES_FILE.exists())
        self.assertEqual(len(game_manager.load_games()), 1)

    def test_ids_uniques(self):
        ids = {
            game_manager.add_game(name=f"Jeu {i}", exe_path="C:/a.exe")["id"]
            for i in range(5)
        }
        self.assertEqual(len(ids), 5)

    def test_add_game_copie_la_couverture(self):
        source = self._make_image()
        game = game_manager.add_game(
            name="Cyberpunk",
            exe_path="C:/Games/cp.exe",
            cover_path=str(source),
        )

        cover = Path(game["cover_path"])
        self.assertTrue(cover.exists())
        self.assertEqual(cover.parent, game_manager.COVERS_DIR)
        self.assertEqual(cover.stem, game["id"])

    def test_add_game_avec_couverture_absente(self):
        game = game_manager.add_game(
            name="Jeu",
            exe_path="C:/a.exe",
            cover_path="C:/introuvable/cover.png",
        )
        self.assertEqual(game["cover_path"], "")

    # ─── Mise à jour ───────────────────────────────────────────────────

    def test_update_game(self):
        game = game_manager.add_game(name="Avant", exe_path="C:/old.exe")
        updated = game_manager.update_game(game["id"], name="Après", exe_path="C:/new.exe")

        self.assertEqual(updated["name"], "Après")
        self.assertEqual(updated["exe_path"], "C:/new.exe")
        self.assertEqual(game_manager.get_game(game["id"])["name"], "Après")

    def test_update_game_inexistant(self):
        self.assertIsNone(game_manager.update_game("inconnu", name="x"))

    def test_update_game_remplace_la_couverture(self):
        first = self._make_image("a.png")
        game = game_manager.add_game(name="Jeu", exe_path="C:/a.exe", cover_path=str(first))
        old_cover = Path(game["cover_path"])

        second = self._make_image("b.jpg", color=(200, 100, 50))
        updated = game_manager.update_game(game["id"], cover_path=str(second))

        self.assertFalse(old_cover.exists(), "l'ancienne couverture doit être supprimée")
        self.assertTrue(Path(updated["cover_path"]).exists())

    # ─── Session / suppression ─────────────────────────────────────────

    def test_record_play_horodate_la_session(self):
        game = game_manager.add_game(name="Jeu", exe_path="C:/a.exe")
        game_manager.record_play(game["id"])

        last_played = game_manager.get_game(game["id"])["last_played"]
        self.assertIsNotNone(last_played)
        datetime.fromisoformat(last_played)  # doit être un timestamp ISO valide

    def test_record_play_jeu_inexistant_sans_erreur(self):
        game_manager.record_play("inconnu")
        self.assertEqual(game_manager.load_games(), [])

    def test_remove_game(self):
        source = self._make_image()
        game = game_manager.add_game(name="Jeu", exe_path="C:/a.exe", cover_path=str(source))
        cover = Path(game["cover_path"])

        self.assertTrue(game_manager.remove_game(game["id"]))
        self.assertEqual(game_manager.load_games(), [])
        self.assertFalse(cover.exists(), "la couverture doit être supprimée")
        self.assertFalse(game_manager.remove_game(game["id"]))

    def test_remove_game_conserve_les_autres(self):
        keep = game_manager.add_game(name="Gardé", exe_path="C:/a.exe")
        drop = game_manager.add_game(name="Supprimé", exe_path="C:/b.exe")

        game_manager.remove_game(drop["id"])

        self.assertEqual([g["id"] for g in game_manager.load_games()], [keep["id"]])

    def test_get_game(self):
        game = game_manager.add_game(name="Jeu", exe_path="C:/a.exe")
        self.assertEqual(game_manager.get_game(game["id"])["name"], "Jeu")
        self.assertIsNone(game_manager.get_game("inconnu"))

    def test_fichier_sauvegarde_en_utf8_lisible(self):
        game_manager.add_game(name="Élodie — été", exe_path="C:/a.exe")
        raw = game_manager.GAMES_FILE.read_text(encoding="utf-8")
        self.assertIn("Élodie — été", raw)
        self.assertEqual(json.loads(raw)[0]["name"], "Élodie — été")


if __name__ == "__main__":
    unittest.main()
