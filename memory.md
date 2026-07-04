# 🧠 memory.md — Diario de decisiones y bloqueos · EcoWeather Málaga

> Registro de decisiones de arquitectura (ADRs) e historial de problemas y soluciones.

## Decisiones de arquitectura

**ADR-001 · Opción del caso práctico: EcoWeather (Opción A)**
Elegida por usar Open-Meteo, una API gratuita sin registro ni API Key, lo que elimina riesgos de gestión de claves en la fuente de datos y simplifica el arranque del proyecto. Ciudad fijada: Málaga (relevancia local del autor).

**ADR-002 · Stack: Streamlit + Python (perfil de negocio)**
Siguiendo la recomendación del enunciado para perfiles de negocio: Streamlit permite construir interfaz, gráficos interactivos (Plotly) y chat en pocas líneas, centrando el esfuerzo en la especificación y el prompt engineering.

**ADR-003 · LLM: Google Gemini 2.5 Flash con SDK `google-genai`**
Elegido por su tier gratuito, baja latencia y ventana de contexto amplia (necesaria para inyectar el JSON completo de dos endpoints de Open-Meteo en cada consulta). Se usa el SDK moderno `google-genai` en lugar del antiguo `google-generativeai`, ya deprecado.

**ADR-004 · Inyección de contexto en el prompt de sistema**
El JSON de ambos endpoints se inserta en el prompt de sistema en cada pregunta, con reglas explícitas: responder solo con los datos proporcionados, citar valores concretos y no inventar información. Objetivo: evitar alucinaciones (requisito de la rúbrica).

**ADR-005 · Arquitectura modular en 3 archivos**
`api_client.py` (datos), `llm_advisor.py` (IA) y `app.py` (interfaz) separados para facilitar mantenimiento y pruebas, en lugar de un único script monolítico.

**ADR-006 · Caché de datos de 15 minutos**
`st.cache_data(ttl=900)` para no saturar la API de Open-Meteo en cada recarga de la página y acelerar la app.

## Bloqueos encontrados y soluciones

**BLQ-001 · Comando `pip` no reconocido en Windows**
La instalación de Python 3.14 no añadió `pip` al PATH. Solución: usar el lanzador de Windows con `py -m pip install -r requirements.txt` y `py -m streamlit run app.py`.

**BLQ-002 · Aviso de deprecación `use_container_width` en Streamlit 1.58**
Los gráficos generaban warnings porque el parámetro `use_container_width=True` está obsoleto. Solución: sustituirlo por `width="stretch"` en las tres llamadas a `st.plotly_chart`. Durante el reemplazo se introdujo por error una comilla sin cerrar que rompía la sintaxis; se corrigió revisando las líneas afectadas una a una.

**BLQ-003 · Seguridad: API Key expuesta accidentalmente**
La primera clave de Gemini quedó expuesta en una captura de pantalla durante la configuración. Solución: se revocó (borró) la clave comprometida en Google AI Studio y se generó una nueva, almacenada únicamente en el fichero `.env` local (incluido en `.gitignore`). Lección aprendida: las claves nunca se muestran en capturas ni se pegan en chats o repositorios.