from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import get_settings
from app.rag.llm import generate_answer_with_gemini
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


@dataclass(frozen=True)
class RagAnswer:
    question: str
    answer: str
    sources: list[RagSource]
    context: str
    abstained: bool = False


def normalize_question(question: str) -> str:
    settings = get_settings()
    normalized = " ".join((question or "").split())

    if not normalized:
        raise ValueError("La pregunta no puede estar vacía.")

    if len(normalized) > settings.max_question_chars:
        raise ValueError(
            f"La pregunta supera el máximo de {settings.max_question_chars} caracteres."
        )

    return normalized


def build_rag_context(
    question: str,
    persist_dir: str | Path | None = None,
    top_k: int | None = None,
    max_distance: float | None = None,
) -> RagContext:
    normalized_question = normalize_question(question)

    matches = search_similar_chunks(
        query=normalized_question,
        persist_dir=persist_dir,
        top_k=top_k,
        max_distance=max_distance,
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
                    f"Distancia coseno: {source.distance:.4f}",
                    "Contenido:",
                    source.text,
                ]
            )
        )

    context = "\n\n---\n\n".join(context_blocks)

    return RagContext(
        question=normalized_question,
        context=context,
        sources=sources,
    )


def answer_question(
    question: str,
    persist_dir: str | Path | None = None,
    top_k: int | None = None,
    max_distance: float | None = None,
) -> RagAnswer:
    rag_context = build_rag_context(
        question=question,
        persist_dir=persist_dir,
        top_k=top_k,
        max_distance=max_distance,
    )

    if not rag_context.sources:
        return RagAnswer(
            question=rag_context.question,
            answer=(
                "No encontré evidencia suficientemente relevante en la documentación "
                "cargada para responder esta pregunta con confianza."
            ),
            sources=[],
            context="",
            abstained=True,
        )

    answer = generate_answer_with_gemini(
        question=rag_context.question,
        context=rag_context.context,
    )

    return RagAnswer(
        question=rag_context.question,
        answer=answer,
        sources=rag_context.sources,
        context=rag_context.context,
        abstained=False,
    )
