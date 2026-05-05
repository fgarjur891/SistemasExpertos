"""
NOTAS PARA LA DEFENSA:
En esta fase realizamos un "Análisis Híbrido". 
1. Usamos Redes Neuronales (Transformers) para la parte subjetiva: el SENTIMIENTO.
2. Usamos IA Simbólica (Diccionarios jerárquicos) para la parte objetiva: la CATEGORÍA.
Esto garantiza que el sistema entienda el 'qué' (problema) y el 'cómo' (emoción).
"""

# Importamos la herramienta pipeline de Hugging Face.
# El pipeline abstrae la complejidad de tokenización y pesos del modelo.
try:
    from transformers import pipeline
except ImportError:
    print("❌ Error: No se encuentra 'transformers'. Revisa si el venv está activo.")

# --- CARGA DEL MODELO NEURONAL ---
# "XLM-RoBERTa" es un modelo multilingüe (Cross-lingual Language Model).
# Entiende perfectamente el español coloquial de redes sociales y chats.
print("Log: Cargando modelo Transformer (XLM-RoBERTa)...")
try:
    # LABEL_0: Negativo | LABEL_1: Neutral | LABEL_2: Positivo.
    analizador_sentimiento = pipeline(
        "sentiment-analysis", 
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
    )
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    # Nota técnica: protobuf y sentencepiece son necesarios para el tokenizador de RoBERTa.
    print("Sugerencia: Asegúrate de haber instalado 'protobuf', 'sentencepiece' y 'tiktoken'.")

def analizar_incidencia_nlp(texto_limpio):
    """
    Recibe el texto de la Fase 1. Si no hay texto, abortamos para evitar errores.
    """
    if not texto_limpio:
        return None

    # 1. ANÁLISIS DE SENTIMIENTO (IA Probabilística)
    # El modelo devuelve una lista con un diccionario que contiene 'label' y 'score'.
    resultado = analizador_sentimiento(texto_limpio)[0]
    etiqueta = resultado['label'].upper() 
    confianza = resultado['score'] # Es la probabilidad (0.0 a 1.0) de que la etiqueta sea correcta

    # MAPEO DE SENTIMIENTO: Convertimos etiquetas abstractas en valores numéricos (-1 a 1).
    # Hacemos esto para que el Sistema Experto pueda usar operadores matemáticos (< o >).
    valor_sentimiento = 0
    if "0" in etiqueta or "NEG" in etiqueta:
        valor_sentimiento = -confianza # Negativo: representamos el enfado como un valor negativo.
    elif "2" in etiqueta or "POS" in etiqueta:
        valor_sentimiento = confianza  # Positivo: satisfacción del cliente.
    else:
        valor_sentimiento = 0 # Neutral.

    # 2. CATEGORIZACIÓN AMPLIADA (IA Simbólica / Diccionarios)
    texto_min = texto_limpio.lower()
    categoria = "desconocido" # Fallback: si no detectamos nada, el sistema experto derivará a un humano.

    # --- DICCIONARIOS DE INTENCIONES ---
    # ¿Por qué no uso IA también para la categoría?
    # Los diccionarios nos dan control total y evitan alucinaciones en reglas de negocio críticas
    
    # 1. FEEDBACK POSITIVO: Incluye palabras de éxito para detectar satisfacción.
    palabras_feedback = ["gracias", "amable", "excelente", "perfecto", "genial", "contento", "atencion",
                         "increible", "maravilla", "superado", "expectativas", 
                         "recomiendo", "feliz", "solucionado", "rapidez", "eficaz", "estupendo", 
                         "magnifico", "agradecido", "ayudado", "equipo", "profesional", "diez", "encantado"]

    # 2. SAT: Soporte técnico especializado.
    palabras_sat = ["manual", "instrucciones", "fallo", "averia", "tecnico", "software", "error",
                    "configurar", "instalacion", "conexion", "pantalla", "bateria", "hardware", 
                    "dispositivo", "app", "web", "bloqueado", "funciona", "averiado", 
                    "asistencia", "reparar", "ayuden" , "soporte", "guia"]

    # 3. INFORMACIÓN: Consultas generales.
    palabras_info = ["horario", "informacion", "duda", "saber", "donde", "telefono", "stock","ubicacion", 
                     "oficina", "direccion", "contacto", "disponible", "precio", "cuanto", 
                     "abierto", "cerrado", "mañana", "tarde", "web", "email", "correo", 
                     "consulta", "pregunta", "catalogo", "tienda"]

    # 4. FACTURACIÓN: Problemas de dinero (críticos).
    palabras_factura = ["banco", "importe", "euro", "cargo", "duplicado", "cuenta", "credito", "debito", 
                        "transferencia", "recibo", "iva", "descuento", "promocion", "abono", "devolucion", 
                        "pagado", "pendiente","cobro", "dinero", "factura", "pago", "tarjeta", "reembolso"]

    # 5. PRODUCTO: Defectos físicos del artículo.
    palabras_producto = ["estropeado", "malogrado", "defectuoso", "usado", "rayado", "golpe", "abierto", "caja",
                          "pieza", "articulo", "objeto", "insatisfecho", "sucio", 
                          "incorrecto", "calidad", "defecto", "dañado", "incidencia"]

    # 6. ENVÍO: Logística y tiempos.
    palabras_envio = ["esperando", "retraso", "paquete", "envio", "tarda", "seguimiento", "semana",
                      "demora", "mensajero", "transporte", "domicilio", "entrega", 
                      "recibido", "perdido", "paradero", "rastreo", "localizador", 
                      "agencia", "dias", "tiempo", "tardanza", "enviado", "llegada"]
    
    # --- LÓGICA DE JERARQUÍA (EL CORAZÓN DEL SISTEMA) ---
    # "El orden de los IF importa: definimos qué intención tiene más peso".
    # Priorizamos Información y Feedback para dar una atención amable antes de procesar una queja.

    if any(p in texto_min for p in palabras_info):
        categoria = "informacion" # Prioridad 1: Dudas rápidas.
        
    elif any(p in texto_min for p in palabras_feedback):
        categoria = "feedback_positivo" # Prioridad 2: Agradecimientos.
        
    elif any(p in texto_min for p in palabras_sat):
        categoria = "sat" # Prioridad 3: Soporte técnico.
        
    elif any(p in texto_min for p in palabras_factura):
        categoria = "facturacion_erronea" # Prioridad 4: Dinero.
        
    elif any(p in texto_min for p in palabras_producto):
        categoria = "producto_roto" # Prioridad 5: Calidad física.
        
    elif any(p in texto_min for p in palabras_envio):
        categoria = "retraso_envio" # Prioridad 6: Tiempos de entrega.

    # Log para depuración: nos permite ver qué decidió la red neuronal.
    print(f"\n[ANÁLISIS NEURONAL]")
    print(f" > Sentimiento: {etiqueta} ({valor_sentimiento:.2f})")
    print(f" > Categoría: {categoria.upper()}")

    # Devolvemos un objeto estructurado que el Motor Experto podrá "entender"
    return {
        "categoria": categoria,
        "sentimiento": valor_sentimiento
    }