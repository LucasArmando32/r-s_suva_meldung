# SUVA Anmeldung - R+S Asbest Sanierung GmbH

Webapp zum automatischen Generieren der 3 SUVA-Anmeldungs-Dokumente.

## Generierte Dokumente

1. **Sanierungsplan.docx** - basiert auf der Vorlage (Tulpenweg)
2. **Luftbilanz.xlsx** - Excel mit Berechnungs-Formeln
3. **SUVA_Anmeldung.docx** - strukturiertes SUVA-Anmeldeformular

## Installation & Start (einmalig einrichten)

### Mac / Linux

Einfach im Terminal:

```bash
cd "R+S Suva Anmeldung"
bash start.sh
```

Beim ersten Mal installiert das Skript alles automatisch. Dann startet die App.

### Windows

Doppelklick auf `start.bat`.

### Manueller Weg (falls die Skripte nicht laufen)

```bash
# 1. In den Ordner wechseln
cd "R+S Suva Anmeldung"

# 2. Flask & co installieren
pip3 install flask python-docx openpyxl

# 3. App starten
python3 app.py
```

## Benutzung

1. Im Browser öffnen: **http://127.0.0.1:8000**
2. Formular ausfüllen (Baustelle, Bauherr, Schadstoff, Raumdimensionen, etc.)
3. Auf "3 Dokumente generieren" klicken
4. Eine ZIP-Datei mit allen 3 Dokumenten wird automatisch heruntergeladen

## Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'flask'"**
> Lösung: `pip3 install flask python-docx openpyxl`

**Problem: Port 8000 ist schon belegt**
> Lösung: `PORT=9000 python3 app.py` (dann Browser auf http://127.0.0.1:9000)

**Problem: Download startet nicht**
> Prüfe:
> 1. Läuft der Server? Du siehst im Terminal "SUVA-Anmeldung App startet..."?
> 2. Öffnest du die App auf http://127.0.0.1:8000 (nicht als `file://.../index.html`)?
> 3. Gehe auf http://127.0.0.1:8000/health um zu prüfen ob der Server antwortet
> 4. Bei einem Fehler erscheint jetzt eine rote Fehlerseite mit Details

**Problem: Port 5000 war blockiert (macOS AirPlay)**
> Die App verwendet jetzt Port **8000**.

## Docker-Deployment (Dockploy)

### Variante A: Dockploy (empfohlen)

1. In Dockploy neuen **Compose / Application** anlegen
2. Git-Repo angeben: `https://github.com/LucasArmando32/r-s_suva_meldung.git`
3. Als Dockerfile-Pfad: `./Dockerfile`
4. Port: **8000**
5. Persistent Volume: `./generated:/app/generated` (damit generierte Dokumente bleiben)
6. Deploy klicken

Dockploy baut automatisch das Image und startet den Container.

### Variante B: Lokal mit Docker

```bash
# Image bauen
docker build -t rs-suva-anmeldung .

# Container starten
docker run -d -p 8000:8000 --name rs-suva rs-suva-anmeldung

# Oder mit docker-compose
docker compose up -d
```

Dann im Browser öffnen: http://127.0.0.1:8000

### Updates deployen

```bash
git pull
docker compose up -d --build
```

## Struktur

```
R+S Suva Anmeldung/
├── app.py                    # Flask Backend
├── generators.py             # Dokument-Generator-Logik
├── requirements.txt          # Python-Abhängigkeiten
├── start.sh / start.bat      # Startskripte
├── static/                   # Logo + CSS
│   ├── logo.svg
│   └── style.css
├── templates/
│   └── index.html            # Formular
├── template_files/           # Vorlagen
│   ├── sanierungsplan_template.docx
│   └── luftbilanz_template.xlsx
└── generated/                # Hier landen generierte Dokumente
```
