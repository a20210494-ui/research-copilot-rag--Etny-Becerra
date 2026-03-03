import streamlit as st
import os
import sys

# Agregar el directorio raíz al path para poder importar desde app.utils
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.utils.styling import apply_custom_styling
from app.utils.session import init_session_state

st.set_page_config(
    page_title="Research Copilot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado y aplicar estilo
init_session_state()
apply_custom_styling()

st.markdown('<div class="main-title">📚 Research Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu Asistente Inteligente para la Investigación Académica</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Recuperación Inteligente</h3>
        <p>Utiliza RAG (Retrieval-Augmented Generation) para encontrar información precisa dentro de tu catálogo de 20 artículos.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>✍️ Citas APA Directas</h3>
        <p>Todas las respuestas incluyen referencias automáticas para asegurar el rigor académico de tus consultas.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Analítica de Datos</h3>
        <p>Visualiza la distribución de tus fuentes y el consumo de recursos del sistema en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("""
### Cómo empezar
1. Selecciona **Chat** en la barra lateral para comenzar a preguntar.
2. Explora el catálogo en **Papers**.
3. Revisa las estadísticas en **Analytics**.

---
*Desarrollado para el curso de Inteligencia Artificial Aplicada.*
""")
