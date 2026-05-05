
# Sistema de Atención al Cliente Neuro-Simbólico 🧠🤖

<img width="723" height="1295" alt="image" src="https://github.com/user-attachments/assets/03cf39ef-ab87-45af-9cf2-9a3539f17da6" />


Este proyecto presenta una solución avanzada de **IA Neuro-Simbólica** que fusiona el aprendizaje profundo (**Deep Learning**) para el procesamiento de lenguaje natural con la lógica determinista de los **Sistemas Expertos**. El objetivo es proporcionar un asistente capaz de "entender" la semántica y el sentimiento del usuario para luego razonar decisiones de negocio precisas.

## 🚀 Resumen del Proyecto
A diferencia de los chatbots convencionales, esta arquitectura permite:
*   **Interpretación Neuronal:** Análisis de sentimiento y categorización mediante modelos Transformer.
*   **Razonamiento Simbólico:** Toma de decisiones basada en reglas de negocio (Algoritmo Rete) y perfiles de cliente (VIP vs. Estándar)
*   **Interacción Humana:** Entrada por voz (STT) y respuesta sintetizada (TTS)

---

## 🛠️ Arquitectura del Sistema
El sistema se organiza en **5 fases críticas** coordinadas por un orquestador central (`main_test.py`):



1.  **Fase 1 - Captura y Limpieza:** Conversión de audio a texto y normalización (Regex, NFD).
2.  **Fase 2 - Análisis NLP:** Clasificación de sentimiento y categoría con el modelo **XLM-RoBERTa**.
3.  **Fase 3 - Motor Experto:** Inferencia lógica mediante la librería **Experta** (basada en CLIPS).
4.  **Fase 4 - Salida de Voz:** Respuesta mediante síntesis de voz (TTS) offline con **Pyttsx3**.
5.  **Fase 5 - Informe PDF:** Generación de reportes de sesión con trazabilidad total (**FPDF2**).

---

## 📦 Instalación y Configuración

### Requisitos Previos
*   Python 3.10 o superior.
*   Entorno virtual (recomendado).

### Instalación de dependencias
Ejecuta el siguiente comando para instalar todos los componentes necesarios:
```bash
pip install experta transformers torch SpeechRecognition pyttsx3 PyAudio nltk fpdf2 protobuf sentencepiece tiktoken
```

O bien, si utilizas un archivo de requerimientos:
```bash
pip install -r requirements.txt
```

---

## 💻 Modo de Ejecución
Sigue estos pasos para iniciar el asistente:

1.  Activa tu entorno virtual.
2.  Ejecuta el controlador principal:
    ```bash
    python main_test.py
    ```
3.  **Selecciona el modo:**
    *   `1`: Modo Manual (Uso de micrófono real).
    *   `2`: Modo Automático (Simulación con frases de test).
4.  **Identifica al cliente:** Introduce un ID (1-5) para cargar el perfil de antigüedad (VIP o Estándar).
5.  **Interacción:** Dicta tu problema o deja que el sistema elija una frase al azar.
6.  **Finalización:** Usa la opción `3` para cerrar la sesión y generar el **Informe PDF** con la trazabilidad completa.

---

## 🧠 Lógica de Negocio y Decisiones
El sistema aplica una jerarquía lógica para resolver conflictos:
*   **Prioridad de Categorías:** Se prioriza el *Feedback Positivo* y la *Información* para evitar falsos negativos en la atención.
*   **Influencia del Sentimiento:** Si el sentimiento es negativo ($< 0.4$), se activan protocolos de "Urgencia" o "Fidelización".
*   **Política VIP:** Clientes con antigüedad $> 24$ meses reciben compensaciones automáticas (Bonos) ante incidencias críticas.

---

## 📂 Estructura de Archivos
| Archivo | Responsabilidad |
| :--- | :--- |
| `main_test.py` | Orquestador central y gestión de la interfaz de usuario. |
| `fase1_captura.py` | Preprocesamiento de texto y gestión de hardware de audio. |
| `fase2_analisis.py` | Inferencia neuronal de sentimiento y categorización por diccionarios. |
| `fase3_motor.py` | Razonamiento lógico y aplicación de reglas de negocio. |
| `fase4_voz.py` | Síntesis de voz multilingüe offline. |
| `fase5_informe.py` | Generación de reportes PDF con diseño dinámico. |

---

## ⚖️ Licencia
Este proyecto ha sido desarrollado como **Proyecto Final** para el módulo de Modelos de Inteligencia Artificial.

**Autor:** Pako García
```
