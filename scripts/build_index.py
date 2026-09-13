from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.loaders.pdf_loader import load_documents_from_directory
from app.rag.chunking import chunk_loaded_pages
from app.rag.vector_store import index_chunks, reset_collection


def main() -> None:
    settings = get_settings()

    print(f"Cargando PDFs desde: {settings.data_dir}")
    pages = load_documents_from_directory(settings.data_dir)
    print(f"Páginas cargadas: {len(pages)}")

    print("Generando chunks semánticamente conscientes...")
    chunks = chunk_loaded_pages(pages)
    print(f"Chunks generados: {len(chunks)}")

    print("Reiniciando colección Chroma (métrica cosine)...")
    reset_collection(persist_dir=settings.vectorstore_dir)

    print("Indexando chunks en Chroma...")
    indexed = index_chunks(chunks, persist_dir=settings.vectorstore_dir)

    print(f"Chunks indexados: {indexed}")
    print(f"Vectorstore persistido en: {settings.vectorstore_dir}")
    print("Índice construido correctamente.")


if __name__ == "__main__":
    main()
