✅ task.md — Checklist de tareas · EcoWeather Málaga


Estados: [ ] pendiente · [/] en progreso · [x] completado



Fase 1: Spec (Especificación)


 Elegir opción del caso práctico (Opción A: EcoWeather & Air Quality Advisor)
 Definir ciudad objetivo (Málaga) y endpoints de Open-Meteo
 Elegir proveedor de LLM (Google Gemini 2.5 Flash) y justificarlo
 Redactar docs/SPECIFICATIONS.md completo (requisitos, flujo de usuario, prompt, arquitectura)


Fase 2: Plan (Planificación)


 Definir arquitectura modular en 3 archivos: api_client.py, llm_advisor.py, app.py
 Elegir metodología de gestión: Opción 1 (dbv-specs-ops, plantilla del profesor)
 Crear repositorio desde la plantilla dbv-specs-ops


Fase 3: Build (Construcción)


 Módulo de conexión a Open-Meteo con manejo de errores (api_client.py)
 Módulo de integración con Gemini e inyección de contexto (llm_advisor.py)
 Interfaz Streamlit: 3 gráficos (temperatura, radiación solar, calidad del aire) + chat (app.py)
 Gestión segura de la API Key con .env + .gitignore
 Corregir parámetro obsoleto use_container_width → width="stretch" (Streamlit 1.58)


Fase 4: Test (Validación)


 Verificar carga de datos reales de Málaga en los 3 gráficos
 Caso de uso 1: precauciones para asmáticos según PM2.5/NO2 → el asistente cita valores reales ✔
 Caso de uso 2: mejor momento para carga de vehículo eléctrico según radiación solar
 Caso de uso 3: resumen ejecutivo semanal de sostenibilidad
 Probar el manejo de errores (desconectar internet y verificar mensaje amigable)
 Verificar arranque limpio siguiendo solo el README en una carpeta nueva


Fase 5: Ship (Entrega)


 Actualizar README.md con instrucciones de instalación (.env, dependencias, arranque)
 Completar walkthrough.md con resumen de cambios y capturas
 Grabar vídeo demostrativo (máximo 3 minutos)
 Revisión final: ninguna API Key en el código ni en el historial de Git
 Entregar enlace al repositorio + vídeo