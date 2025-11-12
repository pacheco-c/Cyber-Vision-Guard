# --- src/event_manager.py ---
import time

# Stato globale dell'evento
evento_attivo = False
inizio_evento = 0

def gestisci_evento(persona_rilevata):
    """
    Gestisce l'inizio e la fine di un evento di rilevamento persona.
    Restituisce un dizionario con i dati dell'evento SOLO quando termina.
    """
    global evento_attivo, inizio_evento

    #  Se rileviamo persona e non c'è evento in corso inizia
    if persona_rilevata and not evento_attivo:
        evento_attivo = True
        inizio_evento = time.time()
        print("🟢 Nuovo evento iniziato.")

    #  Se non c'è più persona ma c'era un evento finisce
    elif not persona_rilevata and evento_attivo:
        fine_evento = time.time()
        durata = round(fine_evento - inizio_evento, 2)
        evento_attivo = False

        evento = {
            "timestamp_inizio": inizio_evento,
            "timestamp_fine": fine_evento,
            "durata": durata,
            "tipo": "persona_rilevata"
        }

        print(f"🔴 Evento terminato (durata: {durata}s).")
        return evento  # lo restituiremo al modulo di cifratura

    # Altrimenti nessun cambiamento → nessun nuovo evento
    return None