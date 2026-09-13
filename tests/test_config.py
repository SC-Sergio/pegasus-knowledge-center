from app import config


def test_settings_resolve_project_relative_paths(monkeypatch):
    monkeypatch.setenv("DATA_DIR", "data/raw")
    monkeypatch.setenv("VECTORSTORE_DIR", "vectorstore/chroma")
    config.get_settings.cache_clear()

    settings = config.get_settings()

    assert settings.data_dir.is_absolute()
    assert settings.vectorstore_dir.is_absolute()
    assert settings.rag_top_k >= 1

    config.get_settings.cache_clear()
