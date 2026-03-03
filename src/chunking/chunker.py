import tiktoken
from loguru import logger
from typing import List

class Chunker:
    """
    Clase para dividir texto en fragmentos (chunks) usando tiktoken.
    """

    def __init__(self, model_name: str = "gpt-4", chunk_size: int = 512, chunk_overlap: int = 50):
        self.tokenizer = tiktoken.encoding_for_model(model_name)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Divide el texto en fragmentos de tamaño fijo (en tokens) con un solapamiento definido.
        """
        if not text:
            return []

        tokens = self.tokenizer.encode(text)
        num_tokens = len(tokens)
        logger.debug(f"Total de tokens a fragmentar: {num_tokens}")

        chunks = []
        for i in range(0, num_tokens, self.chunk_size - self.chunk_overlap):
            # Extraer el fragmento de tokens
            chunk_tokens = tokens[i : i + self.chunk_size]
            
            # Decodificar de nuevo a texto
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)

            # Si ya llegamos al final de los tokens, detenemos el bucle
            if i + self.chunk_size >= num_tokens:
                break

        logger.info(f"Creados {len(chunks)} fragmentos del texto.")
        return chunks

if __name__ == "__main__":
    # Prueba rápida
    sample_text = "Este es un texto de prueba para verificar el funcionamiento del Chunker. " * 50
    chunker = Chunker(chunk_size=20, chunk_overlap=5)
    result = chunker.chunk_text(sample_text)
    for idx, c in enumerate(result[:3]):
        print(f"Chunk {idx+1}: {c[:100]}...")
