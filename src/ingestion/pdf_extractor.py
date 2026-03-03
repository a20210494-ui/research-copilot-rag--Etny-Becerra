import os
import fitz  # PyMuPDF
from loguru import logger

class PDFExtractor:
    """
    Clase para extraer texto de archivos PDF usando PyMuPDF (fitz).
    """

    def __init__(self, papers_dir: str):
        self.papers_dir = papers_dir

    def extract_text(self, filename: str) -> str:
        """
        Extrae el texto completo de un archivo PDF.
        """
        file_path = os.path.join(self.papers_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f"Archivo no encontrado: {file_path}")
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        logger.info(f"Extrayendo texto de: {filename}")
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text += page.get_text("text") + "\n"
            
            logger.success(f"Extracción exitosa: {filename} ({len(text)} caracteres)")
            return text
        except Exception as e:
            logger.error(f"Error al extraer texto de {filename}: {str(e)}")
            raise

if __name__ == "__main__":
    # Prueba rápida
    extractor = PDFExtractor(papers_dir=".")
    try:
        # Intentar extraer de uno de los archivos existentes para probar
        sample_text = extractor.extract_text("bayer2004.pdf")
        print(sample_text[:500])
    except Exception as e:
        print(f"Error en la prueba: {e}")
