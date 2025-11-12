# --- src/security/hash_chain.py ---
import hashlib, json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
CHAIN_FILE = "server/hash_chain.json"

def aggiorna_catena(evento):
    """
    Aggiorna la catena di hash aggiungendo il nuovo evento.
    Crea il file se non esiste.
    """
    os.makedirs(os.path.dirname(CHAIN_FILE), exist_ok=True)

    # Leggi catena precedente
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, "r") as f:
            chain = json.load(f)
    else:
        chain = []

    # Hash del precedente
    prev_hash = chain[-1]["hash"] if chain else "0" * 64

    # Calcola nuovo hash (evento + hash precedente)
    combined = json.dumps(evento, sort_keys=True).encode() + prev_hash.encode()
    new_hash = hashlib.sha256(combined).hexdigest()

    chain.append({
        "evento": evento,
        "hash_precedente": prev_hash,
        "hash": new_hash
    })

    # Salva catena aggiornata
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

    print(f"🧱 Hash chain aggiornata. Nuovo blocco: {new_hash[:16]}...")
    return new_hash

def verifica_catena():
    """
    Verifica l'integrità completa della catena hash.
    Restituisce True se tutti i blocchi sono coerenti.
    """
    if not os.path.exists(CHAIN_FILE):
        print("⚠️ Nessuna catena trovata.")
        return False

    with open(CHAIN_FILE, "r") as f:
        chain = json.load(f)

    for i in range(1, len(chain)):
        evento = chain[i]["evento"]
        hash_prev_registrato = chain[i]["hash_precedente"]

        # Ricalcolo hash del blocco precedente
        combined = json.dumps(chain[i - 1]["evento"], sort_keys=True).encode() + chain[i - 1]["hash_precedente"].encode()
        hash_prev_calcolato = hashlib.sha256(combined).hexdigest()

        if hash_prev_calcolato != hash_prev_registrato:
            print(f"  Errore di integrità al blocco {i}!")
            print(f"  Atteso: {hash_prev_calcolato[:16]}...")
            print(f"  Trovato: {hash_prev_registrato[:16]}...")
            return False

    print(" Catena di integrità verificata: tutti i blocchi sono coerenti.")
    return True