import os
import chromadb
from chromadb.utils import embedding_functions
from loguru import logger
from dotenv import load_dotenv

# Cargar variables de entorno (para la API Key de OpenAI)
load_dotenv()

class ChromaStore:
    """
    Clase para gestionar la base de datos vectorial ChromaDB.
    """

    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "papers_collection"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Configurar la función de embedding de OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY no encontrada en las variables de entorno.")
            raise ValueError("OPENAI_API_KEY no configurada.")

        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )

        # Inicializar el cliente persistente
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Obtener o crear la colección
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )
        logger.info(f"Conectado a la colección de ChromaDB: {self.collection_name}")

    def add_chunks(self, chunks: list, ids: list, metadatas: list):
        """
        Agrega fragmentos de texto a la colección.
        """
        logger.info(f"Agregando {len(chunks)} fragmentos a la base de datos vectorial...")
        try:
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
            logger.success(f"Éxito al agregar {len(chunks)} fragmentos.")
        except Exception as e:
            logger.error(f"Error al agregar fragmentos a ChromaDB: {str(e)}")
            raise

    def query(self, query_text: str, n_results: int = 5):
        """
        Realiza una búsqueda de similitud en la colección.
        """
        logger.info(f"Realizando consulta: '{query_text}'")
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    # Prueba rápida (requiere API KEY válida)
    try:
        store = ChromaStore()
        print("Conexión exitosa a ChromaDB.")
    except Exception as e:
        print(f"Error en la prueba: {e}")
