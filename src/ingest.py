import json
import os
from loguru import logger
from src.ingestion.pdf_extractor import PDFExtractor
from src.ingestion.text_cleaner import TextCleaner

# Configurar el directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

def load_catalog(catalog_path: str):
    """
    Carga el catálogo de artículos desde el archivo JSON.
    """
    if not os.path.exists(catalog_path):
        logger.error(f"Catálogo no encontrado: {catalog_path}")
        raise FileNotFoundError(f"Catálogo no encontrado: {catalog_path}")
    
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_ingestion():
    """
    Procesa todos los artículos definidos en el catálogo.
    """
    catalog_path = os.path.join(PROJECT_ROOT, "paper_catalog.json")
    papers_dir = PROJECT_ROOT
    output_dir = os.path.join(PROJECT_ROOT, "processed_data")

    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    try:
        catalog = load_catalog(catalog_path)
        papers = catalog.get("papers", [])
        
        logger.info(f"Iniciando procesamiento de {len(papers)} artículos...")
        
        extractor = PDFExtractor(papers_dir=papers_dir)
        cleaner = TextCleaner()

        processed_count = 0
        for paper in papers:
            filename = paper.get("filename")
            paper_id = paper.get("id")
            
            if not filename or filename == "N/A":
                logger.warning(f"Saltando artículo {paper_id} (sin archivo PDF asociado).")
                continue

            try:
                # 1. Extraer texto
                raw_text = extractor.extract_text(filename)
                
                # 2. Limpiar texto
                clean_text = cleaner.clean(raw_text)
                
                # 3. Guardar texto procesado
                output_filename = f"{paper_id}_processed.txt"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(clean_text)
                
                logger.success(f"Artículo {paper_id} procesado y guardado en: {output_filename}")
                processed_count += 1
            except Exception as e:
                logger.error(f"Error procesando {filename}: {str(e)}")

        logger.info(f"Procesamiento completado. Artículos procesados: {processed_count}/{len(papers)}")

    except Exception as e:
        logger.critical(f"Error fatal en el proceso de ingesta: {str(e)}")

if __name__ == "__main__":
    # Configuración de logs básica si se ejecuta directamente
    logger.add("ingestion.log", rotation="1 MB", level="INFO")
    run_ingestion()
