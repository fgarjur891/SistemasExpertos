"""
PROYECTO FINAL: ASISTENTE VIRTUAL NEURO-SIMBÓLICO
Módulo: Modelos de Inteligencia Artificial
=============================================================================
FASE 3: MOTOR DE INFERENCIA CLÍNICA/EMPRESARIAL (EXPERTA)

Aquí aplicamos la lógica 
simbólica para deducir hechos futuros a partir de los datos del PLN.

Este es el componente "Simbólico" del sistema Neuro-Simbólico.
Utilizamos el algoritmo Rete (a través de la librería Experta) para procesar reglas.
A diferencia de una red neuronal, aquí el razonamiento es 100% explicable y auditable.
"""

# Parche para compatibilidad con Python moderno (3.10+). 
# "Si el profesor pregunta: Experta usa librerías antiguas que movieron Mapping a collections.abc".
import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import *

# --- 1. DEFINICIÓN DE HECHOS (FACTS) ---
# Los hechos son la "memoria a corto plazo" del motor. 
# Representan lo que el sistema sabe en un momento dado.

class Incidencia(Fact):
    # Viene de la Fase 2: contiene la categoría y el valor del sentimiento (-1 a 1).
    pass

class Cliente(Fact):
    # Datos del perfil: nombre y antigüedad en meses.
    pass

class Prioridad(Fact):
     # Hecho intermedio: El motor lo deduce a partir de la incidencia
    pass

class Resolucion(Fact):
    # El objetivo final: Contiene la acción y el mensaje que dirá la voz
    pass

