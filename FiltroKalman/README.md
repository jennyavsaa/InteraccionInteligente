# 🏀 Seguimiento de Pelotas con Filtro de Kalman + YOLOv8

Este proyecto implementa un sistema de seguimiento de objetos (pelotas) en video utilizando el modelo de detección **YOLOv8** junto con un **Filtro de Kalman lineal** para el rastreo temporal de cada objeto detectado.

---

## 🚀 ¿Qué hace este código?

- Detecta pelotas en movimiento usando YOLOv8.
- Asigna un Filtro de Kalman a cada objeto detectado.
- Realiza el seguimiento de su trayectoria incluso con detecciones intermitentes.
- Visualiza el seguimiento con identificadores y colores únicos.
- Utiliza intersección sobre unión (IoU) para asociar detecciones con predicciones.

---

## 📦 Librerías utilizadas

| Librería       | Función Principal |
|----------------|-------------------|
| `opencv-python`| Procesamiento de video y visualización de resultados. |
| `ultralytics`  | Modelo YOLOv8 para detección de objetos. |
| `numpy`        | Manipulación de vectores y matrices del filtro. |

---

## 🧠 Estructura del código

### `KalmanFilter`
Clase personalizada que implementa el filtro de Kalman con:
- Estado: posición y velocidad en 2D (`[x, y, vx, vy]`)
- Matrices de transición `F`, observación `H`, covarianza `P`, ruido `Q` y `R`
- Funciones: `predict()` y `update()`

### `Track`
Clase auxiliar que representa cada pelota detectada, junto con su identificador, filtro de Kalman, color y contador de frames sin actualizar.

### `match_detections_to_tracks`
Asocia cada nueva detección con un track existente, usando una métrica de **IoU** y un umbral configurable.

### `main()`
Función principal que:
- Carga un video o webcam
- Detecta objetos con YOLOv8
- Actualiza los trackers con Kalman
- Dibuja bounding boxes e identificadores únicos por objeto

---

## 🔁 Lógica del Filtro de Kalman

### Modelo de Estado

El filtro utiliza un modelo de 4 dimensiones:
\[
\mathbf{x} = [x, y, \dot{x}, \dot{y}]^T
\]

### Matriz de transición:

\[
F =
\begin{bmatrix}
1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
\]

### Matriz de observación:

\[
H =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
\end{bmatrix}
\]

---

## 🖼 Visualización

- Cada pelota se visualiza con un color diferente y un número de ID.
- Los tracks persisten incluso si una detección falla por algunos frames.
- Se pueden observar líneas de trayectoria o posiciones previas fácilmente.

---

## 🧪 Instrucciones para correr el proyecto

### 1. Clonar el repositorio
Primero, necesitas clonar el repositorio en tu máquina local. Para hacerlo, abre tu terminal y ejecuta el siguiente comando:
```bash
git clone https://github.com/jennyavsaa/InteraccionInteligente.git
```

Esto descargará el repositorio en tu computadora y creará una carpeta llamada InteraccionInteligente. Después, navega a esa carpeta:
```bash
cd InteraccionInteligente
```
### 2. Crear y activar un entorno virtual (opcional, pero recomendado)
Para evitar conflictos con otras librerías de tu sistema, es recomendable usar un entorno virtual. Esto mantendrá todas las dependencias necesarias para este proyecto aisladas.
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
.\venv\Scripts\activate   # En Windows
```

### 3. Correr el archivo Python
Finalmente, una vez que hayas configurado todo y formateado tu código, puedes ejecutar tu archivo Python. En este caso, ejecutarás el archivo Filtros.py.
Ejecuta el siguiente comando para correr el archivo:
```bash
python3 seg_pelota.py
```
Este comando ejecutará el script seg_pelota.py con Python 3.