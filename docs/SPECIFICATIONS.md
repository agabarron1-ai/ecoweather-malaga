# 📋 SPECIFICATIONS.md — EcoWeather Málaga: Asesor de Clima y Calidad del Aire

**Proyecto:** Trabajo Fin de Módulo — Fundamentos de Inteligencia Artificial (Máster ESIC)
**Opción elegida:** Opción A — EcoWeather & Air Quality Advisor
**Autor:** Arturo
**Fecha:** Julio 2026

---

## 1. Objetivo de la aplicación

Aplicación web que muestra datos meteorológicos y de calidad del aire de **Málaga** en tiempo real, con un **asistente conversacional de IA** integrado que responde preguntas sobre salud, energía y sostenibilidad basándose estrictamente en esos datos.

**Problema de negocio que resuelve:** ayudar a ciudadanos y pequeñas empresas de Málaga a tomar decisiones diarias informadas (actividad al aire libre, precauciones de salud respiratoria, momento óptimo para consumo energético con energía solar) sin necesidad de interpretar datos técnicos.

---

## 2. Alcance funcional (qué hace y qué no hace)

### ✅ Incluido (MVP)

| Funcionalidad | Descripción |
|---|---|
| **F1. Dashboard meteorológico** | Gráfico de temperatura por horas para los próximos 7 días en Málaga |
| **F2. Dashboard calidad del aire** | Gráfico de PM2.5 y NO2 actuales y previstos |
| **F3. Dashboard radiación solar** | Gráfico de radiación solar prevista para la semana |
| **F4. Chatbot asesor** | Chat integrado que responde preguntas del usuario usando los datos de F1–F3 |
| **F5. Manejo de errores** | Si la API falla, se muestra un mensaje amigable y la app no se rompe |

### ❌ Fuera de alcance

- Selección de otras ciudades (fijamos Málaga para simplificar el MVP; ampliable en futuras versiones)
- Registro de usuarios o histórico de conversaciones
- Notificaciones o alertas automáticas

---

## 3. Flujo del usuario

1. El usuario abre la aplicación en el navegador.
2. La app carga automáticamente los datos de Open-Meteo para Málaga (lat 36.72, lon -4.42).
3. El usuario ve los tres gráficos (temperatura, calidad del aire, radiación solar).
4. En la parte inferior, escribe una pregunta en el chat (ej. *"Tengo asma, ¿qué precauciones tomo hoy?"*).
5. La app envía la pregunta + los datos de la API al modelo de IA.
6. El asistente responde basándose únicamente en los datos reales mostrados.

---

## 4. APIs y fuentes de datos

### 4.1 API pública de datos: Open-Meteo (gratuita, sin API Key)

**Endpoint 1 — Previsión meteorológica y radiación solar:**

```
https://api.open-meteo.com/v1/forecast?latitude=36.72&longitude=-4.42&hourly=temperature_2m,shortwave_radiation&forecast_days=7&timezone=Europe%2FMadrid
```

**Endpoint 2 — Calidad del aire:**

```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude=36.72&longitude=-4.42&hourly=pm2_5,nitrogen_dioxide&forecast_days=5&timezone=Europe%2FMadrid
```

Ambos devuelven JSON. No requieren registro ni clave.

### 4.2 Proveedor de LLM: Google Gemini API

- **Modelo:** `gemini-1.5-flash`
- **Justificación:** tier gratuito suficiente para el proyecto, baja latencia, ventana de contexto amplia para inyectar el JSON completo de la API.
- **Gestión de la clave:** variable de entorno `GEMINI_API_KEY` en fichero `.env` local, **incluido en `.gitignore`**. Nunca se sube al repositorio.

---

## 5. Diseño del prompt del asistente (Prompt Engineering)

### Prompt de sistema

