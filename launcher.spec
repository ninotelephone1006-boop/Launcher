# -*- mode: python ; coding: utf-8 -*-
"""
Fichier de spécification PyInstaller pour NiLauncher.
Peut être utilisé avec : pyinstaller launcher.spec

Compatible PyInstaller 6.x (celui installé par requirements.txt).
"""
from pathlib import Path

# ─── Assets et icône : optionnels ───────────────────────────────────────────
# Ils ne sont déclarés que s'ils existent réellement : PyInstaller échoue
# immédiatement sur un chemin absent
# (« ERROR: Unable to find 'launcher/assets' when adding binary and data files. »).
ASSETS_DIR = Path('launcher') / 'assets'
ICON_PATH = ASSETS_DIR / 'icon.ico'

datas = [(str(ASSETS_DIR), 'launcher/assets')] if ASSETS_DIR.is_dir() else []
icon = str(ICON_PATH) if ICON_PATH.is_file() else None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PIL._tkinter_finder',
        'PIL._imagingtk',
        'customtkinter',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'json',
        'uuid',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'pytest',
    ],
    noarchive=False,
)

# PyInstaller 6.x : plus d'argument 'cipher' (RemovedCipherFeatureError)
# et 'a.zipped_data' est toujours vide (les eggs zippés ne sont plus supportés).
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NiLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Mode fenêtré (pas de console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)
