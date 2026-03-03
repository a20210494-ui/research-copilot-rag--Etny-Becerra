import streamlit as st

def display_chat_message(role, content):
    """
    Muestra un mensaje de chat con el rol y contenido especificados.
    """
    with st.chat_message(role):
        st.markdown(content)
