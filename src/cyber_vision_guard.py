import os
import cv2
import time
from ultralytics import YOLO
from event_manager import gestisci_evento
from security.encryptor import cifra_evento
from server_client import invia_file_al_server
from security.encryptor import cifra_immagine


# --- Inizializzazione del sistema ---
print("Avvio Cyber-Vision Guard...")

# Modello YOLO per verifica AI
model = YOLO("yolov8n.pt")
model.overrides['verbose'] = False  # Disattiva log nel terminale

# Apertura webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Errore: impossibile aprire la webcam.")
    exit()

# Lettura primo frame per Motion Detection
ret, frame_precedente = cap.read()
if not ret:
    print("Errore: impossibile leggere il primo frame.")
    exit()

frame_precedente = cv2.cvtColor(frame_precedente, cv2.COLOR_BGR2GRAY)

print("Sistema inizializzato correttamente. Premi 'q' per uscire.")

while True:
    ret, frame_corrente = cap.read()
    if not ret:
        break

    # ---  Motion Detection ---
    frame_grigio = cv2.cvtColor(frame_corrente, cv2.COLOR_BGR2GRAY)
    differenza = cv2.absdiff(frame_precedente, frame_grigio)
    _, soglia = cv2.threshold(differenza, 30, 255, cv2.THRESH_BINARY)
    soglia = cv2.GaussianBlur(soglia, (5, 5), 0)
    contorni, _ = cv2.findContours(soglia, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movimento_rilevato = False
    for contorno in contorni:
        area = cv2.contourArea(contorno)
        if area > 800:
            movimento_rilevato = True
            (x, y, w, h) = cv2.boundingRect(contorno)
            cv2.rectangle(frame_corrente, (x, y), (x + w, y + h), (0, 255, 0), 2)

    persona_rilevata = False

    # --- Se c'è movimento, attiva YOLO ---
    if movimento_rilevato:
        results = model(frame_corrente, verbose=False)
        for box in results[0].boxes:
            cls = int(box.cls[0])
            label = results[0].names[cls]
            conf = float(box.conf[0])

            if label == "person" and conf > 0.5:
                persona_rilevata = True
                (x1, y1, x2, y2) = box.xyxy[0]
                cv2.rectangle(frame_corrente, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                cv2.putText(frame_corrente, f"Persona {conf:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # --- Gestione eventi intelligenti ---
    evento = gestisci_evento(persona_rilevata)
    if evento:
        print(f"🧾 Nuovo evento registrato: {evento}")
        firma = cifra_evento(evento)

        # --- 📸 Salva uno screenshot del momento dell'evento ---
        os.makedirs("frames", exist_ok=True)
        screenshot_path = f"frames/screenshot_{int(time.time())}.jpg"
        cv2.imwrite(screenshot_path, frame_corrente)
        immagine_cifrata = cifra_immagine(screenshot_path)
        print(f"📸 Screenshot salvato in {screenshot_path}")

        # --- 🔐 Invio log + screenshot al server ---
        ultimo_file = sorted(os.listdir("logs"))[-1]  # prende l'ultimo log creato
        percorso_log = os.path.join("logs", ultimo_file)
        invia_file_al_server(percorso_log, immagine_cifrata)

    # --- 3️⃣ Mostra stato sullo schermo ---
    if persona_rilevata:
        stato = "⚠️ PERSONA IN MOVIMENTO RILEVATA ⚠️"
        colore = (0, 0, 255)
    elif movimento_rilevato:
        stato = "Movimento rilevato (in analisi...)"
        colore = (0, 255, 255)
    else:
        stato = "Nessun movimento"
        colore = (255, 255, 255)

    cv2.putText(frame_corrente, stato, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, colore, 2)

    # --- Aggiorna frame precedente e mostra ---
    frame_precedente = frame_grigio.copy()
    cv2.imshow("Cyber-Vision Guard - Motion + AI", frame_corrente)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Sistema arrestato correttamente.")