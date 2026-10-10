@echo off
setlocal
REM ASCII messages stay readable regardless of the Windows console code page.
REM Work from the script directory, including paths with spaces or UNC paths.
pushd "%~dp0"
if errorlevel 1 (
    echo [ERREUR] Impossible d'ouvrir le dossier du projet.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo    NiLauncher - Compilation One-File .exe
echo ============================================================
echo.

REM Prefer python to respect an activated virtual environment; try py next.
set "PYTHON=python"
%PYTHON% -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
if not errorlevel 1 goto python_ready
set "PYTHON=py -3"
%PYTHON% -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
if not errorlevel 1 goto python_ready
echo [ERREUR] Python 3.9+ est introuvable.
echo Installez Python depuis https://www.python.org/downloads/
echo Activez l'option Add Python to PATH, puis relancez ce script.
goto failed

:python_ready
REM Use modules so pip and PyInstaller need not be on PATH.
%PYTHON% -m pip --version >nul 2>&1
if not errorlevel 1 goto install_dependencies
echo Installation de pip pour Python...
%PYTHON% -m ensurepip --upgrade
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer pip. Reparez l'installation de Python
    echo en incluant pip, puis relancez ce script.
    goto failed
)

:install_dependencies
echo [1/3] Installation des dependances...
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances.
    goto failed
)

echo.
echo [2/3] Compilation avec PyInstaller...
echo       Cela peut prendre quelques minutes...
echo.

REM The custom icon is optional.
set "ICON_OPTION="
if exist "launcher\assets\icon.ico" set ICON_OPTION=--icon "launcher\assets\icon.ico"

%PYTHON% -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "NiLauncher" ^
    --add-data "launcher;launcher" ^
    --hidden-import "PIL._tkinter_finder" ^
    --hidden-import "customtkinter" ^
    --collect-all "customtkinter" ^
    %ICON_OPTION% ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERREUR] La compilation a echoue.
    echo Verifiez les messages d'erreur ci-dessus.
    goto failed
)

echo.
echo [3/3] Compilation terminee avec succes !
echo.
echo    Votre launcher : dist\NiLauncher.exe
echo.
popd
pause
exit /b 0

:failed
popd
pause
exit /b 1
