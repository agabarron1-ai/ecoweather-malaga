# 🌤️ EcoWeather Málaga — Asesor de Clima y Calidad del Aire con IA

Trabajo Fin de Módulo · **Fundamentos de Inteligencia Artificial** · Máster ESIC

Aplicación web que muestra la previsión de **temperatura, radiación solar y calidad del aire (PM2.5 y NO2)** de Málaga con datos en tiempo real de la API pública [Open-Meteo](https://open-meteo.com/), e integra un **asistente conversacional (Google Gemini)** que responde preguntas de salud, energía y sostenibilidad basándose estrictamente en esos datos.

**📹 Vídeo demostrativo:** [ENLACE AL VÍDEO — pendiente]

---

## 🚀 Cómo ejecutar la aplicación

### 1. Requisitos previos

- Python 3.10 o superior instalado ([python.org](https://www.python.org/downloads/))
- Una API Key gratuita de Google Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

### 2. Clonar el repositorio

```bash
git clone https://github.com/agabarron1-ai/ecoweather-malaga.git
cd ecoweather-malaga
```

### 3. Configurar la API Key (fichero `.env`)

Crea un archivo llamado `.env` en la raíz del proyecto con una sola línea:

```
GEMINI_API_KEY=tu_clave_de_gemini_aqui
```

> ⚠️ El `.env` está incluido en `.gitignore` y **nunca debe subirse al repositorio**.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

*(En Windows, si `pip` no se reconoce, usar: `py -m pip install -r requirements.txt`)*

### 5. Arrancar la aplicación

```bash
streamlit run app.py
```

*(En Windows, alternativamente: `py -m streamlit run app.py`)*

La app se abre automáticamente en el navegador en `http://localhost:8501`.

---

## 🧭 Cómo usarla

1. Al cargar, la app descarga los datos actuales de Open-Meteo para Málaga y muestra tres gráficos interactivos: temperatura (7 días), radiación solar (7 días) y calidad del aire PM2.5/NO2 (5 días).
2. Al final de la página está el chat **EcoAsesor Málaga**. Ejemplos de preguntas:
   - *"Tengo asma, ¿qué precauciones debo tomar hoy según la calidad del aire?"*
   - *"¿Es buen momento para cargar el coche eléctrico según la radiación solar prevista?"*
   - *"Hazme un resumen ejecutivo con recomendaciones de sostenibilidad para esta semana."*

## 🏗️ Arquitectura

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Interfaz Streamlit: gráficos Plotly + chat |
| `api_client.py` | Conexión con Open-Meteo y manejo de errores |
| `llm_advisor.py` | Prompt de sistema con inyección del JSON real + llamada a Gemini 2.5 Flash |

## 📂 Documentación del proyecto (metodología dbv-specs-ops)

- [`docs/SPECIFICATIONS.md`](docs/SPECIFICATIONS.md) — Especificación técnica completa
- [`task.md`](task.md) — Checklist de tareas del proyecto
- [`memory.md`](memory.md) — Diario de decisiones de arquitectura y bloqueos resueltos
- [`walkthrough.md`](walkthrough.md) — Resumen final de entrega