# --- server/database_manager.py ---
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def crea_connessione():
    """
    Crea una connessione al database MySQL locale.
    Restituisce l'oggetto connessione se va a buon fine, altrimenti None.
    """
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "cyber_vision_guard")
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
            INSERT INTO eventi (timestamp_inizio, timestamp_fine, durata, tipo, hash_corrente, hash_precedente, screenshot_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        dati = (
            evento["timestamp_inizio"],
            evento["timestamp_fine"],
            evento["durata"],
            evento["tipo"],
            hash_corrente,
            hash_precedente,
            evento.get("screenshot_path")
        )
        cursor.execute(query, dati)
        conn.commit()
        
    except Error as e:
        print("❌ Errore durante l'inserimento:", e)
    finally:
        cursor.close()
        conn.close()
def leggi_eventi():
    """
    Legge tutti gli eventi dal database per la dashboard.
    Restituisce una lista di dizionari.
    """
    conn = crea_connessione()
    eventi = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventi ORDER BY timestamp_inizio DESC LIMIT 100")
        eventi = cursor.fetchall()
        cursor.close()
        conn.close()
    return eventi