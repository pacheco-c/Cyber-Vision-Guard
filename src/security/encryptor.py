# --- src/security/encryptor.py ---
import json, time, hashlib, os
from cryptography.fernet import Fernet

# Percorsi dinamici
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
SECURITY_DIR = BASE_DIR                                
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))  
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Creazione cartelle se mancano
os.makedirs(LOGS_DIR, exist_ok=True)

# Percorso chiave segreta
key_path = os.path.join(SECURITY_DIR, "secret.key")

# Se non esiste, genera una nuova chiave segreta
if not os.path.exists(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
else:
    with open(key_path, "rb") as f:
        key = f.read()

fernet = Fernet(key)

def cifra_evento(evento_dict):
    """
    Cifra e firma un evento, poi lo salva nella cartella logs/ in root.
    Restituisce l'hash (firma) del file generato.
    """
    # Converti il dizionario in JSON
    data = json.dumps(evento_dict, indent=4).encode()

    # Cifra i dati
    data_cifrata = fernet.encrypt(data)

    # Calcola la firma SHA256 della parte cifrata
    firma = hashlib.sha256(data_cifrata).hexdigest()

    # Crea il nome file univoco
    filename = os.path.join(LOGS_DIR, f"event_{int(time.time())}.enc")

    # Salva i dati cifrati
    with open(filename, "wb") as f:
        f.write(data_cifrata)

    print(f"🔐 Evento cifrato e salvato: {filename}")
    print(f"🧾 Firma digitale: {firma[:12]}...")  # stampa prime 12 cifre
    return firma