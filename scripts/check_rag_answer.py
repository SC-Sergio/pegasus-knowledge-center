from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.pipeline import answer_question

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"


def main() -> None:
    question = "¿Qué principios arquitectónicos guían los microservicios?"

    result = answer_question(
        question=question,
        persist_dir=VECTORSTORE_DIR,
        top_k=4,
    )

    print(f"Pregunta: {result.question}")
    print("=" * 80)
    print("RESPUESTA:")
    print(result.answer)
    print("=" * 80)
    print("FUENTES:")
    for index, source in enumerate(result.sources, start=1):
        print(
            f"{index}. {source.source} | "
            f"Página {source.page} | "
            f"Chunk {source.chunk_index} | "
            f"Distancia {source.distance:.4f}"
        )


if __name__ == "__main__":
    main()