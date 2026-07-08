from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.loaders.pdf_loader import load_documents_from_directory
from app.rag.chunking import chunk_loaded_pages

DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    pages = load_documents_from_directory(DATA_DIR)
    chunks = chunk_loaded_pages(pages)

    print(f"Páginas cargadas: {len(pages)}")
    print(f"Chunks generados: {len(chunks)}")
    print("-" * 80)

    if chunks:
        first_chunk = chunks[0]
        print(f"Fuente: {first_chunk.source}")
        print(f"Página: {first_chunk.page}")
        print(f"Chunk: {first_chunk.chunk_index}")
        print(f"Tamaño texto: {len(first_chunk.text)} caracteres")
        print("Muestra:")
        print(first_chunk.text[:800])


if __name__ == "__main__":
    main()