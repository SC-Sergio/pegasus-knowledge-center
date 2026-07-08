from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class LoadedPage:
    source: str
    path: str
    page: int
    text: str


def clean_text(text: str) -> str:
    return " ".join((text or "").split())


def list_pdf_files(data_dir: str | Path) -> list[Path]:
    base_dir = Path(data_dir)
    return sorted(base_dir.glob("*.pdf"))


def load_pdf_pages(pdf_path: str | Path) -> list[LoadedPage]:
    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))

    loaded_pages: list[LoadedPage] = []

    for index, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")

        if not text:
            continue

        loaded_pages.append(
            LoadedPage(
                source=pdf_path.name,
                path=str(pdf_path),
                page=index,
                text=text,
            )
        )

    return loaded_pages


def load_documents_from_directory(data_dir: str | Path) -> list[LoadedPage]:
    loaded_pages: list[LoadedPage] = []

    for pdf_file in list_pdf_files(data_dir):
        loaded_pages.extend(load_pdf_pages(pdf_file))

    return loaded_pages