@echo off
REM Startskript fuer die SUVA-Anmeldungs-Webapp (Windows)
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo FEHLER: python nicht gefunden. Bitte Python 3 installieren.
    pause
    exit /b 1
)

if not exist "venv\" (
    echo Lege virtuelle Python-Umgebung an...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installiere Abhaengigkeiten...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo ==============================================
echo   SUVA-Anmeldung App startet auf Port 8000
echo   Oeffne im Browser: http://127.0.0.1:8000
echo   Zum Beenden: Ctrl+C
echo ==============================================
echo.

python app.py
pause
