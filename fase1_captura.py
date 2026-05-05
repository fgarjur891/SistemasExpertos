"""
PROYECTO FINAL: ASISTENTE VIRTUAL NEURO-SIMBÓLICO
Módulo: Modelos de Inteligencia Artificial
=============================================================================
FASE 1: CAPTURA DE VOZ (SIMULADA) Y PREPROCESAMIENTO DE TEXTO (NLP)
=============================================================================
"""

import speech_recognition as sr
import re
import unicodedata
import random  

# --- CONFIGURACIÓN DE PRUEBAS RÁPIDAS ---
# Lista de 25 frases para simular diferentes estados del cliente y categorías
FRASES_PRUEBA = [
    "Mi pedido llegó completamente roto y la caja estaba abierta, exijo una solución inmediata.",
    "Llevo esperando mi paquete más de una semana y nadie me da una respuesta clara.",
    "¿Podrían decirme cuál es su horario de atención al cliente para mañana?",
    "Me han cobrado dos veces el mismo producto en mi tarjeta de crédito.",
    "Hola, quería saber si tienen stock de la nueva pantalla para portátiles.",
    "El servicio técnico ha sido excelente y el agente muy amable, muchas gracias.",
    "Estoy muy decepcionado con la calidad del producto recibido, no es lo que esperaba.",
    "Quiero poner una reclamación formal porque el envío ha sido un desastre total.",
    "¿Dónde puedo encontrar la dirección física de su oficina central?",
    "Me gustaría cancelar mi suscripción porque ya no necesito el servicio.",
    "La pantalla tiene un defecto de fábrica y se apaga sola constantemente.",
    "Increíble atención, resolvieron mi problema en menos de cinco minutos.",
    "El mensajero fue muy grosero y además dejó el paquete en la lluvia.",
    "¿Tienen algún descuento disponible para compras por volumen?",
    "No reconozco este cargo de cincuenta euros en mi última factura.",
    "¡Qué maravilla de producto! Ha superado todas mis expectativas.",
    "He recibido un artículo que no es el que yo compré, esto es un error grave.",
    "Por favor, necesito cambiar mi dirección de entrega antes de que salga el envío.",
    "El software no funciona y me urge terminar un trabajo, denme una solución.",
    "Muchas gracias por la rapidez, sois los mejores del sector.",
    "Llevo tres días intentando contactar por teléfono y siempre estáis comunicando.",
    "¿Me pueden enviar el manual de instrucciones en PDF a mi correo?",
    "La batería del dispositivo no dura ni una hora, creo que está averiado.",
    "Me encanta cómo habéis gestionado mi devolución, un diez para el equipo.",
    "He visto un error en los datos de mi perfil y no puedo editarlos yo mismo."
]

def limpieza_profesional(texto, quitar_numeros=True, quitar_acentos=True):
    """
    PREPROCESAMIENTO DE TEXTO (NLP)
    OJO: Esto no es solo estética. Los Transformers son sensibles al ruido.
    Normalizar aquí reduce el vocabulario que el modelo debe procesar.
    Prepara la frase para que el modelo Transformer pueda analizarla sin ruido.
    """
    print("Log: Iniciando limpieza profesional del texto...")
    # 1. Minúsculas: Evita que 'Pedido' y 'pedido' se traten como tokens distintos[cite: 17].
    texto = texto.lower()

    # 2. Normalización Unicode: Descomponemos caracteres (á -> a + ´) y quitamos la marca 'Mn' (Nonspacing Mark)
    # Es más eficiente que usar un .replace() por cada vocal.
    if quitar_acentos:
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                        if unicodedata.category(c) != 'Mn')

    # 3. Regex para números: En este sistema experto, los números (como IDs de pedido) 
    # no definen el sentimiento, así que los quitamos para limpiar el mensaje.
    if quitar_numeros:
        texto = re.sub(r'\d+', '', texto)

    # 4. Limpieza de símbolos: '[^\w\s]' quita todo lo que no sea letra o espacio.
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # 5. Tokenización básica: .split() y .join() eliminan espacios triples o raros.
    texto = " ".join(texto.split())

    return texto

def obtener_entrada_cliente(modo_simulado):
    """
    CAPTURA DE ENTRADA
    Permite alternar entre captura real por micrófono o selección aleatoria 
    de frases de prueba para agilizar el desarrollo.
    """
    if modo_simulado:
        print("\n--- MODO SIMULACIÓN ACTIVO ---")
        # Escogemos una frase al azar de nuestra lista de 25 casos de ejemplo
        texto_crudo = random.choice(FRASES_PRUEBA)
        print(f"Simulando entrada de voz: '{texto_crudo}'")
    else:
        # --- CÓDIGO DE MICRÓFONO  ---
        r = sr.Recognizer()
        print("\n--- SISTEMA DE CAPTURA DE AUDIO REAL ---")
        lista_mics = sr.Microphone.list_microphone_names()
        for indice, nombre in enumerate(lista_mics):
            print(f"[{indice}] - {nombre}")

        try:
            NUM_MIC = int(input("\nEscribe el NÚMERO del micrófono a usar: "))
            mic = sr.Microphone(device_index=NUM_MIC)
            with mic as source:
                print("Calibrando ruido... ")
                r.adjust_for_ambient_noise(source, duration=1)
                print("\n🎙️ HABLE AHORA...")
                audio = r.listen(source)
            texto_crudo = r.recognize_google(audio, language='es-ES')
        except Exception as e:
            print(f"Error en captura real: {e}")
            return None

    # Procesamiento común (limpieza) para ambos modos 
    texto_limpio = limpieza_profesional(texto_crudo)
    print(f"> Texto listo para PLN: '{texto_limpio}'")
    return texto_limpio

# ==========================================
# PUNTO DE PRUEBA DE LA FASE 1
# ==========================================
if __name__ == "__main__":
    # Ejecutamos en modo simulado para no perder tiempo con el micrófono
    resultado = obtener_entrada_cliente(True)
