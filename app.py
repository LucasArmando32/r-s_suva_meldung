"""
SUVA-Anmeldungs-Webapp
Flask-Backend mit HTML-Formular.
Generiert Sanierungsplan, Luftbilanz und SUVA-Anmeldung als ZIP-Download.
"""
import io
import os
import sys
import traceback
import zipfile
from datetime import datetime

try:
    from flask import Flask, render_template, request, send_file, jsonify
except ImportError:
    print("\n[FEHLER] Flask ist nicht installiert.")
    print("Bitte ausfuehren:  pip3 install flask python-docx openpyxl")
    print("Oder:              pip3 install -r requirements.txt\n")
    sys.exit(1)

from generators import generate_all

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILES_DIR = os.path.join(BASE_DIR, "template_files")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=STATIC_DIR,
)

# Generated-Ordner immer beim Start anlegen (auch unter Gunicorn/Docker)
os.makedirs(GENERATED_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    """Einfacher Health-Check zum Verifizieren dass der Server laeuft."""
    return jsonify({
        "status": "ok",
        "base_dir": BASE_DIR,
        "templates_exist": os.path.exists(os.path.join(TEMPLATE_FILES_DIR, "sanierungsplan_template.docx")),
        "luftbilanz_template_exists": os.path.exists(os.path.join(TEMPLATE_FILES_DIR, "luftbilanz_template.xlsx")),
    })


@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Form-Daten einsammeln
        data = {key: request.form.get(key, "").strip() for key in request.form.keys()}

        # Checkbox-Felder: existieren nur wenn angehakt
        for cb in ("art_asbest", "art_pcb", "art_pak", "suva_anmeldung"):
            data[cb] = request.form.get(cb) == "ja"

        # Eindeutigen Unterordner fuer diese Anmeldung
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_label = (data.get("baustelle_adresse", "anmeldung")
                      .replace("/", "_").replace(" ", "_"))[:40] or "anmeldung"
        out_dir = os.path.join(GENERATED_DIR, f"{timestamp}_{safe_label}")

        # Dokumente generieren
        paths = generate_all(data, out_dir, TEMPLATE_FILES_DIR)

        # ZIP im Speicher
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for _, filepath in paths.items():
                zf.write(filepath, arcname=os.path.basename(filepath))
        buf.seek(0)

        zip_name = f"SUVA_Anmeldung_{safe_label}_{timestamp}.zip"
        print(f"[OK] ZIP generiert: {zip_name} ({len(buf.getvalue())} bytes)")

        return send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=zip_name,
        )

    except Exception as exc:
        err = traceback.format_exc()
        print("[FEHLER] Generierung fehlgeschlagen:\n", err)
        html = f"""
        <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Fehler</title></head>
        <body style="font-family:sans-serif; max-width:900px; margin:40px auto; padding:0 20px;">
        <h1 style="color:#C8102E;">Fehler beim Generieren</h1>
        <p><strong>{type(exc).__name__}:</strong> {exc}</p>
        <pre style="background:#f4f4f5; padding:20px; border-radius:8px; overflow:auto; font-size:13px;">{err}</pre>
        <p><a href="/" style="color:#C8102E;">&larr; Zurueck zum Formular</a></p>
        </body></html>
        """
        return html, 500


def main():
    os.makedirs(GENERATED_DIR, exist_ok=True)
    port = int(os.environ.get("PORT", 8000))

    print("\n" + "=" * 60)
    print("  R+S SUVA Anmeldung - Webapp")
    print("=" * 60)
    print(f"  URL:        http://127.0.0.1:{port}")
    print(f"  Health:     http://127.0.0.1:{port}/health")
    print(f"  Beenden:    Ctrl+C")
    print("=" * 60 + "\n")

    # Templates pruefen
    tpl_doc = os.path.join(TEMPLATE_FILES_DIR, "sanierungsplan_template.docx")
    tpl_xls = os.path.join(TEMPLATE_FILES_DIR, "luftbilanz_template.xlsx")
    if not os.path.exists(tpl_doc):
        print(f"[WARNUNG] Template fehlt: {tpl_doc}")
    if not os.path.exists(tpl_xls):
        print(f"[WARNUNG] Template fehlt: {tpl_xls}")

    app.run(host="127.0.0.1", port=port, debug=True)


if __name__ == "__main__":
    main()
