"""
PROYECTO FINAL: ASISTENTE VIRTUAL NEURO-SIMBÓLICO
Módulo: Modelos de Inteligencia Artificial
=============================================================================
FASE 4: SALIDA DE VOZ (TEXT-TO-SPEECH)

Este módulo utiliza pyttsx3 para convertir la resolución del Sistema Experto
en audio a través de los altavoces del sistema.
"""

import pyttsx3 # Librería que permite síntesis de voz de forma OFFLINE (sin internet).

def hablar_resolucion(texto):
    """
    SINTETIZADOR DE VOZ
    Configura el motor de audio y reproduce el mensaje final.
    """
    # Verificación de seguridad: si no hay texto, no intentamos hablar para evitar errores.
    if not texto:
        return

    # 1. Inicializar el motor
    # pyttsx3 es mejor que gTTS aquí porque no tiene latencia 
    # de red y permite cambiar voces del sistema local
    engine = pyttsx3.init()

    # 2. Configuración de parámetros
    # El 'rate' define la velocidad. 150 es el estándar para una locución clara.
    engine.setProperty('rate', 150)
    
    # 3. Selección de idioma (Lógica de filtrado)
    # Obtenemos la lista de voces instaladas en el sistema operativo del usuario.
    voices = engine.getProperty('voices')
    for voice in voices:
        # Buscamos en el nombre o ID de la voz etiquetas que indiquen español ('spanish' o 'es').
        if "spanish" in voice.name.lower() or "ES" in voice.id:
            engine.setProperty('voice', voice.id)
            break # En cuanto encontramos la primera voz en español, la fijamos y salimos del bucle.

    print(f"🔊 Reproduciendo audio: '{texto}'")
    
    # 4. Ejecución
    engine.say(texto) # Añade el texto a la cola de reproducción.
    
    # PASO CRÍTICO: 'runAndWait' bloquea el hilo de ejecución.
    # Se usa para que el programa NO continúe al menú 
    # principal hasta que el asistente termine de hablar.
    engine.runAndWait() 

# --- PRUEBA INDEPENDIENTE ---
if __name__ == "__main__":
    # Bloque de test unitario para verificar que los altavoces y el motor funcionan.
    hablar_resolucion("Prueba de audio del sistema experto completada con éxito.")