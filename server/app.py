# --- server/app.py ---
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from flask import Flask, request, jsonify, render_template
from security.decryptor import decifra_evento
from flask import send_from_directory
from security.hash_chain import aggiorna_catena, verifica_catena
from database_manager import salva_evento, leggi_eventi
from flask import send_file
from io import BytesIO
from security.decryptor import decifra_file_bytes
from datetime import datetime


app = Flask(__name__)
verifica_catena()

# Crea la cartella dove salvare i file ricevuti
os.makedirs("server/received_logs", exist_ok=True)





@app.route("/image/<path:filename>")
def mostra_immagine(filename):
    """
    Decifra temporaneamente l'immagine cifrata (.enc) e la invia al browser.
    L'immagine non viene mai salvata in chiaro su disco.
    """
    from flask import send_file
    from io import BytesIO
    from security.decryptor import decifra_file_bytes

    full_path = os.path.join("server/received_images", filename)
    if not os.path.exists(full_path):
        return "File non trovato", 404

    try:
        # Decifra il contenuto in RAM
        decrypted_bytes = decifra_file_bytes(full_path)

        # Ritorna al browser come immagine JPEG temporanea
        return send_file(BytesIO(decrypted_bytes), mimetype="image/jpeg")

    except Exception as e:
        print(f"❌ Errore decifratura immagine: {e}")
        return "Errore nella decifratura", 500

@app.route("/api/alert", methods=["POST"])
def ricevi_alert():
    """
    Riceve un file cifrato e un'immagine cifrata dal client,
    li salva localmente e aggiorna il database + hash chain.
    """
    try:
        # === 1️⃣ File log cifrato ===
        file_log = request.files.get("file")
        if not file_log:
            return jsonify({"status": "error", "message": "Nessun file di log ricevuto"}), 400

        os.makedirs("server/received_logs", exist_ok=True)
        log_path = f"server/received_logs/{int(time.time())}_{file_log.filename}"
        file_log.save(log_path)
        print(f"🧾 Log cifrato ricevuto: {log_path}")

        # === 2️⃣ File immagine cifrata (opzionale) ===
        file_img = request.files.get("image")
        img_path = None
        if file_img:
            os.makedirs("server/received_images", exist_ok=True)
            img_path = f"server/received_images/{int(time.time())}_{file_img.filename}"
            file_img.save(img_path)
            print(f"🖼️ Immagine cifrata ricevuta: {img_path}")
        else:
            print("⚠️ Nessuna immagine cifrata ricevuta (campo 'image' mancante).")

        # === 3️⃣ Decifra e processa il log ===
        try:
            evento = decifra_evento(log_path)
            print(f"📄 Evento decifrato: {evento}")

            # Verifica catena di integrità
            try:
                verifica_catena()
            except Exception as e:
                print(f"⚠️ Errore nella verifica catena: {e}")

            # Aggiorna catena hash
            nuovo_hash, hash_precedente = aggiorna_catena(evento)
            print(f"🔗 Hash chain aggiornata → {nuovo_hash[:10]}...")

            # Salva nel database (aggiungendo eventuale riferimento all’immagine)
            evento["screenshot_path"] = img_path  # aggiunge il campo immagine
            salva_evento(evento, nuovo_hash, hash_precedente)

            print("💾 Evento e immagine salvati correttamente nel database.")

        except Exception as e:
            print(f"❌ Errore durante la decifratura o salvataggio: {e}")

        return jsonify({"status": "ok", "message": "File ricevuti e registrati"}), 200

    except Exception as e:
        print(f"🚨 Errore ricezione: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    eventi = leggi_eventi()
    stato_catena = verifica_catena()

    # 🔄 Conversione timestamp UNIX → data leggibile
    for ev in eventi:
        if ev.get("timestamp_inizio"):
            ev["timestamp_inizio_fmt"] = datetime.fromtimestamp(ev["timestamp_inizio"]).strftime("%d/%m/%Y %H:%M:%S")
        else:
            ev["timestamp_inizio_fmt"] = None
        if ev.get("timestamp_fine"):
            ev["timestamp_fine_fmt"] = datetime.fromtimestamp(ev["timestamp_fine"]).strftime("%d/%m/%Y %H:%M:%S")
        else:
            ev["timestamp_fine_fmt"] = None

    # 🎯 Asse X = ID evento, Asse Y = durata
    labels = [ev["id"] for ev in eventi if ev.get("durata")]
    durate = [ev["durata"] for ev in eventi if ev.get("durata")]

    # Dati per tooltip (data + tipo)
    tooltip_info = [
        f"{ev['timestamp_inizio_fmt']} ({ev['tipo']})" for ev in eventi if ev.get("durata")
    ]

    return render_template(
        "dashboard.html",
        eventi=eventi,
        stato=stato_catena,
        labels=labels,
        durate=durate,
        tooltips=tooltip_info
    )
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)