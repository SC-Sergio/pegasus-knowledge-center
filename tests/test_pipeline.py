import pytest

from app.rag import pipeline


def test_relevance_gate_abstains_without_calling_llm(monkeypatch):
    monkeypatch.setattr(pipeline, "search_similar_chunks", lambda **kwargs: [])

    def fail_if_called(**kwargs):
        raise AssertionError("El LLM no debe invocarse sin evidencia relevante.")

    monkeypatch.setattr(pipeline, "generate_answer_with_gemini", fail_if_called)

    result = pipeline.answer_question("¿Cuál fue el resultado del partido de ayer?")

    assert result.abstained is True
    assert result.sources == []
    assert "evidencia suficientemente relevante" in result.answer


def test_answer_question_uses_filtered_sources(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "search_similar_chunks",
        lambda **kwargs: [
            {
                "text": "El Technical Lead coordina la investigación técnica.",
                "metadata": {
                    "source": "incidentes.pdf",
                    "page": 6,
                    "chunk_index": 2,
                },
                "distance": 0.18,
            }
        ],
    )
    monkeypatch.setattr(
        pipeline,
        "generate_answer_with_gemini",
        lambda **kwargs: "Respuesta basada en la evidencia.",
    )

    result = pipeline.answer_question("¿Qué hace el Technical Lead?")

    assert result.abstained is False
    assert result.answer == "Respuesta basada en la evidencia."
    assert len(result.sources) == 1
    assert result.sources[0].distance == pytest.approx(0.18)
    assert "incidentes.pdf" in result.context


def test_normalize_question_rejects_empty_input():
    with pytest.raises(ValueError, match="no puede estar vacía"):
        pipeline.normalize_question("   ")
