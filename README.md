## 💻 Modo de Ejecución
Sigue estos pasos para iniciar el asistente[cite: 2, 10]:

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
El sistema aplica una jerarquía lógica para resolver conflictos[cite: 2, 6]:
*   **Prioridad de Categorías:** Se prioriza el *Feedback Positivo* y la *Información* para evitar falsos negativos en la atención[cite: 2, 10].
*   **Influencia del Sentimiento:** Si el sentimiento es negativo ($< 0.4$), se activan protocolos de "Urgencia" o "Fidelización"[cite: 2, 10].
*   **Política VIP:** Clientes con antigüedad $> 24$ meses reciben compensaciones automáticas (Bonos) ante incidencias críticas[cite: 2, 6, 9].

---

## 📂 Estructura de Archivos
| Archivo | Responsabilidad |
| :--- | :--- |
| `main_test.py` | Orquestador central y gestión de la interfaz de usuario[cite: 9, 10]. |
| `fase1_captura.py` | Preprocesamiento de texto y gestión de hardware de audio[cite: 4, 10]. |
| `fase2_analisis.py` | Inferencia neuronal de sentimiento y categorización por diccionarios[cite: 5, 10]. |
| `fase3_motor.py` | Razonamiento lógico y aplicación de reglas de negocio[cite: 6, 10]. |
| `fase4_voz.py` | Síntesis de voz multilingüe offline[cite: 7, 10]. |
| `fase5_informe.py` | Generación de reportes PDF con diseño dinámico[cite: 8, 10]. |

---

## ⚖️ Licencia
Este proyecto ha sido desarrollado como **Proyecto Final** para el módulo de Modelos de Inteligencia Artificial[cite: 10].

**Autor:** Pako García[cite: 10]
**Pseudónimo:** PKROTAquí tienes una propuesta completa de `README.md` estructurada para tu repositorio de Git. Está diseñada para ser profesional, técnica y visualmente organizada, reflejando todos los puntos clave de tu proyecto[cite: 1, 10].

---

# Sistema de Atención al Cliente Neuro-Simbólico 🧠🤖

![Banner del Proyecto](https://i.imgur.com/tu_enlace_a_la_imagen.png) 
*(Nota: Sube la imagen del cerebro y el templo griego a tu repo y pon la ruta aquí)*

Este proyecto presenta una solución avanzada de **IA Neuro-Simbólica** que fusiona el aprendizaje profundo (**Deep Learning**) para el procesamiento de lenguaje natural con la lógica determinista de los **Sistemas Expertos**. El objetivo es proporcionar un asistente capaz de "entender" la semántica y el sentimiento del usuario para luego razonar decisiones de negocio precisas[cite: 2, 10].

## 🚀 Resumen del Proyecto
A diferencia de los chatbots convencionales, esta arquitectura permite:
*   **Interpretación Neuronal:** Análisis de sentimiento y categorización mediante modelos Transformer[cite: 1, 10].
*   **Razonamiento Simbólico:** Toma de decisiones basada en reglas de negocio (Algoritmo Rete) y perfiles de cliente (VIP vs. Estándar)[cite: 2, 6].
*   **Interacción Humana:** Entrada por voz (STT) y respuesta sintetizada (TTS)[cite: 1, 7].

---

## 🛠️ Arquitectura del Sistema
El sistema se organiza en **5 fases críticas** coordinadas por un orquestador central (`main_test.py`)[cite: 2, 10]:



1.  **Fase 1 - Captura y Limpieza:** Conversión de audio a texto y normalización (Regex, NFD)[cite: 1, 4].
2.  **Fase 2 - Análisis NLP:** Clasificación de sentimiento y categoría con el modelo **XLM-RoBERTa**[cite: 1, 5].
3.  **Fase 3 - Motor Experto:** Inferencia lógica mediante la librería **Experta** (basada en CLIPS)[cite: 1, 6].
4.  **Fase 4 - Salida de Voz:** Respuesta mediante síntesis de voz (TTS) offline con **Pyttsx3**[cite: 1, 7].
5.  **Fase 5 - Informe PDF:** Generación de reportes de sesión con trazabilidad total (**FPDF2**)[cite: 1, 8].

---

## 📦 Instalación y Configuración

### Requisitos Previos
*   Python 3.10 o superior.
*   Entorno virtual (recomendado).

### Instalación de dependencias
Ejecuta el siguiente comando para instalar todos los componentes necesarios[cite: 10]:
```bash
pip install experta transformers torch SpeechRecognition pyttsx3 PyAudio nltk fpdf2 protobuf sentencepiece tiktoken
```

O bien, si utilizas un archivo de requerimientos:
```bash
pip install -r requirements.txt
```

---

## 💻 Modo de Ejecución
Sigue estos pasos para iniciar el asistente[cite: 2, 10]:

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
El sistema aplica una jerarquía lógica para resolver conflictos[cite: 2, 6]:
*   **Prioridad de Categorías:** Se prioriza el *Feedback Positivo* y la *Información* para evitar falsos negativos en la atención[cite: 2, 10].
*   **Influencia del Sentimiento:** Si el sentimiento es negativo ($< 0.4$), se activan protocolos de "Urgencia" o "Fidelización"[cite: 2, 10].
*   **Política VIP:** Clientes con antigüedad $> 24$ meses reciben compensaciones automáticas (Bonos) ante incidencias críticas[cite: 2, 6, 9].

---

## 📂 Estructura de Archivos
| Archivo | Responsabilidad |
| :--- | :--- |
| `main_test.py` | Orquestador central y gestión de la interfaz de usuario[cite: 9, 10]. |
| `fase1_captura.py` | Preprocesamiento de texto y gestión de hardware de audio[cite: 4, 10]. |
| `fase2_analisis.py` | Inferencia neuronal de sentimiento y categorización por diccionarios[cite: 5, 10]. |
| `fase3_motor.py` | Razonamiento lógico y aplicación de reglas de negocio[cite: 6, 10]. |
| `fase4_voz.py` | Síntesis de voz multilingüe offline[cite: 7, 10]. |
| `fase5_informe.py` | Generación de reportes PDF con diseño dinámico[cite: 8, 10]. |

---

## ⚖️ Licencia
Este proyecto ha sido desarrollado como **Proyecto Final** para el módulo de Modelos de Inteligencia Artificial[cite: 10].

**Autor:** Pako García[cite: 10]
**Pseudónimo:** PKROT[cite: 10]
```
