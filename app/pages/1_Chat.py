import streamlit as st
import os
import sys

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rag_engine import RAGEngine
from app.utils.styling import apply_custom_styling
from app.utils.session import init_session_state, clear_chat_history
from app.components.chat_message import display_chat_message
from app.components.citation import format_apa_citation

st.set_page_config(page_title="Chat - Research Copilot", page_icon="💬", layout="centered")

# Inicializar y Estilizar
init_session_state()
apply_custom_styling()

st.title("💬 Chat Académico")

# Sidebar para elegir la estrategia
with st.sidebar:
    st.header("Configuración")
    st.session_state.strategy = st.selectbox(
        "Estrategia de Prompt",
        options=["v1", "v2", "v3", "v4"],
        index=["v1", "v2", "v3", "v4"].index(st.session_state.strategy),
        format_func=lambda x: {
            "v1": "V1: Delimitadores",
            "v2": "V2: JSON Output",
            "v3": "V3: Few-Shot",
            "v4": "V4: Chain of Thought"
        }[x]
    )
    st.info(f"Usando estrategia: {st.session_state.strategy}")

# Inicializar el motor RAG
@st.cache_resource
def get_rag_engine():
    catalog_path = os.path.join(os.path.dirname(__file__), "..", "..", "paper_catalog.json")
    return RAGEngine(catalog_path=catalog_path)

try:
    engine = get_rag_engine()
except Exception as e:
    st.error(f"Error al inicializar el motor RAG: {e}")
    st.stop()

# Botón para limpiar historial
if st.button("Limpiar Historial"):
    clear_chat_history()
    st.rerun()

# Mostrar mensajes previos
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu pregunta académica aquí..."):
    # Agregar mensaje de usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    display_chat_message("user", prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos..."):
            answer, citations = engine.query(prompt, strategy=st.session_state.strategy)
            st.markdown(answer)
            
            if citations:
                st.info(f"**Citas:** {', '.join(citations)}")

    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": answer})
