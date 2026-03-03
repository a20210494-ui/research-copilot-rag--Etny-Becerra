import os
import json
from loguru import logger
from src.rag_engine import RAGEngine
from tqdm import tqdm

def run_evaluation(questions_path: str = "eval/questions.json", results_path: str = "eval/results.md"):
    """
    Lee preguntas, consulta al motor RAG y guarda los resultados.
    """
    if not os.path.exists(questions_path):
        logger.error(f"Archivo de preguntas no encontrado: {questions_path}")
        return

    with open(questions_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        questions = data.get("questions", [])

    engine = RAGEngine()
    results = []

    logger.info(f"Iniciando evaluación de {len(questions)} preguntas...")

    for i, q in enumerate(tqdm(questions, desc="Evaluando")):
        answer, citations = engine.query(q)
        results.append({
            "num": i + 1,
            "question": q,
            "answer": answer,
            "citations": citations
        })

    # Guardar en Markdown
    with open(results_path, "w", encoding="utf-8") as f:
        f.write("# Reporte de Evaluación - Research Copilot\n\n")
        f.write(f"Total de preguntas evaluadas: {len(questions)}\n\n")
        
        for r in results:
            f.write(f"### Pregunta {r['num']}: {r['question']}\n")
            f.write(f"**Respuesta:** {r['answer']}\n\n")
            if r['citations']:
                f.write(f"**Citas:** {', '.join(r['citations'])}\n\n")
            f.write("---\n\n")

    logger.success(f"Evaluación completada. Resultados guardados en {results_path}")

if __name__ == "__main__":
    run_evaluation()
