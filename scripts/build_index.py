from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.loaders.pdf_loader import load_documents_from_directory
from app.rag.chunking import chunk_loaded_pages
from app.rag.vector_store import index_chunks, reset_collection

DATA_DIR = PROJECT_ROOT / "data" / "raw"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"


def main() -> None:
    print("Cargando PDFs...")
    pages = load_documents_from_directory(DATA_DIR)
    print(f"Páginas cargadas: {len(pages)}")

    print("Generando chunks...")
    chunks = chunk_loaded_pages(pages)
    print(f"Chunks generados: {len(chunks)}")

    print("Reiniciando colección Chroma...")
    reset_collection(persist_dir=VECTORSTORE_DIR)

    print("Indexando chunks en Chroma...")
    indexed = index_chunks(chunks, persist_dir=VECTORSTORE_DIR)

    print(f"Chunks indexados: {indexed}")
    print(f"Vectorstore persistido en: {VECTORSTORE_DIR}")
    print("Índice construido correctamente.")


if __name__ == "__main__":
    main()