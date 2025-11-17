# --- server/database_manager.py ---
import mysql.connector
from mysql.connector import Error

def crea_connessione():
    """
    Crea una connessione al database MySQL locale.
    Restituisce l'oggetto connessione se va a buon fine, altrimenti None.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",            # Cambia se usi un utente diverso
            password="",  # Inserisci la tua password MySQL
            database="cyber_vision_guard"
        )
        if conn.is_connected():
            print("✅ Connessione al database MySQL riuscita.")
            return conn
    except Error as e:
        print("❌ Errore durante la connessione:", e)
    return None

def salva_evento(evento, hash_corrente, hash_precedente):
    """
    Salva un evento decifrato nel database MySQL.
    """
    conn = crea_connessione()
    if conn is None:
        print("❌ Connessione al DB fallita, evento non salvato.")
        return

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO eventi (timestamp_inizio, timestamp_fine, durata, tipo, hash_corrente, hash_precedente)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        dati = (
            evento["timestamp_inizio"],
            evento["timestamp_fine"],
            evento["durata"],
            evento["tipo"],
            hash_corrente,
            hash_precedente
        )
        cursor.execute(query, dati)
        conn.commit()
        
    except Error as e:
        print("❌ Errore durante l'inserimento:", e)
    finally:
        cursor.close()
        conn.close()