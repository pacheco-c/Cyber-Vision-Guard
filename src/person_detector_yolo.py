from ultralytics import YOLO
import cv2

# --- Carica il modello pre-addestrato YOLOv8 (nano = veloce e leggero) ---
model = YOLO("yolov8n.pt")
model.overrides['verbose'] = False  # Disattiva i log nel terminale

# --- Apri la webcam ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Errore: impossibile aprire la webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- Rilevamento persone ---
    results = model(frame, verbose=False)

    # --- Disegna riquadri e nomi degli oggetti rilevati ---
    annotated_frame = results[0].plot()

    # --- Mostra la finestra ---
    cv2.imshow("Cyber-Vision Guard - YOLOv8 Person Detection", annotated_frame)

    # --- Esci con 'q' ---
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()