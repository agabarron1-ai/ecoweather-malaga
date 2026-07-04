# 🎬 walkthrough.md — Resumen de entrega · EcoWeather Málaga

## Qué se ha construido

**EcoWeather Málaga**: aplicación web en Streamlit que combina datos en tiempo real de la API pública Open-Meteo (temperatura, radiación solar, PM2.5 y NO2 de Málaga) con un asistente conversacional basado en Google Gemini 2.5 Flash. El asistente recibe en cada consulta el JSON completo devuelto por la API, inyectado en el prompt de sistema, y responde únicamente basándose en esos datos reales.

## Cambios realizados (desarrollo incremental)

1. **Especificación** (`docs/SPECIFICATIONS.md`): requisitos funcionales, flujo de usuario, endpoints, diseño del prompt y arquitectura, redactados antes de escribir código (enfoque SDD).
2. **Construcción de la app** en 3 módulos: `api_client.py` (datos + manejo de errores), `llm_advisor.py` (IA + inyección de contexto), `app.py` (interfaz con 3 gráficos interactivos y chat).
3. **Seguridad**: API Key gestionada por variable de entorno en `.env`, excluido del repositorio vía `.gitignore`. Una clave expuesta accidentalmente durante la configuración fue revocada y sustituida (ver `memory.md`, BLQ-003).
4. **Correcciones**: adaptación a Streamlit 1.58 (`use_container_width` → `width="stretch"`) y ajuste de comandos de Python en Windows (`py -m ...`).
5. **Documentación viva**: `task.md` y `memory.md` actualizados durante el desarrollo, con historial de commits incremental en Git.

## Pruebas ejecutadas

| Prueba | Resultado |
|---|---|
| Carga de datos reales de Málaga en los 3 gráficos | ✅ Correcto |
| Caso de uso: precauciones para asmáticos | ✅ El asistente citó los valores reales del día (PM2.5 entre 3.6 y 6.1 µg/m³; NO2 entre 1.6 y 13.9 µg/m³) y recomendó en base a ellos |
| Caso de uso: carga de vehículo eléctrico según radiación solar | ✅ Correcto |
| Caso de uso: resumen ejecutivo semanal de sostenibilidad | ✅ Correcto |
| Manejo de fallo de la API (sin conexión) | ✅ Mensaje amigable, la app no se rompe |
| Arranque desde cero siguiendo solo el README | ✅ Correcto |

## Demostración

**📹 Vídeo demostrativo (máx. 3 minutos):** [ENLACE AL VÍDEO — pendiente]

El vídeo muestra: la interfaz cargando datos en tiempo real de Open-Meteo, los tres gráficos interactivos, y la interacción conversacional con el chatbot respondiendo a los casos de uso con valores reales de los datos.