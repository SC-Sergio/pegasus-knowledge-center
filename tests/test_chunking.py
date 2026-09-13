from app.loaders.pdf_loader import LoadedPage
from app.rag.chunking import chunk_loaded_pages, split_text_by_size


def test_split_text_prefers_natural_boundaries_and_respects_size():
    text = (
        "Primer párrafo con una idea completa. "
        "Segunda oración relacionada con el mismo tema.\n\n"
        "Segundo párrafo con información adicional que debería quedar cerca de un corte natural. "
        "Tercera oración para forzar más de un fragmento."
    )

    chunks = split_text_by_size(text, chunk_size=110, chunk_overlap=20)

    assert len(chunks) >= 2
    assert all(chunk.strip() for chunk in chunks)
    assert all(len(chunk) <= 110 for chunk in chunks)


def test_chunk_loaded_pages_preserves_source_metadata():
    pages = [
        LoadedPage(
            source="manual.pdf",
            path="data/raw/manual.pdf",
            page=7,
            text="Texto suficientemente largo. " * 20,
        )
    ]

    chunks = chunk_loaded_pages(pages, chunk_size=120, chunk_overlap=20)

    assert chunks
    assert all(chunk.source == "manual.pdf" for chunk in chunks)
    assert all(chunk.page == 7 for chunk in chunks)
    assert [chunk.chunk_index for chunk in chunks] == list(range(1, len(chunks) + 1))
