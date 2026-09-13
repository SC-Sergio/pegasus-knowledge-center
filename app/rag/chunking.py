from __future__ import annotations

from dataclasses import dataclass

from app.loaders.pdf_loader import LoadedPage


@dataclass(frozen=True)
class TextChunk:
    source: str
    path: str
    page: int
    chunk_index: int
    text: str


def _best_split_point(text: str, lower_bound: int, upper_bound: int) -> int:
    """Busca un corte natural cercano al límite superior."""
    candidates = ("\n\n", "\n", ". ", "? ", "! ", "; ", ": ", ", ", " ")

    for separator in candidates:
        position = text.rfind(separator, lower_bound, upper_bound)
        if position >= lower_bound:
            return position + len(separator)

    return upper_bound


def split_text_by_size(
    text: str,
    chunk_size: int = 1100,
    chunk_overlap: int = 160,
) -> list[str]:
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap no puede ser negativo.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size.")

    normalized = text.strip()
    chunks: list[str] = []
    start = 0

    while start < len(normalized):
        hard_end = min(start + chunk_size, len(normalized))

        if hard_end == len(normalized):
            end = hard_end
        else:
            search_start = start + max(chunk_size // 2, chunk_overlap + 1)
            end = _best_split_point(normalized, search_start, hard_end)
            if end <= start:
                end = hard_end

        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(normalized):
            break

        next_start = max(0, end - chunk_overlap)
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks


def chunk_loaded_pages(
    pages: list[LoadedPage],
    chunk_size: int = 1100,
    chunk_overlap: int = 160,
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
