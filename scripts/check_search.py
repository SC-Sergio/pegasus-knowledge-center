from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.vector_store import search_similar_chunks

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"


def main() -> None:
    query = "¿Qué principios arquitectónicos guían los microservicios?"

    print(f"Pregunta: {query}")
    print("-" * 80)

    matches = search_similar_chunks(
        query=query,
        persist_dir=VECTORSTORE_DIR,
        top_k=4,
    )

    if not matches:
        print("No se encontraron resultados.")
        return

    for index, match in enumerate(matches, start=1):
        metadata = match["metadata"]
        distance = match["distance"]

        print(f"Resultado {index}")
        print(f"Fuente: {metadata.get('source')}")
        print(f"Página: {metadata.get('page')}")
        print(f"Chunk: {metadata.get('chunk_index')}")
        print(f"Distancia: {distance}")
        print("Texto:")
        print(match["text"][:700])
        print("-" * 80)


if __name__ == "__main__":
    main()