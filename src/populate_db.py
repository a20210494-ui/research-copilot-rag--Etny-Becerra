import os
from loguru import logger
from src.chunking.chunker import Chunker
from src.vectorstore.chroma_store import ChromaStore

# Configuración de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "processed_data")

def populate():
    """
    Lee los archivos procesados, los divide en fragmentos y los guarda en ChromaDB.
    """
    if not os.path.exists(PROCESSED_DATA_DIR):
        logger.error(f"Directorio de datos procesados no encontrado: {PROCESSED_DATA_DIR}")
        return

    # Inicializar componentes
    chunker = Chunker(chunk_size=512, chunk_overlap=50)
    store = ChromaStore(persist_directory="./chroma_db", collection_name="papers_collection")

    files = [f for f in os.listdir(PROCESSED_DATA_DIR) if f.endswith(".txt")]
    logger.info(f"Encontrados {len(files)} archivos para procesar.")

    for filename in files:
        paper_id = filename.replace("_processed.txt", "")
        file_path = os.path.join(PROCESSED_DATA_DIR, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"Archivo vacío: {filename}")
                continue

            # 1. Crear fragmentos (chunks)
            chunks = chunker.chunk_text(content)
            
            # 2. Preparar IDs y Metadatos para ChromaDB
            ids = [f"{paper_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"paper_id": paper_id, "chunk_index": i} for i in range(len(chunks))]

            # 3. Guardar en ChromaDB
            store.add_chunks(chunks=chunks, ids=ids, metadatas=metadatas)
            logger.success(f"Procesado y guardado: {paper_id} ({len(chunks)} chunks)")

        except Exception as e:
            logger.error(f"Error procesando {filename}: {str(e)}")

    logger.info("Proceso de población de base de datos vectorial finalizado.")

if __name__ == "__main__":
    populate()
