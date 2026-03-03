import streamlit as st

def apply_custom_styling():
    """
    Aplica estilos CSS personalizados y configura fuentes académicas.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300..900&display=swap');
        
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Georgia', 'Source Serif 4', serif;
        }
        
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            color: #1a365d;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .subtitle {
            font-size: 1.5rem;
            color: #2d3748;
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .feature-card {
            padding: 2rem;
            border-radius: 10px;
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
            height: 100%;
        }
        
        .chat-container {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
