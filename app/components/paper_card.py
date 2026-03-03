import streamlit as st

def display_paper_card(paper):
    """
    Muestra una tarjeta informativa para un artículo académico.
    """
    title = paper.get('title', 'Sin título')
    year = paper.get('year', 'N/A')
    
    with st.expander(f"**{title}** ({year})"):
        authors = paper.get('authors', [])
        st.write(f"**Autores:** {', '.join(authors)}")
        
        # Intentar obtener Journal o Venue
        journal = paper.get('journal') or paper.get('venue', 'Información no disponible')
        st.write(f"**Journal/Venue:** {journal}")
        
        st.write(f"**DOI:** {paper.get('doi', 'N/A')}")
        
        topics = paper.get('topics', [])
        st.write(f"**Tópicos:** {', '.join(topics) if topics else 'N/A'}")
        
        st.write(f"**Archivo:** `{paper.get('filename', 'N/A')}`")
