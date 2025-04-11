# 🎧 Interfaz Interactiva para Aplicación de Filtros a Audio

Este proyecto proporciona una interfaz gráfica hecha con [Gradio](https://www.gradio.app/) que permite cargar un archivo de audio y aplicar filtros digitales como **pasa-bajas**, **pasa-altas** o **pasa-banda**, así como visualizar la señal en el dominio del tiempo y en el dominio de la frecuencia (Transformada de Fourier).

---

## 🚀 ¿Qué hace este código?

- Carga un archivo de audio `.wav`.
- Permite elegir un tipo de filtro: `lowpass`, `highpass` o `bandpass`.
- Permite definir las frecuencias de corte.
- Aplica el filtro a la señal.
- Muestra:
  - Señal original
  - Señal filtrada
  - Transformada de Fourier de ambas (opcional)
- Descarga el audio resultante.
- Todo esto, de forma interactiva usando una interfaz gráfica amigable con Gradio.

---

## 📦 Librerías utilizadas

| Librería      | Función Principal |
|---------------|-------------------|
| `gradio`      | Crear la interfaz gráfica interactiva. |
| `librosa`     | Cargar y analizar señales de audio. |
| `matplotlib`  | Graficar señales en el dominio del tiempo y la frecuencia. |
| `numpy`       | Operaciones matemáticas sobre señales. |
| `soundfile`   | Guardar señales de audio como archivos `.wav`. |
| `scipy.signal`| Aplicar filtros digitales con `butter` y `lfilter`. |
| `tempfile`    | Crear archivos temporales para las gráficas y audios. |

---

## 🧠 Estructura del código

### 1. `apply_filter`
Aplica un filtro digital Butterworth (pasa-bajas, pasa-altas o pasa-banda) a la señal.

### 2. `plot_signal`
Grafica la señal en el dominio del tiempo con `librosa.display.waveshow`.

### 3. `plot_fourier`
Calcula y grafica la Transformada de Fourier usando `numpy.fft`.

### 4. `save_audio`
Guarda la señal filtrada como archivo `.wav`.

### 5. `process_audio`
Función que integra todo el flujo: carga, filtra, grafica y devuelve resultados.

---

## 🖼 Interfaz con Gradio

La interfaz fue creada usando `gr.Blocks` e incluye:

- **Carga de audio** con `gr.Audio`.
- **Selección de filtros** con `gr.Dropdown`.
- **Ajuste de frecuencias** con `gr.Slider`.
- **Checkboxes** para activar visualización de FFT.
- **Botón** para procesar la señal.
- **Gráficas** con `gr.Image`.
- **Reproducción y descarga** del audio filtrado.

---

## 🖥️ Descripción de la Interfaz Gráfica

La interfaz está dividida en secciones bien definidas, con elementos visuales e interactivos para una experiencia fluida:

### 🎵 Carga y Reproducción de Audio
- **Botón para cargar archivo `.wav`**: permite subir un archivo de audio desde tu dispositivo.
- **Reproductor de audio original**: con controles de reproducción, volumen y velocidad de reproducción.
- **Reproductor de audio filtrado**: muestra cómo suena el audio después de aplicar el filtro seleccionado.

### 🎚️ Controles de Filtro
- **Dropdown “Tipo de filtro”**: opciones como `lowpass`, `highpass`, `bandpass`.
- **Slider “Frecuencia de corte”**: permite ajustar la frecuencia en Hz para los filtros pasa bajos o pasa altos (o frecuencias límite en caso de banda).
- **Checkboxes**:
  - `Mostrar Transformada de Fourier (Original)`
  - `Mostrar Transformada de Fourier (Filtrada)`

### ⚙️ Botón de acción
- **Aplicar Filtro**: ejecuta todo el proceso de filtrado, visualización y generación del nuevo audio.

### 📊 Visualización de señales
- **Gráfica de “Señal Original”**:
  - Muestra la amplitud de la señal a lo largo del tiempo.
  - Eje X: Tiempo (s), Eje Y: Amplitud.
- **Gráfica de “Señal Filtrada”**:
  - Visualiza el resultado tras aplicar el filtro seleccionado.
  - Comparativa clara con la señal original.
- Ambas gráficas permiten **zoom** y **descarga** de la imagen generada.

---

## 🖼 Interfaz Gráfica
![image](https://github.com/user-attachments/assets/0921b45f-b8c5-4b61-89e7-95aa8b192a50)
![image](https://github.com/user-attachments/assets/6d287345-ab9b-4397-a80b-4d66c65bd404)

---

## 🧪 Instrucciones para clonar y correr el repositorio

Para correr el archivo principal `FILTROS.py`, asegúrate de tener tu entorno virtual activado (si estás usando uno) y que todas las dependencias estén instaladas.

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

#### 2.1 Crear el entorno virtual
Para crear un entorno virtual, ejecuta el siguiente comando en la terminal:
```bash
python3 -m venv venv
```
Este comando crea una carpeta llamada venv, que contiene el entorno virtual para tu proyecto.

#### 2.2 Activar el entorno virtual
Para activar el entorno virtual, dependiendo de tu sistema operativo, ejecuta uno de los siguientes comandos:
```bash
source hsiv/bin/activate  # En Linux/Mac
.\hsiv\Scripts\activate   # En Windows
```
Cuando el entorno virtual está activado, verás algo como (venv) al inicio de la línea en tu terminal.

### 3. Instalar dependencias

#### 3.1 Instalar toml y black
Ejecuta los siguientes comandos para instalar las dependencias:
```bash
pip install toml
pip install black
```
- toml es necesario si tu proyecto utiliza un archivo .toml de configuración.
- black es un formateador de código, y lo usaremos para limitar el largo de las líneas en el código a 79 caracteres.

### 4. Formatear el código con Black
Una vez que hayas configurado el archivo pyproject.toml para ajustar la longitud de las líneas, puedes proceder a formatear tu código con Black para asegurarte de que todas las líneas de código se ajusten a los 79 caracteres establecidos. Esto garantizará que tu proyecto mantenga un estilo consistente y conforme a las buenas prácticas de PEP-8. Para formatear el código, simplemente ejecuta el siguiente comando desde la terminal en la raíz de tu proyecto:
Para formatear tu código, simplemente ejecuta:
```bash
black .
```
### 5. Evitar conflicto con Flask
Si tu proyecto utiliza Flask, por ejemplo, si tienes un archivo como app.py o __init__.py que define la configuración de tu aplicación, Black no debería causar ningún conflicto directo con la lógica de Flask. Black simplemente formatea el código para mejorar su legibilidad y mantener la consistencia del estilo, sin modificar la lógica subyacente de la aplicación. Sin embargo, debes tener cuidado de no modificar de forma involuntaria archivos que tienen una estructura o indentación crucial para Flask, como el archivo __init__.py o cualquier archivo de configuración que dependa de una indentación específica para el funcionamiento de la aplicación. Asegúrate de revisar el código después de formatearlo para verificar que no haya cambios no deseados en la lógica del proyecto.

### 6. Correr el archivo Python
Finalmente, una vez que hayas configurado todo y formateado tu código, puedes ejecutar tu archivo Python. En este caso, ejecutarás el archivo Filtros.py.
Ejecuta el siguiente comando para correr el archivo:
```bash
python3 Filtros.py
```
Este comando ejecutará el script Filtros.py con Python 3.
