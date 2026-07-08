from dataclasses import dataclass

from app.loaders.pdf_loader import LoadedPage


@dataclass(frozen=True)
class TextChunk:
    source: str
    path: str
    page: int
    chunk_index: int
    text: str


def split_text_by_size(text: str, chunk_size: int = 1200, chunk_overlap: int = 180) -> list[str]:
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap no puede ser negativo.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size.")

    chunks: list[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def chunk_loaded_pages(
    pages: list[LoadedPage],
    chunk_size: int = 1200,
    chunk_overlap: int = 180,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []

    for page in pages:
        page_chunks = split_text_by_size(
            page.text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for index, chunk_text in enumerate(page_chunks, start=1):
            chunks.append(
                TextChunk(
                    source=page.source,
                    path=page.path,
                    page=page.page,
                    chunk_index=index,
                    text=chunk_text,
                )
            )

    return chunks