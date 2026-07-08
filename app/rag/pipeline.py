from dataclasses import dataclass
from pathlib import Path

from app.rag.vector_store import search_similar_chunks


@dataclass(frozen=True)
class RagSource:
    source: str
    page: int
    chunk_index: int
    distance: float
    text: str


@dataclass(frozen=True)
class RagContext:
    question: str
    context: str
    sources: list[RagSource]


def build_rag_context(
    question: str,
    persist_dir: str | Path = "vectorstore/chroma",
    top_k: int = 4,
) -> RagContext:
    matches = search_similar_chunks(
        query=question,
        persist_dir=persist_dir,
        top_k=top_k,
    )

    sources: list[RagSource] = []

    for match in matches:
        metadata = match["metadata"]

        sources.append(
            RagSource(
                source=str(metadata.get("source", "Fuente desconocida")),
                page=int(metadata.get("page", 0)),
                chunk_index=int(metadata.get("chunk_index", 0)),
                distance=float(match["distance"]),
                text=str(match["text"]),
            )
        )

    context_blocks = []

    for index, source in enumerate(sources, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"[Fuente {index}]",
                    f"Documento: {source.source}",
                    f"Página: {source.page}",
                    f"Chunk: {source.chunk_index}",
                    f"Distancia: {source.distance:.4f}",
                    "Contenido:",
                    source.text,
                ]
            )
        )

    context = "\n\n---\n\n".join(context_blocks)

    return RagContext(
        question=question,
        context=context,
        sources=sources,
    )