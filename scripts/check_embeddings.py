from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.loaders.pdf_loader import load_documents_from_directory
from app.rag.chunking import chunk_loaded_pages
from app.rag.embeddings import DEFAULT_EMBEDDING_MODEL, embed_query, embed_texts

DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    pages = load_documents_from_directory(DATA_DIR)
    chunks = chunk_loaded_pages(pages)

    sample_chunks = chunks[:3]
    sample_texts = [chunk.text for chunk in sample_chunks]

    print(f"Modelo de embeddings: {DEFAULT_EMBEDDING_MODEL}")
    print(f"Páginas cargadas: {len(pages)}")
    print(f"Chunks disponibles: {len(chunks)}")
    print(f"Chunks usados en prueba: {len(sample_texts)}")
    print("-" * 80)

    vectors = embed_texts(sample_texts)
    query_vector = embed_query("¿Qué principios arquitectónicos guían los microservicios?")

    print(f"Embeddings generados: {len(vectors)}")

    if vectors:
        print(f"Dimensión del primer embedding: {len(vectors[0])}")
        print(f"Primeros 8 valores del primer embedding: {vectors[0][:8]}")

    print(f"Dimensión del embedding de consulta: {len(query_vector)}")
    print("-" * 80)
    print("Prueba de embeddings completada correctamente.")


if __name__ == "__main__":
    main()