import streamlit as st
import json
import os
import sys
import pandas as pd

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.utils.styling import apply_custom_styling
from app.components.paper_card import display_paper_card

st.set_page_config(page_title="Papers - Research Copilot", page_icon="📄", layout="wide")

# Estilizar
apply_custom_styling()

st.title("📄 Navegador de Artículos")

def load_catalog():
    catalog_path = os.path.join(os.path.dirname(__file__), "..", "..", "paper_catalog.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            return json.load(f).get("papers", [])
    return []

papers = load_catalog()

if not papers:
    st.warning("No se encontró el catálogo de artículos.")
    st.stop()

# Filtros en la parte superior
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("Buscar por título o autor", "")
with col2:
    years = sorted(list(set([p["year"] for p in papers])), reverse=True)
    year_filter = st.multiselect("Filtrar por año", options=years, default=years)

# Filtrado de datos
filtered_papers = [
    p for p in papers 
    if (search_query.lower() in p["title"].lower() or any(search_query.lower() in a.lower() for a in p["authors"]))
    and (p["year"] in year_filter)
]

st.write(f"Mostrando {len(filtered_papers)} de {len(papers)} artículos.")

# Mostrar como tarjetas
for paper in filtered_papers:
    display_paper_card(paper)
