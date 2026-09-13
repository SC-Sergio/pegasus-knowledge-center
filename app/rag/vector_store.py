from __future__ import annotations

from pathlib import Path

import chromadb

from app.config import get_settings
from app.rag.chunking import TextChunk
from app.rag.embeddings import embed_query, embed_texts

DEFAULT_COLLECTION_NAME = "pegasus_knowledge"
COLLECTION_CONFIGURATION = {"hnsw": {"space": "cosine"}}


def get_chroma_client(persist_dir: str | Path | None = None):
    resolved_dir = Path(persist_dir or get_settings().vectorstore_dir)
    resolved_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(resolved_dir))


def get_or_create_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path | None = None,
):
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(
        name=collection_name,
        configuration=COLLECTION_CONFIGURATION,
    )


def build_chunk_id(chunk: TextChunk) -> str:
    safe_source = (
        chunk.source.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )
    return f"{safe_source}_p{chunk.page}_c{chunk.chunk_index}"


def reset_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path | None = None,
) -> None:
    client = get_chroma_client(persist_dir)

    existing_names = [collection.name for collection in client.list_collections()]

    if collection_name in existing_names:
        client.delete_collection(name=collection_name)


def index_chunks(
    chunks: list[TextChunk],
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path | None = None,
    batch_size: int = 32,
) -> int:
    collection = get_or_create_collection(
        collection_name=collection_name,
        persist_dir=persist_dir,
    )

    total_indexed = 0

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]

        ids = [build_chunk_id(chunk) for chunk in batch]
        documents = [chunk.text for chunk in batch]
        metadatas = [
            {
                "source": chunk.source,
                "path": chunk.path,
                "page": chunk.page,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in batch
        ]

        embeddings = embed_texts(documents)

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        total_indexed += len(batch)

    return total_indexed


def search_similar_chunks(
    query: str,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path | None = None,
    top_k: int | None = None,
    max_distance: float | None = None,
) -> list[dict]:
    settings = get_settings()
    collection = get_or_create_collection(
        collection_name=collection_name,
        persist_dir=persist_dir,
    )

    query_embedding = embed_query(query)
    resolved_top_k = top_k or settings.rag_top_k
    resolved_max_distance = (
        settings.rag_max_cosine_distance
        if max_distance is None
        else max_distance
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=resolved_top_k,
        include=["documents", "metadatas", "distances"],
    )

    matches: list[dict] = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        numeric_distance = float(distance)

        if numeric_distance > resolved_max_distance:
            continue

        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": numeric_distance,
            }
        )

    return matches
