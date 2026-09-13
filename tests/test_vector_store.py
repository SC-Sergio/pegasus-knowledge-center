from app.rag import vector_store


class FakeCollection:
    def query(self, **kwargs):
        return {
            "documents": [["relevante", "irrelevante"]],
            "metadatas": [[
                {"source": "a.pdf", "page": 1, "chunk_index": 1},
                {"source": "b.pdf", "page": 2, "chunk_index": 1},
            ]],
            "distances": [[0.20, 0.91]],
        }


def test_search_filters_matches_over_cosine_threshold(monkeypatch):
    monkeypatch.setattr(
        vector_store,
        "get_or_create_collection",
        lambda **kwargs: FakeCollection(),
    )
    monkeypatch.setattr(vector_store, "embed_query", lambda query: [0.1, 0.2])

    matches = vector_store.search_similar_chunks(
        "consulta",
        top_k=2,
        max_distance=0.65,
    )

    assert len(matches) == 1
    assert matches[0]["text"] == "relevante"
    assert matches[0]["distance"] == 0.20
