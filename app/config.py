from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _resolve_path(value: str, default: str) -> Path:
    raw = (value or default).strip()
    path = Path(raw)
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def _get_int(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} debe ser un número entero.") from exc
    if not minimum <= value <= maximum:
        raise RuntimeError(f"{name} debe estar entre {minimum} y {maximum}.")
    return value


def _get_float(name: str, default: float, minimum: float, maximum: float) -> float:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = float(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} debe ser un número.") from exc
    if not minimum <= value <= maximum:
        raise RuntimeError(f"{name} debe estar entre {minimum} y {maximum}.")
    return value


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_env: str
    data_dir: Path
    vectorstore_dir: Path
    llm_model: str
    embedding_model: str
    rag_top_k: int
    rag_max_cosine_distance: float
    max_question_chars: int


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings(
        app_name=os.getenv("APP_NAME", "Pegasus Engineering Knowledge Center").strip(),
        app_env=os.getenv("APP_ENV", "dev").strip(),
        data_dir=_resolve_path(os.getenv("DATA_DIR", ""), "data/raw"),
        vectorstore_dir=_resolve_path(
            os.getenv("VECTORSTORE_DIR", ""),
            "vectorstore/chroma",
        ),
        llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash").strip(),
        embedding_model=os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        ).strip(),
        rag_top_k=_get_int("RAG_TOP_K", 4, 1, 12),
        rag_max_cosine_distance=_get_float(
            "RAG_MAX_COSINE_DISTANCE",
            0.65,
            0.0,
            2.0,
        ),
        max_question_chars=_get_int("MAX_QUESTION_CHARS", 1200, 80, 5000),
    )
