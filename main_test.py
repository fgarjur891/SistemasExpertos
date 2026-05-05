"""
PROYECTO FINAL: ASISTENTE VIRTUAL NEURO-SIMBÓLICO
Controlador Central con Menú, Historial y Reporte de Sesión
=============================================================================
"""

import random
import time
import winsound
import pyttsx3
import sys

# Importación de mis módulos de fase
from fase1_captura import obtener_entrada_cliente
from fase2_analisis import analizar_incidencia_nlp
from fase3_motor import procesar_con_sistema_experto
from fase4_voz import hablar_resolucion
from fase5_informe import generar_pdf_resumen

# --- CONFIGURACIÓN DE USUARIOS PARA LA SESIÓN  (ejemplos por rapidez)---
USUARIOS = {
    "1": {"nombre": "Ana", "meses": 48},
    "2": {"nombre": "Luis", "meses": 5},
    "3": {"nombre": "Marta", "meses": 12},
    "4": {"nombre": "Pako", "meses": 30},
    "5": {"nombre": "Carlos", "meses": 2}
}

def sonar_bips_llamada():
    # Efecto de audio inicial para el contestador.
    print("\n🔔 [CONECTANDO CON EL CLIENTE...]")
    try:
        winsound.Beep(1000, 300) 
        time.sleep(0.2)
        winsound.Beep(1000, 300)
    except:
        pass
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say("Llamada entrante.")
    engine.runAndWait()

def imprimir_informe_final(historial):
    # Genera un resumen visual de la sesión en consola (Base para el PDF)
    print("\n" + "!"*60)
    print("      INFORME DE SESIÓN - ASISTENTE EXPERTO")
    print("!"*60)
    if not historial:
        print("No se registraron interacciones en esta sesión.")
    else:
        for i, registro in enumerate(historial, 1):
            print(f"\nINTERACCIÓN #{i}")
            print(f"👤 Cliente: {registro['nombre']} ({registro['antiguedad']} meses)")
            print(f"📥 Frase entrada: '{registro['entrada']}'")
            print(f"🧠 Categoría: {registro['categoria'].upper()}")
            print(f"📢 Solución: {registro['solucion']}")
    print("\n" + "!"*60)
    print("Informe generado correctamente. Sesión finalizada.")

def mostrar_menu():
    print("\n" + "="*55)
    print("      CONTESTADOR INTELIGENTE (MOTOR EXPERTO)")
    print("="*55)
    print("1. Modo MANUAL (Usar Micrófono Real)")
    print("2. Modo AUTOMÁTICO (Simular con Frases de Prueba)")
    print("3. GENERAR INFORME DE SESIÓN Y SALIR")
    print("="*55)
    return input("Seleccione una opción: ")

def ejecutar_sistema_completo():
    historial_sesion = [] # Almacén de datos para el reporte final

    while True:
        opcion = mostrar_menu()

        if opcion == "3":
            imprimir_informe_final(historial_sesion)
            generar_pdf_resumen(historial_sesion)
            break
        
        if opcion not in ["1", "2"]:
            print("❌ Opción no válida.")
            continue

        # Selección de cliente para contextualizar el motor experto
        print("\nUsuarios en base de datos: " + ", ".join([f"{k}:{v['nombre']}" for k, v in USUARIOS.items()]))
        id_u = input("Elija el ID del cliente que llama: ")
        if id_u not in USUARIOS:
            print("ID no reconocido. Se procederá como 'Invitado' (Cliente Nuevo).")
            # Opcionalmente podrías poner: continue (para volver a pedirlo)

        cliente = USUARIOS.get(id_u, {"nombre": "Invitado", "meses": 0})
        
        # --- NUEVO: FEEDBACK VISUAL INMEDIATO ---
        print(f"\nCLIENTE: {cliente['nombre']}")
        print(f"ANTIGÜEDAD: {cliente['meses']} meses")
        
        if cliente['meses'] > 24:
            print("PERFIL: Cliente VIP (Elegible para bonificaciones)")
        else:
            print("PERFIL: Cliente Estándar")

        # 0. Efecto de sonido
        sonar_bips_llamada()

        # 1. ENTRADA (Fase 1) - modo_simulado es True si la opción es 2
        es_simulado = (opcion == "2")
        texto_cliente = obtener_entrada_cliente(modo_simulado=es_simulado)

        if texto_cliente:
            # 2. ANÁLISIS NEURONAL (Fase 2)
            datos_nlp = analizar_incidencia_nlp(texto_cliente)

            # 3. SISTEMA EXPERTO (Fase 3)
            respuesta_final = procesar_con_sistema_experto(
                datos_nlp, 
                nombre_cliente=cliente['nombre'], 
                meses=cliente['meses']
            )

            # 4. SALIDA DE VOZ (Fase 4)
            print("\n" + "-"*55)
            print(f"📢 RESPUESTA AL CLIENTE: {respuesta_final}")
            print("-"*55)
            hablar_resolucion(respuesta_final)

            # 5. GUARDAR EN HISTORIAL
            historial_sesion.append({
                "nombre": cliente['nombre'],
                "antiguedad": cliente['meses'],
                "entrada": texto_cliente,
                "categoria": datos_nlp['categoria'],
                "solucion": respuesta_final
            })

if __name__ == "__main__":
    ejecutar_sistema_completo()