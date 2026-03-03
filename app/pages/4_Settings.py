import streamlit as st
import os

st.set_page_config(page_title="Settings - Research Copilot", page_icon="⚙️", layout="centered")

st.title("⚙️ Configuración del Sistema")

st.header("Parámetros del Modelo")
model_name = st.selectbox("Modelo LLM", options=["gpt-4", "gpt-3.5-turbo"], index=0)
temperature = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

st.divider()

st.header("Información del Sistema")
st.write(f"**Directorio de Base de Datos:** `./chroma_db` or `{os.path.abspath('./chroma_db')}`")
st.write(f"**Carpeta de Prompts:** `./prompts`")
st.write(f"**Estado de la API:** {'Conectado' if os.getenv('OPENAI_API_KEY') else 'Error (Sin Key)'}")

if st.button("Guardar Configuración"):
    st.success("Configuración guardada (Simulada para este entorno)")
