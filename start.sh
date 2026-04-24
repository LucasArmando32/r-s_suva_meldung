#!/bin/bash
# Startskript fuer die SUVA-Anmeldungs-Webapp (macOS/Linux)
set -e
cd "$(dirname "$0")"

PY=python3
if ! command -v $PY >/dev/null 2>&1; then
    echo "FEHLER: python3 nicht gefunden. Bitte Python 3 installieren."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Lege virtuelle Python-Umgebung an..."
    $PY -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installiere Abhaengigkeiten..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "=============================================="
echo "  SUVA-Anmeldung App startet auf Port 8000"
echo "  Oeffne im Browser: http://127.0.0.1:8000"
echo "  Zum Beenden: Ctrl+C"
echo "=============================================="
echo ""

python app.py
