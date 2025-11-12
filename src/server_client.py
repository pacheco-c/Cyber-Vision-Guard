# --- src/server_client.py ---
import requests, os

SERVER_URL = "http://127.0.0.1:5000/api/alert"

def invia_file_al_server(percorso_file):
    """
    Invia un file cifrato (.enc) al server Flask.
    Restituisce True se l'invio ha successo, False in caso di errore.
    """
    if not os.path.exists(percorso_file):
        print(f" File non trovato: {percorso_file}")
        return False

    try:
        with open(percorso_file, "rb") as f:
            files = {"file": f}
            response = requests.post(SERVER_URL, files=files)

        if response.status_code == 200:
            print(f"File inviato con successo → {os.path.basename(percorso_file)}")
            return True
        else:
            print(f"Errore invio ({response.status_code}): {response.text}")
            return False

    except Exception as e:
        print(f"🚨 Errore durante l'invio: {e}")
        return False