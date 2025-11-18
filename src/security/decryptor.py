# --- src/security/decryptor.py ---
import json, hashlib
import os
from cryptography.fernet import Fernet


def decifra_evento(percorso_file_enc, key_path=None):
    """
    Decifra un file .enc ricevuto e verifica la sua integrità tramite hash SHA256.
    Restituisce il dizionario originale del log se valido.
    """
   
    if key_path is None:
        key_path = os.path.join(os.path.dirname(__file__), "secret.key")
    # Carica la chiave
    with open(key_path, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    # Leggi il file cifrato
    with open(percorso_file_enc, "rb") as f:
        data_cifrata = f.read()

    # Calcola l’hash per la verifica
    firma_calcolata = hashlib.sha256(data_cifrata).hexdigest()

    # Decifra i dati
    data_decifrata = fernet.decrypt(data_cifrata)
    evento = json.loads(data_decifrata.decode())

    print("Log decifrato correttamente!")
    print(f" Firma SHA256: {firma_calcolata[:16]}...")
    print(f" Evento: {evento}")
    return evento

def decifra_file_bytes(percorso_file):
    """
    Decifra un file cifrato (.enc) e restituisce i bytes del contenuto.
    Utile per inviare immagini al browser senza scrivere su disco.
    """
    

    key_path = os.path.join(os.path.dirname(__file__), "secret.key")
    # Carica la chiave
    with open(key_path, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    with open(percorso_file, "rb") as f:
        dati_cifrati = f.read()

    dati_decifrati = fernet.decrypt(dati_cifrati)
    return dati_decifrati