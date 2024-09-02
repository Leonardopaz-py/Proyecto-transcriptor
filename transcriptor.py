import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from pydub import AudioSegment
import speech_recognition as sr
import os

def convertir_a_wav(archivo_ogg, archivo_wav): #Converti audio a wav
    sonido = AudioSegment.from_file(archivo_ogg, format="ogg")
    sonido.export(archivo_wav, format="wav")

def transcribir_audio(archivo_audio):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(archivo_audio) as source:
            audio = recognizer.record(source)
        texto = recognizer.recognize_google(audio, language='es-ES')
        return texto
    except sr.UnknownValueError:
        return "No se pudo entender el audio."
    except sr.RequestError as e:
        return f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}"
    except Exception as e:
        return f"Ha ocurrido un error: {e}"

def procesar_archivos(lista_archivos_ogg):
    transcripciones = []
    carpeta_salida = os.path.join(os.path.expanduser("~"), "Desktop", "Transcripciones")
    os.makedirs(carpeta_salida, exist_ok=True)
    
    for archivo_ogg in lista_archivos_ogg:
        nombre_archivo = os.path.basename(archivo_ogg)
        nombre_sin_extension, _ = os.path.splitext(nombre_archivo)
        archivo_wav = os.path.join(carpeta_salida, nombre_sin_extension + ".wav")
        
        convertir_a_wav(archivo_ogg, archivo_wav)
        texto_transcrito = transcribir_audio(archivo_wav)
        transcripciones.append(f"Transcripción de {nombre_archivo}:\n{texto_transcrito}\n")
        
    # Guardar las transcripciones en un archivo .txt
    archivo_salida = os.path.join(carpeta_salida, "transcripciones.txt")
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.writelines(transcripciones)
    
    return archivo_salida

def on_drop(event):
    archivos = event.data.strip().split()
    if archivos:
        archivos_ogg = [f.replace('{', '').replace('}', '') for f in archivos]
        archivo_txt = procesar_archivos(archivos_ogg)
        lbl_resultado.config(text=f"Transcripciones guardadas en: {archivo_txt}")

def abrir_archivos():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos OGG", "*.ogg")])
    if archivos:
        archivo_txt = procesar_archivos(archivos)
        lbl_resultado.config(text=f"Transcripciones guardadas en: {archivo_txt}")

# Crear la ventana principal
root = TkinterDnD.Tk()
root.title("Transcriptor de Audio")

# Configurar la interfaz
lbl_instrucciones = tk.Label(root, text="Arrastra y suelta archivos de audio aquí\nO usa el botón para seleccionar archivos")
lbl_instrucciones.pack(pady=10, padx=10)

# Configurar el área de arrastrar y soltar
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Botón para abrir archivos
btn_abrir = tk.Button(root, text="Seleccionar archivos", command=abrir_archivos)
btn_abrir.pack(pady=10)

# Etiqueta para mostrar el resultado
lbl_resultado = tk.Label(root, text="")
lbl_resultado.pack(pady=10, padx=10)

# Ejecutar la aplicación
root.mainloop()