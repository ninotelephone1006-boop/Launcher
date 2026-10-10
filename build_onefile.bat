@echo off
REM ============================================================
REM  Script de compilation en UN SEUL fichier .exe (onefile)
REM  Le résultat est un unique NiLauncher.exe autonome.
REM ============================================================

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   NiLauncher - Compilation One-File .exe             ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.9+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation des dépendances.
    pause
    exit /b 1
)

echo.
echo [2/3] Compilation avec PyInstaller (mode one-file)...
echo       Cela peut prendre plusieurs minutes...
echo.

pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "NiLauncher" ^
    --add-data "launcher;launcher" ^
    --hidden-import "PIL._tkinter_finder" ^
    --hidden-import "customtkinter" ^
    --collect-all "customtkinter" ^
    --icon "launcher/assets/icon.ico" ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERREUR] La compilation a échoué.
    pause
    exit /b 1
)

echo.
echo [3/3] Compilation terminée avec succès !
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   Fichier exécutable unique :                        ║
echo ║   dist\NiLauncher.exe                                ║
echo ║                                                      ║
echo ║   Ce fichier est 100%% autonome et portable.          ║
echo ╚══════════════════════════════════════════════════════╝
echo.
pause
