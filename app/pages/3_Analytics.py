import streamlit as st
import json
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.utils.styling import apply_custom_styling

st.set_page_config(page_title="Analytics - Research Copilot", page_icon="📊", layout="wide")

# Estilizar
apply_custom_styling()

def load_catalog():
    catalog_path = os.path.join(os.path.dirname(__file__), "..", "..", "paper_catalog.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            return json.load(f).get("papers", [])
    return []

papers = load_catalog()

if not papers:
    st.warning("No hay datos suficientes para mostrar analíticas.")
    st.stop()

df = pd.DataFrame(papers)

# Distribución por año
st.subheader("Distribución de Artículos por Año")
year_counts = df['year'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
year_counts.plot(kind='bar', color='#1a365d', ax=ax)
ax.set_xlabel("Año")
ax.set_ylabel("Cantidad")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Estadísticas de Tópicos
st.subheader("Tópicos más frecuentes")
all_topics = []
for topics in df['topics']:
    all_topics.extend(topics)

topic_counts = pd.Series(all_topics).value_counts().head(10)
st.bar_chart(topic_counts)

# Simulación de uso de Tokens (Métrica del sistema)
st.divider()
st.subheader("📊 Seguimiento de Recursos del Sistema")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Uso de Tokens por Consulta (Promedio)**")
    tokens_df = pd.DataFrame({
        'Model': ['GPT-4 (Prompt)', 'GPT-4 (Completion)', 'Embedding'],
        'Tokens': [1200, 350, 512]
    })
    st.bar_chart(tokens_df.set_index('Model'))

with col2:
    st.markdown("**Carga de Contexto**")
    context_data = pd.DataFrame({
        'Tipo': ['Contexto Recuperado', 'Espacio Libre'],
        'Tokens': [2560, 5632] # Simulación de una ventana de 8k
    })
    fig2, ax2 = plt.subplots()
    ax2.pie(context_data['Tokens'], labels=context_data['Tipo'], autopct='%1.1f%%', colors=['#1a365d', '#e2e8f0'])
    st.pyplot(fig2)

st.info("Estas métricas permiten monitorear la eficiencia del pipeline RAG y los costos asociados a la API de OpenAI.")
