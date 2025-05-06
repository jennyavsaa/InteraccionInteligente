import cv2
import torch
import numpy as np
from ultralytics import YOLO
from filterpy.kalman import KalmanFilter
import random

# Clase para cada objeto seguido (cada pelota)
class KalmanTracker:
    count = 0

    def __init__(self, bbox):
        # Crear un filtro de Kalman simple (x, y, dx, dy)
        print("ANDO EN KALMAAAAAAAAAAAAAAAAAAAN")
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        self.kf.F = np.array([[1, 0, 1, 0],
                              [0, 1, 0, 1],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        self.kf.H = np.array([[1, 0, 0, 0],
                              [0, 1, 0, 0]])
        self.kf.R *= 70  # Ruido de medición, más confianza a YOLOs
        self.kf.P *= 1000  # Incertidumbre inicial
        self.kf.Q *= 0.1  # Ruido del proceso,  adpatación a cambios

        x, y = self.get_center(bbox)
        self.kf.x[:2] = np.array([[x], [y]])

        self.id = KalmanTracker.count
        KalmanTracker.count += 1
        self.age = 0
        self.time_since_update = 0
        self.history = []

        # Asignar un color único al objeto (pelota)
        self.color = [random.randint(0, 255) for _ in range(3)]  # Color aleatorio

    def update(self, bbox):
        x, y = self.get_center(bbox)
        self.kf.update(np.array([[x], [y]]))
        self.time_since_update = 0
        self.history.append((x, y))

    def predict(self):
        self.kf.predict()
        self.age += 1
        self.time_since_update += 1
        x, y = self.kf.x[0], self.kf.x[1]
        return int(x), int(y)

    @staticmethod
    def get_center(bbox):
        x1, y1, x2, y2 = bbox
        return int((x1 + x2) / 2), int((y1 + y2) / 2)
device = torch.device('cpu')
model = YOLO("yolov8m.pt").to(device)
cap = cv2.VideoCapture("pelota3.webm")  # AQUI CAMBIA ARCHIVO 

trackers = []
# print("FPS del video:", cap.get(cv2.CAP_PROP_FPS))

def iou(bbox1, bbox2): # Calcula la Intersección sobre la Unión 
    x1, y1, x2, y2 = bbox1
    x1_p, y1_p, x2_p, y2_p = bbox2

    xi1 = max(x1, x1_p)
    yi1 = max(y1, y1_p)
    xi2 = min(x2, x2_p)
    yi2 = min(y2, y2_p)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    bbox1_area = (x2 - x1) * (y2 - y1)
    bbox2_area = (x2_p - x1_p) * (y2_p - y1_p)

    union = bbox1_area + bbox2_area - inter_area
    return inter_area / union if union > 0 else 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    detections = []
    results = model(frame)[0]

    for r in results.boxes:
        class_id = int(r.cls[0])
        conf = float(r.conf[0])
        if conf < 0.8 or class_id != 32:  # CAMBIA CONFIANZA O ID
            continue

        x1, y1, x2, y2 = map(int, r.xyxy[0])  # Coordenadas de la caja delimitadora del objeto detectado en el formato 
        # Puedes filtrar por clase aquí si sabes cuál es la clase de "pelota"
        detections.append((x1, y1, x2, y2))

    # Actualizar trackers
    updated_ids = set() # ID trackers
    for det in detections:
        best_iou = 0
        best_tracker = None
        for tracker in trackers:
            pred = tracker.predict() # predice su próxima posición
            pred_box = (pred[0]-30, pred[1]-30, pred[0]+30, pred[1]+30) #caja delimitadora alrededor de esa predicción
            i = iou(pred_box, det) # predicción del tracker y la nueva detección con la función 
            
            # IoU más alto hasta el momento, se guarda por más cercano a la detección actual.
            if i > best_iou:
                best_iou = i
                best_tracker = tracker

        if best_iou > 0.05 and best_tracker: # predicción del tracker y la detección es mayor que 0.2
            best_tracker.update(det)
            updated_ids.add(best_tracker.id)
        else:
            new_tracker = KalmanTracker(det)
            trackers.append(new_tracker)

    # Dibujar trackers y trayectorias
    for tracker in trackers:
        x, y = tracker.predict() # Predicción de su próxima posición

        # Dibujar la trayectoria con el color asignado
        for (px, py) in tracker.history: # tracker con tracker history
            cv2.circle(frame, (int(px), int(py)), 2, tracker.color, -1)  # Puntos de trayectoria

        # Dibujar la predicción como un punto de color
        cv2.circle(frame, (x, y), 10, tracker.color, -1)  # Predicción

        if tracker.time_since_update < 10: #no ha sido actualizado recientemente dibuja ID
            cv2.putText(frame, f'ID {tracker.id}', (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Seguimiento de Pelota", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
