# Cyber-Vision Guard

Sistema di sorveglianza AI-secure locale: rileva movimento e persone via
webcam, cifra e firma digitalmente ogni evento rilevato, lo invia a un
server Flask locale che ne verifica l'integrità tramite una catena di
hash, lo salva su MySQL e lo espone su una dashboard web con grafico
degli eventi.

Progetto personale che combina visione artificiale (OpenCV, YOLOv8),
cybersecurity (crittografia Fernet, firma SHA256, hash chain) e sviluppo
web (Flask, Chart.js).

## Architettura

```
Webcam
  │  motion detection (OpenCV, differenza tra frame)
  ▼
Verifica persona (YOLOv8)
  │  filtro durata minima evento
  ▼
Cifratura Fernet + firma SHA256  (client, src/security/encryptor.py)
  │  invio HTTP (log + screenshot)
  ▼
Server Flask (server/app.py)
  │  decifratura, verifica hash chain, salvataggio
  ▼
MySQL (tabella eventi) ──► Dashboard web (Chart.js)
```

## Struttura del progetto

```
src/
  cyber_vision_guard.py   # entry point client: motion detection + YOLO + invio eventi
  event_manager.py        # logica inizio/fine evento e durata minima
  server_client.py        # invio HTTP dei file cifrati al server
  security/
    encryptor.py           # cifratura Fernet + firma SHA256 (client)
    decryptor.py            # decifratura (lato server)
    hash_chain.py            # catena di hash per l'integrità degli eventi
server/
  app.py                  # server Flask: riceve, verifica, salva, espone la dashboard
  database_manager.py     # connessione e query MySQL
  templates/dashboard.html
archive/                  # prototipo originale (motion detection senza YOLO)
documents/
  development_log.md      # diario di sviluppo
  project_idea.md          # idea iniziale del progetto
```

## Prerequisiti

- Python 3.8+
- MacBook (o altro dispositivo) con webcam
- Server MySQL locale in esecuzione

## Setup

1. Clona il repository e crea un ambiente virtuale:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copia `.env.example` in `.env` e inserisci le credenziali del tuo
   MySQL locale:
   ```
   cp .env.example .env
   ```

3. Crea il database e la tabella `eventi`:
   ```sql
   CREATE DATABASE IF NOT EXISTS cyber_vision_guard;
   USE cyber_vision_guard;

   CREATE TABLE eventi (
       id INT AUTO_INCREMENT PRIMARY KEY,
       timestamp_inizio DOUBLE NOT NULL,
       timestamp_fine DOUBLE NOT NULL,
       durata FLOAT NOT NULL,
       tipo VARCHAR(50) NOT NULL,
       hash_corrente VARCHAR(64) NOT NULL,
       hash_precedente VARCHAR(64) NOT NULL,
       screenshot_path VARCHAR(255)
   );
   ```

La chiave di cifratura (`src/security/secret.key`) viene generata
automaticamente al primo avvio, non serve crearla a mano.

## Avvio

Entrambi i comandi vanno lanciati dalla root del progetto, in due
terminali separati.

Server (riceve gli eventi ed espone la dashboard):
```
python server/app.py
```
Dashboard disponibile su `http://127.0.0.1:5000/dashboard`.

Client (avvia webcam e rilevamento):
```
python src/cyber_vision_guard.py
```
Premi `q` nella finestra video per terminare.

## Sicurezza

- Ogni evento viene cifrato con Fernet (AES simmetrico) prima di
  lasciare il client.
- Ogni file cifrato è firmato con un hash SHA256, verificabile lato
  server.
- Gli eventi sono concatenati in una hash chain (`server/hash_chain.json`):
  ogni blocco include l'hash del precedente, così un'alterazione di un
  evento passato invalida tutta la catena successiva.
- Le credenziali MySQL non sono mai hardcoded: vengono lette da `.env`
  (non versionato).

## Note di sviluppo

Il diario di sviluppo con la cronologia dettagliata dei passi seguiti
è in [`documents/development_log.md`](documents/development_log.md).
