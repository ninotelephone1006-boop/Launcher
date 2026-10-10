"""
Tests de launcher/covers.py (génération et chargement des couvertures).

Ce module est volontairement indépendant de Tk / CustomTkinter : il est donc
testable sur n'importe quelle machine, sans affichage.
"""
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from launcher.config import COVER_HEIGHT, COVER_WIDTH
from launcher.covers import create_default_cover, load_cover_image


def legacy_default_cover(width: int = COVER_WIDTH, height: int = COVER_HEIGHT) -> Image.Image:
    """
    Implémentation historique (pixel par pixel), conservée ici comme référence :
    elle verrouille le rendu visuel de la couverture par défaut.
    """
    img = Image.new("RGB", (width, height), "#21262d")
    for y in range(height):
        r = int(28 + (y / height) * 15)
        g = int(33 + (y / height) * 10)
        b = int(45 + (y / height) * 20)
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    return img


class TestCreateDefaultCover(unittest.TestCase):
    def test_dimensions_et_mode(self):
        img = create_default_cover()
        self.assertEqual(img.size, (COVER_WIDTH, COVER_HEIGHT))
        self.assertEqual(img.mode, "RGB")

    def test_rendu_identique_a_l_ancienne_version(self):
        """La version rapide doit produire exactement la même image."""
        expected = legacy_default_cover()
        actual = create_default_cover()
        self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_rendu_identique_pour_des_tailles_personnalisees(self):
        for width, height in [(1, 5), (7, 9), (64, 32)]:
            expected = legacy_default_cover(width, height)
            actual = create_default_cover(width, height)
            self.assertEqual(
                actual.tobytes(),
                expected.tobytes(),
                f"différence de rendu pour {width}x{height}",
            )

    def test_degrade_uniforme_sur_une_ligne(self):
        img = create_default_cover(40, 20)
        first_row = {img.getpixel((x, 0)) for x in range(40)}
        self.assertEqual(len(first_row), 1, "la couleur doit être constante sur une ligne")

    def test_plus_rapide_que_l_ancienne_version(self):
        runs = 3
        start = time.perf_counter()
        for _ in range(runs):
            legacy_default_cover()
        legacy_time = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(runs):
            create_default_cover()
        new_time = time.perf_counter() - start

        self.assertLess(
            new_time,
            legacy_time / 5,
            "create_default_cover doit rester nettement plus rapide que la "
            "version pixel par pixel (une carte est générée à chaque affichage)",
        )


class TestLoadCoverImage(unittest.TestCase):
    def test_fichier_valide_redimensionne(self):
        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "cover.png"
            Image.new("RGB", (500, 700), "#ff0000").save(source)

            img = load_cover_image(str(source))

            self.assertEqual(img.size, (COVER_WIDTH, COVER_HEIGHT))
            self.assertEqual(img.getpixel((0, 0)), (255, 0, 0))

    def test_taille_personnalisee(self):
        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "cover.png"
            Image.new("RGB", (500, 700), "#00ff00").save(source)
            self.assertEqual(load_cover_image(str(source), size=(50, 60)).size, (50, 60))

    def test_chemin_vide_renvoie_la_couverture_par_defaut(self):
        img = load_cover_image("")
        self.assertEqual(img.tobytes(), create_default_cover().tobytes())

    def test_fichier_absent_renvoie_la_couverture_par_defaut(self):
        img = load_cover_image("C:/dossier/inexistant/jeu.png")
        self.assertEqual(img.size, (COVER_WIDTH, COVER_HEIGHT))
        self.assertEqual(img.tobytes(), create_default_cover().tobytes())

    def test_fichier_corrompu_renvoie_la_couverture_par_defaut(self):
        with TemporaryDirectory() as tmp:
            broken = Path(tmp) / "broken.png"
            broken.write_bytes(b"ceci n'est pas une image")
            img = load_cover_image(str(broken))
            self.assertEqual(img.tobytes(), create_default_cover().tobytes())


if __name__ == "__main__":
    unittest.main()
