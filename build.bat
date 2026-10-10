@echo off
REM ============================================================
REM  Script de compilation du launcher NiLauncher en .exe
REM  Exécuter ce script sous Windows avec Python >= 3.9 installé
REM ============================================================

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   NiLauncher - Compilateur en .exe                   ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM Vérifier que Python est installé
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
echo [2/3] Compilation avec PyInstaller...
echo       Cela peut prendre quelques minutes...
echo.

pyinstaller ^
    --noconfirm ^
    --onedir ^
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
    echo Vérifiez les messages d'erreur ci-dessus.
    pause
    exit /b 1
)

echo.
echo [3/3] Compilation terminée avec succès !
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   Votre launcher se trouve dans :                    ║
echo ║   dist\NiLauncher\NiLauncher.exe                     ║
echo ║                                                      ║
echo ║   Vous pouvez copier le dossier dist\NiLauncher      ║
echo ║   n'importe où et lancer NiLauncher.exe !            ║
echo ╚══════════════════════════════════════════════════════╝
echo.
pause
