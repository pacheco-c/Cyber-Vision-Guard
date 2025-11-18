# --- src/server_client.py ---
import requests, os

SERVER_URL = "http://127.0.0.1:5000/api/alert"

def invia_file_al_server(percorso_file, screenshot_path=None):
    """
    Invia un file cifrato (.enc) e, se disponibile, anche uno screenshot al server Flask.
    Restituisce True se l'invio ha successo, False in caso di errore.
    """
    if not os.path.exists(percorso_file):
        print(f"❌ File non trovato: {percorso_file}")
        return False

    # Prepara i file da inviare
    files = {"file": open(percorso_file, "rb")}

    if screenshot_path and os.path.exists(screenshot_path):
        files["image"] = open(screenshot_path, "rb")
        print(f"📸 Allegato screenshot: {os.path.basename(screenshot_path)}")

    try:
        response = requests.post(SERVER_URL, files=files)

        if response.status_code == 200:
            print(f"✅ File inviato con successo → {os.path.basename(percorso_file)}")
            return True
        else:
            print(f"⚠️ Errore invio ({response.status_code}): {response.text}")
            return False

    except Exception as e:
        print(f"🚨 Errore durante l'invio: {e}")
        return False

    finally:
        # Chiude tutti i file aperti
        for f in files.values():
            f.close()