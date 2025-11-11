import cv2

# Inizializza la webcam
cap = cv2.VideoCapture(0)

# Inizializza il rilevatore HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ridimensiona per prestazioni migliori
    frame_resized = cv2.resize(frame, (640, 480))

    # Rileva persone
    boxes, weights = hog.detectMultiScale(
        frame_resized,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    # Disegna rettangoli solo se la confidenza è alta
    for i, (x, y, w, h) in enumerate(boxes):
        if weights[i] > 0.6:  # soglia di confidenza
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Cyber-Vision Guard - Person Detector (HOG)", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()