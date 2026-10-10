# 🎮 NiLauncher — Launcher de Jeux Vidéo

Un launcher de jeux vidéo **moderne**, **élégant** et **100 % fonctionnel** pour Windows, inspiré de Steam, Epic Games et GOG Galaxy.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🎨 **Design premium** | Interface sombre haut de gamme inspirée de Steam/Epic Games |
| 📚 **Bibliothèque** | Grille de cartes de jeux avec couvertures et effets de survol |
| ➕ **Ajout de jeux** | Sélection d'exécutables .exe avec auto-détection du nom |
| ✏️ **Édition** | Modification du nom, de l'exécutable et de la couverture |
| 🗑️ **Suppression** | Retrait de jeux de la bibliothèque (confirmation requise) |
| ▶️ **Lancement** | Un clic pour lancer le jeu directement |
| 🔍 **Recherche** | Barre de recherche pour filtrer les jeux en temps réel |
| 💾 **Sauvegarde** | Persistance automatique en JSON (games.json) |
| 🖼️ **Couvertures** | Images personnalisées ou couverture par défaut générée |
| 📂 **Portable** | Compilable en un seul fichier .exe autonome |

---

## 📁 Structure du Projet

```
Launcher/
├── main.py                      # Point d'entrée de l'application
├── requirements.txt             # Dépendances Python
├── build.bat                    # Script de build (dossier)
├── build_onefile.bat            # Script de build (fichier unique .exe)
├── launcher.spec                # Configuration PyInstaller
├── games.json                   # Sauvegarde des jeux (généré auto.)
├── covers/                      # Dossier des couvertures (généré auto.)
├── dist/                        # Dossier de sortie (généré par le build)
│   └── NiLauncher.exe           # Exécutable compilé
├── launcher/
│   ├── __init__.py
│   ├── app.py                   # Application principale (orchestration)
│   ├── config.py                # Configuration, chemins, constantes
│   ├── covers.py                # Couvertures : génération + chargement (Pillow)
│   ├── game_manager.py          # CRUD des jeux + persistance JSON
│   ├── assets/
│   │   └── icon.ico             # Icône de l'application (optionnel)
│   └── ui/
│       ├── __init__.py
│       ├── theme.py             # Thème, couleurs, polices, dimensions
│       ├── sidebar.py           # Barre latérale de navigation
│       ├── game_card.py         # Carte individuelle de jeu
│       ├── game_grid.py         # Grille scrollable de cartes
│       ├── add_game_dialog.py   # Dialogue d'ajout de jeu
│       └── edit_game_dialog.py  # Dialogue d'édition de jeu
└── tests/                       # Tests unitaires (aucun affichage requis)
    ├── test_covers.py           # Rendu, robustesse et performance des couvertures
    ├── test_game_manager.py     # CRUD + persistance JSON
    └── test_theme_exports.py    # Anti-ImportError (noms de config/theme)
```

---

## 🚀 Installation et Lancement

### Prérequis

