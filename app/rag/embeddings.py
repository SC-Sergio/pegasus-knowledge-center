from functools import lru_cache

from sentence_transformers import SentenceTransformer


DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def get_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL) -> SentenceTransformer:
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str], model_name: str = DEFAULT_EMBEDDING_MODEL) -> list[list[float]]:
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


def embed_query(query: str, model_name: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
    vectors = embed_texts([query], model_name=model_name)
    return vectors[0] if vectors else []