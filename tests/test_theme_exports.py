"""
Vérifie que tous les noms importés depuis launcher.config et référencés via
launcher.ui.theme existent réellement.

C'est exactement le type d'erreur qui faisait plancher le launcher au démarrage
(ImportError: cannot import name 'GAME_GRID_PADDING'). Ce test ne nécessite
aucun affichage graphique.
"""
import ast
import unittest
from pathlib import Path

from launcher import config
from launcher.ui import theme

PACKAGE_DIR = Path(__file__).resolve().parent.parent / "launcher"


def _iter_module_sources():
    for path in sorted(PACKAGE_DIR.rglob("*.py")):
        yield path.relative_to(PACKAGE_DIR), path.read_text(encoding="utf-8")


def _config_imports():
    """Noms importés depuis config dans chaque module du paquet."""
    for relative, source in _iter_module_sources():
        tree = ast.parse(source, filename=str(relative))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            module = node.module or ""
            if module != "config" and not module.endswith(".config"):
                continue
            for alias in node.names:
                if alias.name != "*":
                    yield str(relative), node.lineno, alias.name


def _theme_attributes():
    """Attributs accédés via theme.X dans les modules d'interface."""
    for relative, source in _iter_module_sources():
        tree = ast.parse(source, filename=str(relative))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "theme"
            ):
                yield str(relative), node.lineno, node.attr


class TestNomsExportes(unittest.TestCase):
    def test_tous_les_imports_de_config_existent(self):
        manquants = [
            f"{module}:{ligne} -> config.{nom}"
            for module, ligne, nom in _config_imports()
            if not hasattr(config, nom)
        ]
        self.assertEqual(manquants, [], "noms absents de launcher/config.py")

    def test_tous_les_attributs_de_theme_existent(self):
        manquants = [
            f"{module}:{ligne} -> theme.{nom}"
            for module, ligne, nom in _theme_attributes()
            if not hasattr(theme, nom)
        ]
        self.assertEqual(manquants, [], "noms absents de launcher/ui/theme.py")

    def test_theme_expose_bien_les_dimensions_de_config(self):
        """Les dimensions partagées doivent venir de config (source unique)."""
        for nom in (
            "CARD_WIDTH",
            "CARD_HEIGHT",
            "CARD_COVER_HEIGHT",
            "SIDEBAR_WIDTH",
            "GAME_GRID_PADDING",
            "GAME_GRID_SPACING",
        ):
            self.assertEqual(
                getattr(theme, nom),
                getattr(config, nom),
                f"{nom} diverge entre theme.py et config.py",
            )

    def test_le_test_couvre_bien_le_code(self):
        """Garde-fou : le scan doit trouver des imports et des usages."""
        self.assertGreater(len(list(_config_imports())), 5)
        self.assertGreater(len(list(_theme_attributes())), 20)


if __name__ == "__main__":
    unittest.main()