- **Python 3.9 ou supérieur** — [Télécharger Python](https://www.python.org/downloads/)
- **Windows 10/11**

### Étape 1 : Cloner / Télécharger le projet

```bash
git clone <url-du-repo>
cd Launcher
```

### Étape 2 : Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### Étape 4 : Lancer en mode développement

```bash
python main.py
```

---

## 📦 Compilation en .exe

### Option A — Fichier unique (.exe autonome)

Double-cliquez sur `build_onefile.bat` ou exécutez :

```bash
build_onefile.bat
```

Le fichier `NiLauncher.exe` sera généré dans `dist/`.

### Option B — Dossier complet (démarrage plus rapide)

Double-cliquez sur `build.bat` ou exécutez :

```bash
build.bat
```

Le dossier `dist/NiLauncher/` contiendra l'exécutable et ses dépendances.

### Depannage : `pip` non reconnu

Les scripts utilisent maintenant `python -m pip` et `python -m PyInstaller` :
les commandes `pip` et `pyinstaller` n'ont plus besoin d'etre dans le `PATH`.
Ils utilisent Python 3.9+ via `python` (en respectant un environnement virtuel
active), puis essaient `py -3` si necessaire. Si pip manque, ils tentent de
l'installer avec `ensurepip --upgrade`.

Si aucun Python compatible n'est trouve, installez Python 3.9+ avec les options
**pip** et **Add Python to PATH**, puis rouvrez votre terminal. Pour une
installation manuelle lorsque seule la commande `py` fonctionne :

```bat
py -3 -m ensurepip --upgrade
py -3 -m pip install -r requirements.txt
```

Les messages des scripts sont en ASCII pour eviter les caracteres illisibles
lies a l'encodage de la console Windows. L'icone personnalisee est optionnelle.

### Compilation avec le fichier launcher.spec

```bash
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm launcher.spec
```

Le dossier `launcher/assets/` et l'icône `launcher/assets/icon.ico` sont
**optionnels** : le `.spec` ne les déclare que s'ils existent, sinon
PyInstaller s'arrête sur « Unable to find 'launcher/assets' ».

### Compilation manuelle avec PyInstaller

```bash
# Installation de PyInstaller
python -m pip install pyinstaller

# Compilation (fichier unique)
python -m PyInstaller --noconfirm --onefile --windowed \
    --name "NiLauncher" \
    --add-data "launcher;launcher" \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "customtkinter" \
    --collect-all "customtkinter" \
    main.py
```

> **Note** : Sur Windows, utilisez `--add-data "launcher;launcher"` (point-virgule).
> Sur Linux/macOS, utilisez `--add-data "launcher:launcher"` (colon).

---

## 🎨 Personnalisation

### Changer les couleurs

Modifiez le dictionnaire `COLORS` dans `launcher/config.py` :

```python
COLORS = {
    "bg_primary": "#0d1117",       # Fond principal
    "accent_primary": "#6366f1",   # Couleur d'accent
    "accent_hover": "#818cf8",     # Accent au survol
    # ... etc.
}
```

### Ajouter une icône personnalisée

Placez votre fichier `.ico` dans `launcher/assets/icon.ico` avant la compilation.

---

## 🔧 Architecture Technique

### Stack

| Composant | Technologie |
|---|---|
| Interface graphique | **CustomTkinter** (tkinter moderne) |
| Traitement d'images | **Pillow** (PIL) |
| Packaging | **PyInstaller** |
| Stockage | **JSON** (games.json) |

### Design Pattern

- **MVC simplifié** : Séparation entre la logique métier (`game_manager.py`) et l'interface (`ui/`)
- **Configuration centralisée** : Toutes les constantes dans `config.py`
- **Thème unifié** : Couleurs et styles définis dans `ui/theme.py`
- **Callbacks** : Communication entre composants via fonctions de rappel

---

## ✅ Tests et vérifications

Les tests ne touchent pas à l'interface graphique : ils tournent donc aussi bien
sur Windows que sur Linux/macOS.

```bash
# 30 tests : couvertures, persistance JSON, noms exportés par config/theme
python -m unittest discover -s tests -v

# Analyse statique (optionnel, repère les imports morts)
python -m pyflakes main.py launcher tests
```

| Test | Ce qu'il verrouille |
|---|---|
| `test_theme_exports` | Aucun `ImportError` au démarrage : chaque nom importé de `config` / `theme` existe |
| `test_game_manager` | Ajout, édition, suppression, horodatage de session, `games.json` corrompu ignoré |
| `test_covers` | Couverture par défaut identique à l'ancienne version mais bien plus rapide, image absente/illisible gérée |

---

## 📝 Format de sauvegarde (games.json)

```json
[
  {
    "id": "a1b2c3d4",
    "name": "The Witcher 3",
    "exe_path": "C:\\Games\\Witcher3\\bin\\witcher3.exe",
    "cover_path": "C:\\Launcher\\covers\\a1b2c3d4.png",
    "last_played": "2026-10-10T14:30:00"
  }
]
```

---

## 📄 Licence

MIT — Utilisation libre à des fins personnelles et commerciales.
