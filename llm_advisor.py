"""
llm_advisor.py — Integración con Google Gemini.
Construye el prompt de sistema inyectando los datos reales de Open-Meteo
para que el asistente responda sin alucinaciones.
"""

import os
import json
from dotenv import load_dotenv
from google import genai

# Carga la clave desde el fichero .env (nunca se sube a GitHub)
load_dotenv()

MODELO = "gemini-2.5-flash"

PROMPT_SISTEMA = """Eres "EcoAsesor Málaga", un asesor experto en salud ambiental y
eficiencia energética. Tu única fuente de información son los datos meteorológicos
y de calidad del aire que se te proporcionan a continuación en formato JSON,
obtenidos de la API de Open-Meteo para la ciudad de Málaga.

REGLAS:
1. Responde SOLO basándote en los datos proporcionados. Si la información necesaria
   no está en los datos, dilo claramente. No inventes valores.
2. Responde en español, con tono cercano y claro, evitando jerga técnica.
3. Cuando des recomendaciones de salud (asma, alergias, deporte), cita el valor
   concreto del dato en que te basas (ej. "el PM2.5 actual es 12 µg/m³").
4. Para preguntas de energía solar o vehículos eléctricos, usa los datos de
   radiación solar (shortwave_radiation) para identificar las mejores horas.
5. No des consejos médicos diagnósticos; recomienda consultar a un profesional
   si la pregunta lo requiere.

DATOS METEOROLÓGICOS Y DE RADIACIÓN SOLAR (JSON):
{datos_meteo}

DATOS DE CALIDAD DEL AIRE (JSON):
{datos_aire}
"""


def preguntar_asesor(pregunta, datos_meteo, datos_aire):
    """Envía la pregunta del usuario al LLM junto con los datos reales de la API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return ("⚠️ No se ha encontrado la clave de Gemini. "
                "Crea un fichero .env con la línea: GEMINI_API_KEY=tu_clave")

    contexto = PROMPT_SISTEMA.format(
        datos_meteo=json.dumps(datos_meteo, ensure_ascii=False),
        datos_aire=json.dumps(datos_aire, ensure_ascii=False),
    )

    try:
        cliente = genai.Client(api_key=api_key)
        respuesta = cliente.models.generate_content(
            model=MODELO,
            contents=f"{contexto}\n\nPREGUNTA DEL USUARIO: {pregunta}",
        )
        return respuesta.text
    except Exception as error:
        return f"⚠️ Error al conectar con el asistente de IA: {error}"
