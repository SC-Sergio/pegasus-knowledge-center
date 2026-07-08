from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.pipeline import build_rag_context

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"


def main() -> None:
    question = "¿Qué principios arquitectónicos guían los microservicios?"

    rag_context = build_rag_context(
        question=question,
        persist_dir=VECTORSTORE_DIR,
        top_k=4,
    )

    print(f"Pregunta: {rag_context.question}")
    print(f"Fuentes recuperadas: {len(rag_context.sources)}")
    print("=" * 80)

    print("CONTEXTO RAG:")
    print(rag_context.context[:3000])

    print("=" * 80)
    print("FUENTES:")
    for index, source in enumerate(rag_context.sources, start=1):
        print(
            f"{index}. {source.source} | "
            f"Página {source.page} | "
            f"Chunk {source.chunk_index} | "
            f"Distancia {source.distance:.4f}"
        )


if __name__ == "__main__":
    main()