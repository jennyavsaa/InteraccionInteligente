"""Interfaz interactiva con Gradio para aplicar filtros a audios."""

import tempfile

import gradio as gr
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter


def apply_filter(audio, sr, filter_type, cutoff_low, cutoff_high=None):
    """
    Aplica un filtro pasa-bajas, pasa-altas o pasa-banda a una señal de audio.

    Parámetros:
        audio (np.ndarray): Señal de audio.
        sr (int): Frecuencia de muestreo.
        filter_type (str): Tipo de filtro ("lowpass", "highpass" o "bandpass").
        cutoff_low (float): Frecuencia de corte baja.
        cutoff_high (float, opcional): Frecuencia de corte alta (pasa-banda).

    Retorna:
        np.ndarray: Señal de audio filtrada.
    """
    nyquist = 0.5 * sr
    if filter_type == "lowpass":
        normal_cutoff = cutoff_low / nyquist
        b, a = butter(5, normal_cutoff, btype="low", analog=False)
    elif filter_type == "highpass":
        normal_cutoff = cutoff_low / nyquist
        b, a = butter(5, normal_cutoff, btype="high", analog=False)
    elif filter_type == "bandpass":
        low = cutoff_low / nyquist
        high = cutoff_high / nyquist
        b, a = butter(5, [low, high], btype="band")

    filtered_audio = lfilter(b, a, audio)
    return filtered_audio


def save_plot(fig):
    """
    Guarda una figura de Matplotlib en un archivo temporal .png.

    Parámetros:
        fig (matplotlib.figure.Figure): Figura a guardar.

    Retorna:
        str: Ruta del archivo de imagen guardado.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(temp_file.name)
    plt.close(fig)
    return temp_file.name


def plot_signal(audio, sr, title="Signal"):
    """
    Genera y guarda una gráfica de la señal de audio.

    Parámetros:
        audio (np.ndarray): Señal de audio.
        sr (int): Frecuencia de muestreo.
        title (str): Título de la gráfica.

    Retorna:
        str: Ruta de la imagen generada.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.waveshow(audio, sr=sr, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")
    return save_plot(fig)


def plot_fourier(audio, sr):
    """
    Genera y guarda la gráfica de la Transformada de Fourier de una señal.

    Parámetros:
        audio (np.ndarray): Señal de audio.
        sr (int): Frecuencia de muestreo.

    Retorna:
        str: Ruta de la imagen generada.
    """
    fft_audio = np.fft.fft(audio)
    fft_freqs = np.fft.fftfreq(len(fft_audio), 1 / sr)
    fft_magnitude = np.abs(fft_audio)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        fft_freqs[: len(fft_freqs) // 2],
        fft_magnitude[: len(fft_magnitude) // 2],
    )
    ax.set_title("Transformada de Fourier")
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud")
    return save_plot(fig)


def save_audio(audio, sr):
    """
    Guarda una señal de audio en un archivo temporal .wav.

    Parámetros:
        audio (np.ndarray): Señal de audio.
        sr (int): Frecuencia de muestreo.

    Retorna:
        str: Ruta del archivo .wav generado.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio, sr)
    return temp_file.name


def process_audio(
    audio_path,
    filter_type,
    cutoff_low,
    cutoff_high,
    fft_checkbox,
    fft_filtered_checkbox,
):
    """
    Procesa archivo de audio; aplica filtro, grafica y la trans de Fourier.

    Parámetros:
        audio_path (str): Ruta del archivo de audio.
        filter_type (str): Tipo de filtro a aplicar.
        cutoff_low (float): Frecuencia de corte baja.
        cutoff_high (float): Frecuencia de corte alta (solo para pasa-banda).
        fft_checkbox (bool)|: Si se debe graficar la FFT original.
        fft_filtered_checkbox (bool): Si debe graficar FFT de señal filtrada.

    Retorna:
        tuple: Rutas de las imágenes generadas y el audio filtrado.
    """
    audio, sr = librosa.load(audio_path, sr=None, mono=True)
    original_plot = plot_signal(audio, sr, title="Señal Original")
    filtered_audio = apply_filter(
        audio, sr, filter_type, cutoff_low, cutoff_high
    )
    filtered_plot = plot_signal(
        filtered_audio, sr, title=f"Señal Filtrada ({filter_type})"
    )
    fourier_plot = None
    if fft_checkbox:
        fourier_plot = plot_fourier(audio, sr)
    fourier_filtered_plot = None
    if fft_filtered_checkbox:
        fourier_filtered_plot = plot_fourier(filtered_audio, sr)
    filtered_audio_path = save_audio(filtered_audio, sr)

    return (
        original_plot,
        filtered_plot,
        fourier_plot,
        fourier_filtered_plot,
        filtered_audio_path,
    )


# Construcción de la interfaz gráfica con Gradio
with gr.Blocks() as demo:
    with gr.Row():
        audio_input = gr.Audio(
            label="Cargar archivo de audio (.wav)", type="filepath"
        )
        processed_audio_output = gr.Audio(label="Audio Filtrado")
        filter_type = gr.Dropdown(
            choices=["lowpass", "highpass", "bandpass"],
            label="Tipo de filtro",
            value="lowpass",
        )
        cutoff_low = gr.Slider(
            minimum=100,
            maximum=8000,
            step=100,
            label="Frecuencia de corte baja",
        )
        cutoff_high = gr.Slider(
            minimum=100,
            maximum=8000,
            step=100,
            label="Frecuencia de corte alta (solo para pasa-banda)",
            visible=False,
        )

    def update_cutoff_high_visibility(filter_choice):
        """Actualiza visibilidad de control de frecuencia alta segun filtro."""
        return gr.update(visible=(filter_choice == "bandpass"))

    filter_type.change(
        fn=update_cutoff_high_visibility,
        inputs=filter_type,
        outputs=cutoff_high,
    )

    with gr.Row():
        fft_checkbox = gr.Checkbox(
            label="Mostrar Transformada de Fourier (Original)", value=False
        )
        fft_filtered_checkbox = gr.Checkbox(
            label="Mostrar Transformada de Fourier (Filtrada)", value=False
        )

    filter_btn = gr.Button("Aplicar Filtro")

    with gr.Row():
        original_signal_plot = gr.Image(label="Señal Original")
        filtered_signal_plot = gr.Image(label="Señal Filtrada")
    with gr.Row():
        fourier_signal_plot = gr.Image(
            label="Transformada de Fourier (Original)", visible=False
        )
        fourier_filtered_signal_plot = gr.Image(
            label="Transformada de Fourier (Filtrada)", visible=False
        )

    filter_btn.click(
        process_audio,
        inputs=[
            audio_input,
            filter_type,
            cutoff_low,
            cutoff_high,
            fft_checkbox,
            fft_filtered_checkbox,
        ],
        outputs=[
            original_signal_plot,
            filtered_signal_plot,
            fourier_signal_plot,
            fourier_filtered_signal_plot,
            processed_audio_output,
        ],
    )

    fft_checkbox.change(
        fn=lambda fft: gr.update(visible=fft),
        inputs=fft_checkbox,
        outputs=fourier_signal_plot,
    )
    fft_filtered_checkbox.change(
        fn=lambda fft: gr.update(visible=fft),
        inputs=fft_filtered_checkbox,
        outputs=fourier_filtered_signal_plot,
    )

# Ejecutar app de Gradio
demo.launch()
