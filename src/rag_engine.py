import os
import json
from loguru import logger
from openai import OpenAI
from src.vectorstore.chroma_store import ChromaStore
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class RAGEngine:
    """
    Motor RAG para recuperar contexto y generar respuestas con citas APA.
    """

    def __init__(self, catalog_path: str = "paper_catalog.json"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.store = ChromaStore(persist_directory="./chroma_db", collection_name="papers_collection")
        self.catalog = self._load_catalog(catalog_path)

    def _load_catalog(self, catalog_path: str):
        if not os.path.exists(catalog_path):
            logger.error(f"Catálogo no encontrado: {catalog_path}")
            return {}
        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Indexar por paper_id para búsqueda rápida
            return {p["id"]: p for p in data.get("papers", [])}

    def _get_apa_citation(self, paper_id: str):
        paper = self.catalog.get(paper_id)
        if not paper:
            return f"[{paper_id}]"
        
        authors = paper.get("authors", [])
        year = paper.get("year", "n.d.")
        
        if len(authors) > 2:
            author_str = f"{authors[0]} et al."
        elif len(authors) == 2:
            author_str = f"{authors[0]} & {authors[1]}"
        elif len(authors) == 1:
            author_str = authors[0]
        else:
            author_str = "Unknown"
            
        return f"({author_str}, {year})"

    def _load_prompt_template(self, strategy: str):
        mapping = {
            "v1": "v1_delimiters.txt",
            "v2": "v2_json_output.txt",
            "v3": "v3_few_shot.txt",
            "v4": "v4_chain_of_thought.txt"
        }
        filename = mapping.get(strategy, "v1_delimiters.txt")
        # Ajustar ruta relativa a la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base_dir, "prompts", filename)
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            logger.warning(f"Template {path} no encontrado, usando backup.")
            return "CONTEXT: {context}\nQUESTION: {question}\nANSWER:"

    def query(self, query_text: str, strategy: str = "v1"):
        """
        Consulta la base de datos y genera una respuesta aumentada usando la estrategia elegida.
        """
        # 1. Recuperar contexto
        results = self.store.query(query_text, n_results=5)
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents or (distances and distances[0] > 0.8):
            return "Lo siento, no encontré información relevante sobre ese tema en los documentos cargados.", []

        # 2. Construir contexto para el prompt
        context_parts = []
        citations = []
        for doc, meta in zip(documents, metadatas):
            paper_id = meta.get("paper_id")
            citation = self._get_apa_citation(paper_id)
            context_parts.append(f"CONTEXTO: {doc}\nFUENTE: {citation}")
            if citation not in citations:
                citations.append(citation)

        full_context = "\n\n".join(context_parts)

        # 3. Preparar prompt basado en la estrategia
        template = self._load_prompt_template(strategy)
        # Limpieza básica de placeholders si el usuario los puso entre llaves dobles en el prompt file
        prompt = template.replace("{context}", full_context).replace("{question}", query_text)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            answer = response.choices[0].message.content
            return answer, citations
        except Exception as e:
            logger.error(f"Error en la llamada a OpenAI: {str(e)}")
            return "Hubo un error al procesar tu consulta.", []

if __name__ == "__main__":
    # Prueba rápida
    engine = RAGEngine()
    res, cit = engine.query("¿Qué dice Gary Becker sobre el crimen?")
    print(res)
    print(f"Citas: {cit}")
