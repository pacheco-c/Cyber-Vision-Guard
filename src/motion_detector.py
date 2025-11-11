import cv2
import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Errore: impossibile aprire la webcam.")
    exit()

ret, frame_precedente = cap.read()
if not ret:
    print("Errore: impossibile leggere il primo frame.")
    exit()

frame_precedente = cv2.cvtColor(frame_precedente, cv2.COLOR_BGR2GRAY)

ultimo_alert = 0
durata_movimento = 0
SOGLIA_TEMPO = 0.5
COOLDOWN = 4

while True:
    ret, frame_corrente = cap.read()
    if not ret:
        break

    frame_grigio = cv2.cvtColor(frame_corrente, cv2.COLOR_BGR2GRAY)
    differenza = cv2.absdiff(frame_precedente, frame_grigio)
    _, soglia = cv2.threshold(differenza, 60, 255, cv2.THRESH_BINARY)
    soglia = cv2.GaussianBlur(soglia, (5, 5), 0)

    # --- Rilevo le differenze ---
    contorni, _ = cv2.findContours(soglia, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movimento_rilevato = False 

   
    for contorno in contorni:
        area = cv2.contourArea(contorno)   #calcolo l'area
        if area > 3500:  
            movimento_rilevato = True
            (x, y, w, h) = cv2.boundingRect(contorno)  # rettangolo di bounding
            cv2.rectangle(frame_corrente, (x, y), (x + w, y + h), (0, 255, 0), 2)

    
    cv2.imshow("Cyber-Vision Guard - Motion Detection", frame_corrente)

    


    tempo_attuale = time.time()

    if movimento_rilevato:
        durata_movimento += 1/30
        if durata_movimento > SOGLIA_TEMPO and (tempo_attuale - ultimo_alert > COOLDOWN):
            print(f"Movimento rilevato alle {time.strftime('%H:%M:%S')}")
            ultimo_alert = tempo_attuale
            durata_movimento = 0
    else:
        durata_movimento = 0

    frame_precedente = frame_grigio.copy()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()