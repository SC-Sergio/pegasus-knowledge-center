from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import get_settings


@lru_cache(maxsize=2)
def get_embedding_model(model_name: str | None = None) -> SentenceTransformer:
    resolved_name = model_name or get_settings().embedding_model
    return SentenceTransformer(resolved_name)


def embed_texts(
    texts: list[str],
    model_name: str | None = None,
) -> list[list[float]]:
    if not texts:
        return []

    model = get_embedding_model(model_name)
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def embed_query(query: str, model_name: str | None = None) -> list[float]:
    vectors = embed_texts([query], model_name=model_name)
    return vectors[0] if vectors else []
