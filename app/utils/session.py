import streamlit as st

def init_session_state():
    """
    Inicializa las variables del estado de la sesión si no existen.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "strategy" not in st.session_state:
        st.session_state.strategy = "v1"

def clear_chat_history():
    """
    Limpia el historial de mensajes.
    """
    st.session_state.messages = []
