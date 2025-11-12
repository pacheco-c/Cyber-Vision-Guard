10 Novembre 2025

- Creata struttura cartelle del progetto
- Scritto documento di idea iniziale
- Creato ambiente virtuale Python
- Installate librerie base
- Testata webcam integrata con OpenCV (OK)
- Implementata lettura di frame consecutivi (frame_precedente e frame_corrente)
- Aggiunta elaborazione delle differenze tra i frame con OpenCV
- Ora il sistema mostra la "mappa di differenza" (aree bianche dove c'è movimento)
- Implementata rilevazione contorni con cv2.findContours
- Disegnati rettangoli verdi sulle aree di movimento
- Sistema genera alert testuale in console quando viene rilevato movimento reale
- Implementata gestione intelligente degli alert
- Aggiunto controllo temporale (SOGLIA_TEMPO e COOLDOWN) per evitare falsi positivi e messaggi ripetuti
- Ora il sistema invia un alert solo se il movimento è continuo per almeno 0.5s e non vengono generati nuovi alert entro 4s

11 Novembre 2025

- Creata cartella /models per i modelli AI
- Scaricato e aggiunto il modello Haar Cascade (haarcascade_fullbody.xml)
- Creato e testato person_detector_test.py per riconoscimento persone con webcam
- Verificato funzionamento base del modello (rettangoli blu sui corpi rilevati)
- Sostituito modello Haar Cascade con HOG + SVM per rilevamento persone
- Migliorata sensibilità e ridotti i falsi positivi
- Verificato funzionamento con illuminazione ambientale normale
- Integrato YOLOv8 (Ultralytics) per rilevamento persone e oggetti
- Creato script person_detector_yolo.py con riconoscimento in tempo reale
- Verificato funzionamento con webcam su Mac M4
- Integrato rilevamento movimento nel file principale cyber_vision_guard.py
- Aggiunto confronto frame → soglia → contorni → flag movimento_rilevato
- Integrato YOLOv8 nel ciclo di Motion Detection
- Sistema ora rileva movimento e verifica se è causato da una persona
- Aggiunto alert visivo rosso "Persona in movimento rilevata"
- Test preliminare completato con webcam in tempo reale

12 Novembre 2025
- Creato modulo `event_manager.py` per la gestione intelligente degli eventi.
- Implementata logica di inizio/fine evento con timestamp e durata.
- Integrato Event Manager nel loop principale di `cyber_vision_guard.py`.
- Ora il sistema genera un solo log per ogni persona rilevata, evitando spam e rallentamenti.
- Creato modulo `security/encryptor.py` per cifratura e firma digitale.
- Implementata generazione automatica della chiave segreta (`secret.key`).
- Integrato nel loop principale: ogni evento viene ora cifrato e firmato.
- Test eseguito: generazione file `.enc` in /logs con hash verificabile.