# --- 2. EL MOTOR DE REGLAS (KNOWLEDGE ENGINE) ---
class MotorAtencion(KnowledgeEngine):
    """
    Contiene la lógica de negocio. Las reglas se disparan solas cuando los hechos 
    coinciden con los patrones de las reglas.
    """

    # --- BLOQUE A: DEDUCCIÓN (Razonamiento de diagnóstico) ---
    # Usamos 'salience' para controlar el orden. Salience alto = se ejecuta antes.

    @Rule(
        # Si el producto está roto Y el sentimiento es muy negativo (<= -0.7)
        Incidencia(categoria="producto_roto", sentimiento=P(lambda x: x <= -0.7)),
        NOT(Prioridad()), # Solo si aún no hemos definido la prioridad
        salience=100
    )
    def prioridad_muy_alta(self):
        # Deducción: Un cliente muy enfadado con algo roto es CRÍTICO
        self.declare(Prioridad(nivel="CRITICA"))

    @Rule(
        OR(
            Incidencia(categoria="facturacion_erronea"),
            Incidencia(categoria="producto_roto"),
            Incidencia(categoria="retraso_envio")
        ),
        NOT(Prioridad()),
        salience=90
    )
    def prioridad_general(self):
        # Cualquier problema serio recibe al menos prioridad MEDIA
        self.declare(Prioridad(nivel="MEDIA"))

    # --- BLOQUE B: POLÍTICAS (Toma de decisiones estratégica) ---
    """El operador << es un vínculo de variable (alias). Lo utilizo para asignar un 
    nombre a un hecho específico que cumple los requisitos de la regla. Sin este alias, 
    el motor de reglas (KnowledgeEngine) no tendría una referencia física para poder usar 
    el método self.modify() y actualizar la información de la respuesta final"""
    @Rule(
        Prioridad(nivel=MATCH.n), # Capturamos el nivel de prioridad en una variable 'n'
        Cliente(antiguedad=P(lambda x: x > 24)), # Si lleva más de 2 años es VIP
        AS.res << Resolucion(accion=None), # Seleccionamos el hecho Resolucion para modificarlo
        salience=50
    )
    def politica_vip(self, res, n):
        # Regla de Fidelización: A los VIP se les compensa siempre (Bono)
        self.modify(res, accion="BONO_FIDELIDAD", mensaje_voz="Gracias por su fidelidad. Hemos asignado un bono...")

    @Rule(
        Prioridad(nivel="CRITICA"),
        Cliente(antiguedad=P(lambda x: x <= 24)), # Cliente estándar enfadado
        AS.res << Resolucion(accion=None),
        salience=40
    )
    def politica_critica_estandar(self, res):
        # Regla de urgencia: Atención por supervisor
        self.modify(res, accion="URGENCIA_ESTANDAR", mensaje_voz="Lamentamos su mala experiencia. Un supervisor le contactará...")

    # BLOQUE C: FLUJOS DIRECTOS (INFORMACIÓN Y OTROS)
    # Categorías que no requieren cálculo de prioridad previa.

    @Rule(
        Incidencia(categoria="sat"),
        AS.res << Resolucion(accion=None),
        salience=60 # Prioridad media-alta para ganar a la seguridad final
    )
    def flujo_sat(self, res):
        # Regla 6: Servicio Técnico (SAT) con respuesta personalizada.
        self.modify(res, 
                    accion="DERIVAR_TECNICO", 
                    mensaje_voz="Pasamos nota a nuestros especialistas para ayudarle, no se retire")

    @Rule(
        Incidencia(categoria="informacion"),
        AS.res << Resolucion(accion=None),
        salience=60
    )
    def flujo_informacion(self, res):
        # Regla 7: Consultas generales.
        self.modify(res, 
                    accion="INFORMAR", 
                    mensaje_voz="Visite nuestra web www.sistemasexpertos.org, encontrará la información necesaria")

    @Rule(
        Incidencia(categoria="feedback_positivo"),
        AS.res << Resolucion(accion=None),
        salience=60
    )
    def agradecer_cliente(self, res):
        # Regla 8: Gestión de agradecimientos.
        self.modify(res, 
                    accion="AGRADECER", 
                    mensaje_voz="¡Muchas gracias por sus amables palabras! Nos motiva mucho seguir mejorando para usted.")

    @Rule(
        Incidencia(categoria="desconocido"),
        AS.res << Resolucion(accion=None),
        salience=10 # Por encima del paracaídas final pero por debajo de lo demás
    )
    def alerta_desconocido(self, res):
        #Regla 9: Fallback cuando la Fase 2 no entiende la categoría.
        self.modify(res, 
                    accion="DERIVAR_HUMANO", 
                    mensaje_voz="No estoy seguro de haberle entendido bien. Le paso con un agente humano para ayudarle mejor.")

    # --- BLOQUE D: SEGURIDAD (Manejo de errores y fallbacks) ---

    @Rule(
        AS.res << Resolucion(accion=None),
        salience=-100 # Se ejecuta solo si NADA de lo anterior funcionó
    )
    def seguridad_final(self, res):
        # Regla 'Paracaídas': Evita que el sistema se quede mudo ante casos raros
        self.modify(res, accion="ERROR_LOGICA", mensaje_voz="He recibido su incidencia y la estoy procesando...")

# --- 3. INTEGRACIÓN ---
def procesar_con_sistema_experto(datos_nlp, nombre_cliente, meses):
    # Esta función es el puente: inyecta los datos de la IA Neuronal en el Motor Simbólico
    engine = MotorAtencion()
    engine.reset() # Limpia la memoria de trabajo

    # Declaramos los hechos iniciales (Lo que sabemos)
    engine.declare(Cliente(nombre=nombre_cliente, antiguedad=meses))
    engine.declare(Incidencia(categoria=datos_nlp['categoria'], sentimiento=datos_nlp['sentimiento']))
    engine.declare(Resolucion(accion=None)) # Hecho vacío para que el motor lo rellene

    engine.run() # Dispara el motor de inferencia
    
    # Buscamos la respuesta final en los hechos resultantes
    for f in engine.facts.values():
        if isinstance(f, Resolucion):
            return f.get('mensaje_voz', "Error en el motor")