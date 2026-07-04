"""
api_client.py — Conexión con la API pública Open-Meteo (gratuita, sin API Key).
Obtiene previsión meteorológica, radiación solar y calidad del aire para Málaga.
"""

import requests

# Coordenadas de Málaga
LATITUD = 36.72
LONGITUD = -4.42

URL_METEO = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUD}&longitude={LONGITUD}"
    "&hourly=temperature_2m,shortwave_radiation"
    "&forecast_days=7&timezone=Europe%2FMadrid"
)

URL_AIRE = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    f"?latitude={LATITUD}&longitude={LONGITUD}"
    "&hourly=pm2_5,nitrogen_dioxide"
    "&forecast_days=5&timezone=Europe%2FMadrid"
)


def obtener_datos_meteo():
    """Devuelve el JSON de temperatura y radiación solar, o None si la API falla."""
    try:
        respuesta = requests.get(URL_METEO, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException:
        return None


def obtener_datos_aire():
    """Devuelve el JSON de calidad del aire (PM2.5 y NO2), o None si la API falla."""
    try:
        respuesta = requests.get(URL_AIRE, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException:
        return None
