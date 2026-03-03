import re
import unicodedata
from loguru import logger

class TextCleaner:
    """
    Clase para limpiar y normalizar texto extraído de PDFs.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Limpia el texto: normaliza espacios, elimina saltos de línea innecesarios
        y maneja caracteres especiales.
        """
        if not text:
            return ""

        # Normalizar caracteres Unicode (por ejemplo, ligaduras como 'fi')
        text = unicodedata.normalize("NFKC", text)

        # Eliminar saltos de línea que ocurren en medio de una oración (guiones al final de línea)
        text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

        # Reemplazar saltos de línea simples por espacios (pero mantener párrafos dobles)
        # Primero, marcamos los párrafos dobles
        text = re.sub(r"\n\s*\n", "[[PARAGRAPH]]", text)
        # Reemplazamos saltos de línea simples por espacios
        text = re.sub(r"\n", " ", text)
        # Restauramos los párrafos
        text = re.sub(r"\[\[PARAGRAPH\]\]", "\n\n", text)

        # Eliminar espacios múltiples
        text = re.sub(r"\s+", " ", text)
        
        # Eliminar espacios al inicio y final
        text = text.strip()

        logger.debug(f"Texto limpiado: {len(text)} caracteres resultantes.")
        return text

if __name__ == "__main__":
    # Prueba rápida
    dirty_text = "Esta es una prue- \nba de limpieza. \n\n Con múl- \ntiples líneas y   espacios."
    cleaner = TextCleaner()
    print(f"Original: {dirty_text}")
    print(f"Limpio: {cleaner.clean(dirty_text)}")
