# ==========================================
# R+S SUVA Anmeldung - Webapp
# Production Docker image (Gunicorn + Flask)
# ==========================================
FROM python:3.12-slim

# Labels
LABEL maintainer="R+S Asbest- und Schadstoff-Sanierung GmbH"
LABEL description="SUVA Anmeldung Webapp - generiert Sanierungsplan, Luftbilanz und Alarmliste"

# Systempakete (fuer python-docx wird nichts Spezielles benoetigt, aber locales helfen)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Python-Einstellungen
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Requirements zuerst kopieren (bessere Layer-Caching-Nutzung)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY app.py generators.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY template_files/ ./template_files/

# Output-Ordner anlegen (dort landen generierte Dokumente).
# Sollte ueber Volume gemountet werden, damit Downloads persistent bleiben.
RUN mkdir -p /app/generated && chmod 775 /app/generated

# Nicht als root laufen (Security)
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Port freigeben
EXPOSE 8000

# Healthcheck gegen /health Endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health').status==200 else 1)"

# Gunicorn als Production-WSGI-Server
# 2 Workers, 4 Threads pro Worker, 60s Timeout (fuer grosse Dokumenten-Generierung)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
