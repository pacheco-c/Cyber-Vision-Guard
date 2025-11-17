# --- src/event_manager.py ---
import time

# Stato globale dell'evento
evento_attivo = False
inizio_evento = 0

# Durata minima (in secondi) richiesta per considerare valido un evento
DURATA_MINIMA = 2.0  # ← puoi cambiare questo valore a piacere

def gestisci_evento(persona_rilevata):
    """
    Gestisce l'inizio e la fine di un evento di rilevamento persona.
    Restituisce un dizionario SOLO se la durata supera DURATA_MINIMA.
    """
    global evento_attivo, inizio_evento

    # 🟢 1. Se rilevi una persona e non c'è un evento in corso → inizia il timer
    if persona_rilevata and not evento_attivo:
        evento_attivo = True
        inizio_evento = time.time()
        print("🟢 Nuovo evento iniziato (timer avviato).")

    # 🟡 2. Se la persona se ne va → calcola durata
    elif not persona_rilevata and evento_attivo:
        fine_evento = time.time()
        durata = round(fine_evento - inizio_evento, 2)
        evento_attivo = False

        # 🔴 Se durata è inferiore alla soglia → ignora
        if durata < DURATA_MINIMA:
            print(f"⚠️ Movimento troppo breve ({durata}s) — evento ignorato.")
            return None

        # ✅ Evento valido → restituisci i dati
        evento = {
            "timestamp_inizio": inizio_evento,
            "timestamp_fine": fine_evento,
            "durata": durata,
            "tipo": "persona_rilevata"
        }

        print(f"🔴 Evento terminato (durata: {durata}s). Log registrato.")
        return evento

    # 🔁 Se non cambia nulla, non ritorna niente
    return None

