from pathlib import Path

import chromadb

from app.rag.chunking import TextChunk
from app.rag.embeddings import embed_query, embed_texts


DEFAULT_COLLECTION_NAME = "pegasus_knowledge"


def get_chroma_client(persist_dir: str | Path = "vectorstore/chroma"):
    persist_path = Path(persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_path))


def get_or_create_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path = "vectorstore/chroma",
):
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name=collection_name)


def build_chunk_id(chunk: TextChunk) -> str:
    safe_source = chunk.source.replace(" ", "_").replace("/", "_").replace("\\", "_")
    return f"{safe_source}_p{chunk.page}_c{chunk.chunk_index}"


def reset_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path = "vectorstore/chroma",
) -> None:
    client = get_chroma_client(persist_dir)

    existing_names = [collection.name for collection in client.list_collections()]

    if collection_name in existing_names:
        client.delete_collection(name=collection_name)


def index_chunks(
    chunks: list[TextChunk],
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path = "vectorstore/chroma",
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
    persist_dir: str | Path = "vectorstore/chroma",
    top_k: int = 4,
) -> list[dict]:
    collection = get_or_create_collection(
        collection_name=collection_name,
        persist_dir=persist_dir,
    )

    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    matches: list[dict] = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return matches