```
Eres "EcoAsesor Málaga", un asesor experto en salud ambiental y eficiencia
energética. Tu única fuente de información son los datos meteorológicos y de
calidad del aire que se te proporcionan a continuación en formato JSON,
obtenidos de la API de Open-Meteo para la ciudad de Málaga.

REGLAS:
1. Responde SOLO basándote en los datos proporcionados. Si la información
   necesaria no está en los datos, dilo claramente. No inventes valores.
2. Responde en español, con tono cercano y claro, evitando jerga técnica.
3. Cuando des recomendaciones de salud (asma, alergias, deporte), cita el
   valor concreto del dato en que te basas (ej. "el PM2.5 actual es 12 µg/m³").
4. Para preguntas de energía solar o vehículos eléctricos, usa los datos de
   radiación solar (shortwave_radiation) para identificar las mejores horas.
5. No des consejos médicos diagnósticos; recomienda consultar a un profesional
   si la pregunta lo requiere.

DATOS ACTUALES (JSON de Open-Meteo):
{datos_meteo}

{datos_aire}
```

### Estrategia de inyección de contexto

En cada pregunta del usuario, la app descarga (o reutiliza de caché) el JSON de los dos endpoints y lo inserta en el prompt de sistema antes de llamar al LLM. Así el asistente responde con datos reales y se evitan alucinaciones.

### Casos de uso de prueba (validación del chatbot)

1. *"¿Es buen día hoy para cargar el coche eléctrico o usar paneles solares según la radiación prevista?"*
2. *"Tengo asma, ¿qué precauciones debo tomar hoy en Málaga según la calidad del aire?"*
3. *"Hazme un resumen ejecutivo con recomendaciones de sostenibilidad para esta semana."*

---

## 6. Arquitectura del software

### Stack tecnológico

| Capa | Tecnología | Motivo |
|---|---|---|
| Interfaz web + gráficos + chat | **Streamlit** (Python) | Recomendado para perfiles de negocio; app completa en pocas líneas |
| Gráficos | Plotly (integrado en Streamlit) | Gráficos interactivos sin esfuerzo extra |
| Datos externos | `requests` → Open-Meteo | API gratuita sin clave |
| IA | `google-generativeai` → Gemini 1.5 Flash | Tier gratuito, respuesta rápida |
| Configuración | `python-dotenv` → fichero `.env` | Seguridad de la API Key |

### Estructura de archivos

```
├── app.py                  # Interfaz Streamlit (gráficos + chat)
├── api_client.py           # Llamadas a Open-Meteo + manejo de errores
├── llm_advisor.py          # Construcción del prompt e integración con Gemini
├── requirements.txt        # Dependencias
├── .env                    # GEMINI_API_KEY (NO se sube a GitHub)
├── .gitignore              # Incluye .env
├── README.md               # Instrucciones de instalación y arranque
├── task.md                 # Checklist de tareas vivas
├── memory.md               # Diario de decisiones y bloqueos
├── walkthrough.md          # Resumen final de entrega
└── docs/
    └── SPECIFICATIONS.md   # Este documento
```

### Manejo de errores (requisito de la rúbrica)

- Si Open-Meteo no responde: mensaje amigable en pantalla ("No hemos podido obtener los datos meteorológicos, inténtalo en unos minutos") y la app sigue funcionando.
- Si Gemini falla o no hay clave configurada: aviso claro en el chat indicando cómo configurar el `.env`.
- Caché de datos de 15 minutos (`st.cache_data`) para no saturar la API y acelerar la app.

---

## 7. Criterios de éxito (Definition of Done)

- [ ] La app arranca con `streamlit run app.py` siguiendo solo el README
- [ ] Los 3 gráficos cargan datos reales de Málaga
- [ ] El chatbot responde correctamente los 3 casos de uso de prueba citando datos concretos
- [ ] Ninguna API Key aparece en el código ni en el historial de Git
- [ ] `task.md` y `memory.md` actualizados durante el desarrollo
- [ ] Vídeo demostrativo de máximo 3 minutos grabado y enlazado
