"""
app.py — EcoWeather Málaga: Asesor de Clima y Calidad del Aire con IA.
Interfaz web construida con Streamlit: dashboard + chatbot.

Ejecutar con:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import obtener_datos_meteo, obtener_datos_aire
from llm_advisor import preguntar_asesor

# ---------- Configuración de la página ----------
st.set_page_config(page_title="EcoWeather Málaga", page_icon="🌤️", layout="wide")
st.title("🌤️ EcoWeather Málaga")
st.caption("Asesor inteligente de clima, calidad del aire y energía · Datos: Open-Meteo · IA: Google Gemini")


# ---------- Carga de datos con caché (15 min) ----------
@st.cache_data(ttl=900)
def cargar_datos():
    return obtener_datos_meteo(), obtener_datos_aire()


datos_meteo, datos_aire = cargar_datos()

# ---------- Manejo de errores de la API (requisito de la rúbrica) ----------
if datos_meteo is None or datos_aire is None:
    st.error("😕 No hemos podido obtener los datos de Open-Meteo en este momento. "
             "Comprueba tu conexión a internet e inténtalo de nuevo en unos minutos.")
    st.stop()

# ---------- Dashboard: 3 gráficos ----------
col1, col2 = st.columns(2)

df_meteo = pd.DataFrame({
    "Fecha y hora": pd.to_datetime(datos_meteo["hourly"]["time"]),
    "Temperatura (°C)": datos_meteo["hourly"]["temperature_2m"],
    "Radiación solar (W/m²)": datos_meteo["hourly"]["shortwave_radiation"],
})

df_aire = pd.DataFrame({
    "Fecha y hora": pd.to_datetime(datos_aire["hourly"]["time"]),
    "PM2.5 (µg/m³)": datos_aire["hourly"]["pm2_5"],
    "NO2 (µg/m³)": datos_aire["hourly"]["nitrogen_dioxide"],
})

with col1:
    st.subheader("🌡️ Temperatura (próximos 7 días)")
    fig_temp = px.line(df_meteo, x="Fecha y hora", y="Temperatura (°C)")
    st.plotly_chart(fig_temp, width="stretch")

with col2:
    st.subheader("☀️ Radiación solar (próximos 7 días)")
    fig_rad = px.area(df_meteo, x="Fecha y hora", y="Radiación solar (W/m²)")
    st.plotly_chart(fig_rad, width="stretch")

st.subheader("😮‍💨 Calidad del aire: PM2.5 y NO2 (próximos 5 días)")
fig_aire = px.line(df_aire, x="Fecha y hora", y=["PM2.5 (µg/m³)", "NO2 (µg/m³)"])
st.plotly_chart(fig_aire, width="stretch")

# ---------- Chatbot ----------
st.divider()
st.subheader("💬 Pregunta a EcoAsesor Málaga")
st.caption("Ejemplos: «¿Es buen momento para cargar el coche eléctrico?» · "
           "«Tengo asma, ¿qué precauciones tomo hoy?» · "
           "«Resumen ejecutivo de sostenibilidad para esta semana»")

# Historial de conversación en la sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

pregunta = st.chat_input("Escribe tu pregunta sobre el clima, el aire o la energía en Málaga...")

if pregunta:
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando los datos y pensando..."):
            respuesta = preguntar_asesor(pregunta, datos_meteo, datos_aire)
        st.markdown(respuesta)

    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})
