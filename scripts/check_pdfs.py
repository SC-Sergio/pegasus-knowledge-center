from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.loaders.pdf_loader import list_pdf_files, load_documents_from_directory

DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    pdf_files = list_pdf_files(DATA_DIR)

    if not pdf_files:
        print("No se encontraron PDFs en data/raw.")
        return

    pages = load_documents_from_directory(DATA_DIR)

    print(f"PDFs encontrados: {len(pdf_files)}")
    print(f"Páginas con texto extraídas: {len(pages)}")
    print("-" * 80)

    for pdf_file in pdf_files:
        pdf_pages = [page for page in pages if page.source == pdf_file.name]
        first_page = pdf_pages[0] if pdf_pages else None

        print(f"Archivo: {pdf_file.name}")
        print(f"Páginas con texto: {len(pdf_pages)}")

        if first_page:
            print(f"Muestra página {first_page.page}: {first_page.text[:500]}")
        else:
            print("Muestra: sin texto extraíble.")

        print("-" * 80)


if __name__ == "__main__":
    main()