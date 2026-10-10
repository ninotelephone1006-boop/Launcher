"""
Point d'entrée principal du launcher NiLauncher.
Lance l'application GUI et démarre la boucle d'événements.
"""
import sys
import os

# S'assurer que le répertoire du script est dans le path
# (nécessaire pour le fonctionnement avec PyInstaller)
if getattr(sys, 'frozen', False):
    # Mode packagé (.exe)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Mode développement
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajouter le répertoire de base au path Python
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def main():
    """Fonction principale : initialise et lance le launcher."""

    # Importer l'application (après la configuration du path)
    from launcher.app import LauncherApp

    # Créer et lancer l'application
    app = LauncherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
