# --- server/app.py ---
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from flask import Flask, request, jsonify
from security.decryptor import decifra_evento
from security.hash_chain import aggiorna_catena
from security.hash_chain import verifica_catena
import time


app = Flask(__name__)
verifica_catena()

# Crea la cartella dove salvare i file ricevuti
os.makedirs("server/received_logs", exist_ok=True)

@app.route("/api/alert", methods=["POST"])
def ricevi_alert():
    """
    Riceve un file cifrato da Cyber-Vision Guard e lo salva localmente.
    """
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"status": "error", "message": "Nessun file ricevuto"}), 400

        # Salva il file con timestamp
        filename = f"server/received_logs/{int(time.time())}_{file.filename}"
        file.save(filename)

        print(f"Ricevuto file cifrato: {filename}")
        try:
            evento = decifra_evento(filename)
            try:
                verifica_catena()
            except Exception as e:
                print(f"⚠️  Errore nella verifica della catena: {e}")
            aggiorna_catena(evento)
        except Exception as e:
            print(f"⚠️ Errore durante la decifratura: {e}")
        return jsonify({"status": "ok", "message": "File ricevuto con successo"}), 200

    except Exception as e:
        print("Errore ricezione:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)