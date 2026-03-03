def format_apa_citation(paper_id, catalog_data, page=None):
    """
    Genera una cita APA (Autor, Año) basada en el catálogo.
    """
    paper = catalog_data.get(paper_id)
    if not paper:
        return f"({paper_id}, n.d.)"
    
    authors = paper.get("authors", [])
    year = paper.get("year", "n.d.")
    
    if not authors:
        author_str = "Anónimo"
    elif len(authors) > 2:
        author_str = f"{authors[0]} et al."
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    else:
        author_str = authors[0]
        
    citation = f"({author_str}, {year})"
    if page:
        citation = f"({author_str}, {year}, p. {page})"
    
    return citation

def format_full_reference(paper):
    """
    Genera la referencia completa estilo APA para una lista bibliográfica.
    """
    authors = paper.get("authors", [])
    if not authors:
        auth_part = "Anónimo."
    elif len(authors) > 2:
        auth_part = f"{authors[0]}, et al."
    elif len(authors) == 2:
        auth_part = f"{authors[0]}, & {authors[1]}."
    else:
        auth_part = f"{authors[0]}."
        
    title = paper.get("title", "")
    journal = paper.get("journal", "")
    year = paper.get("year", "n.d.")
    
    return f"{auth_part} ({year}). *{title}*. {journal}."
