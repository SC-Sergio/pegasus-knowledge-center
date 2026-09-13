from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.rag.pipeline import answer_question
from app.rag.vector_store import get_or_create_collection

settings = get_settings()


def count_pdf_files() -> int:
    return len(list(settings.data_dir.glob("*.pdf")))


def count_indexed_chunks() -> int:
    try:
        collection = get_or_create_collection(persist_dir=settings.vectorstore_dir)
        return collection.count()
    except Exception:
        return 0


def get_relevance_label(distance: float) -> tuple[str, str]:
    if distance <= 0.25:
        return "Alta", "#34D399"

    if distance <= 0.50:
        return "Media", "#FBBF24"

    return "Baja", "#F87171"


def format_source_title(source_name: str) -> str:
    return source_name.replace(".pdf", "")


def render_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 3rem;
            padding-bottom: 4rem;
            max-width: 1320px;
        }
        .pegasus-shell {
            padding: 1.3rem 1.5rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at top left, rgba(92, 200, 255, 0.18), transparent 34%),
                radial-gradient(circle at top right, rgba(124, 92, 255, 0.18), transparent 32%),
                linear-gradient(135deg, rgba(11, 16, 32, 0.96), rgba(15, 23, 42, 0.92));
            border: 1px solid rgba(125, 211, 252, 0.20);
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
            margin-bottom: 1.2rem;
        }
        .status-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-bottom: 1rem;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 800;
            border: 1px solid rgba(125, 211, 252, 0.24);
            background: rgba(15, 23, 42, 0.74);
            color: #D8EEFF;
        }
        .status-pill-ok {
            color: #A7F3D0;
            background: rgba(16, 185, 129, 0.13);
            border-color: rgba(16, 185, 129, 0.34);
        }
        .main-title {
            font-size: clamp(2.25rem, 5vw, 4.5rem);
            font-weight: 900;
            line-height: 0.95;
            letter-spacing: -0.065em;
            margin: 0.2rem 0 0.9rem 0;
            color: #F8FBFF;
        }
        .subtitle {
            color: #B8C7DB;
            font-size: 1.04rem;
            line-height: 1.7;
            max-width: 900px;
            margin-bottom: 1rem;
        }
        .hint-card {
            padding: 1rem 1.15rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(92, 200, 255, 0.11), rgba(124, 92, 255, 0.10));
            border: 1px solid rgba(92, 200, 255, 0.22);
            color: #BFD5EA;
            margin-bottom: 1rem;
        }
        div[data-testid="stMetric"] {
            background: rgba(18, 26, 43, 0.88);
            border: 1px solid rgba(125, 211, 252, 0.16);
            padding: 1rem 1.05rem;
            border-radius: 18px;
        }
        div[data-testid="stExpander"] {
            border: 1px solid rgba(125, 211, 252, 0.16);
            border-radius: 15px;
            overflow: hidden;
            background: rgba(15, 23, 42, 0.40);
        }
        .stButton > button {
            border-radius: 14px;
            font-weight: 800;
            min-height: 3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(pdf_count: int, indexed_chunks: int) -> None:
    with st.sidebar:
        st.markdown("## Pegasus KC")
        st.success("Índice vectorial listo" if indexed_chunks else "Índice vectorial no disponible")
        st.caption(f"Entorno: `{settings.app_env}`")

        st.divider()

        st.markdown("### Estado")
        st.markdown("**Modo:** RAG generativo")
        st.markdown("**Vector store:** Chroma / cosine")
        st.markdown(f"**LLM:** `{settings.llm_model}`")
        st.markdown("**Embeddings:** Sentence Transformers")

        st.divider()

        st.markdown("### Inventario")
        st.metric("PDFs", pdf_count)
        st.metric("Chunks", indexed_chunks)

        st.divider()

        st.caption(
            "PDF → chunks → embeddings normalizados → Chroma/cosine → "
            "relevance gate → Gemini → respuesta trazable"
        )


def render_hero() -> None:
    st.markdown(
        """
        <div class="pegasus-shell">
            <div class="status-row">
                <span class="status-pill status-pill-ok">● RAG con relevance gating</span>
                <span class="status-pill">Engineering Knowledge Center</span>
                <span class="status-pill">Gemini + Chroma</span>
            </div>
            <div class="main-title">Pegasus Engineering<br>Knowledge Center</div>
            <div class="subtitle">
                Copiloto para consultar documentación técnica con recuperación semántica,
                abstención cuando no existe evidencia suficiente y trazabilidad por documento,
                página y fragmento.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_example_questions() -> str:
    return st.selectbox(
        "Pregunta sugerida",
        options=[
            "",
            "¿Qué debe hacer un nuevo desarrollador durante su primera semana?",
            "¿Qué responsabilidades tiene el Technical Lead durante un incidente?",
            "¿Cuáles son los tres pilares filosóficos del front-end?",
            "¿Qué significa aplicar privilegio mínimo en microservicios?",
            "¿Qué debe incluir un post-mortem?",
        ],
        index=0,
        help="Selecciona una pregunta de demo para probar el agente rápidamente.",
    )


def render_sources(result) -> None:
    st.markdown("## Evidencia documental")

    if not result.sources:
        st.info("La consulta fue descartada por falta de evidencia suficientemente relevante.")
        return

    avg_distance = sum(source.distance for source in result.sources) / len(result.sources)
    best_source = min(result.sources, key=lambda item: item.distance)
    best_label, _ = get_relevance_label(best_source.distance)

    source_col_1, source_col_2, source_col_3 = st.columns(3)

    with source_col_1:
        st.metric("Fuentes aceptadas", len(result.sources))

    with source_col_2:
        st.metric("Distancia coseno media", f"{avg_distance:.4f}")

    with source_col_3:
        st.metric("Mejor relevancia", best_label)

    for index, source in enumerate(result.sources, start=1):
        relevance_label, relevance_color = get_relevance_label(source.distance)
        clean_title = format_source_title(source.source)

        label = (
            f"Fuente {index}: {clean_title} · "
            f"Página {source.page} · Relevancia {relevance_label}"
        )

        with st.expander(label, expanded=index == 1):
            source_meta = (
                f"**Documento:** {clean_title}  \n"
                f"**Página:** {source.page}  \n"
                f"**Chunk:** {source.chunk_index}  \n"
                f"**Distancia coseno:** `{source.distance:.4f}`  \n"
                f"**Relevancia:** <span style='color:{relevance_color}'>"
                f"{relevance_label}</span>"
            )
            st.markdown(source_meta, unsafe_allow_html=True)
            st.write(source.text)

    with st.expander("Ver contexto completo enviado al LLM"):
        st.text_area("Contexto RAG", value=result.context, height=340)


st.set_page_config(
    page_title=settings.app_name,
    page_icon="🧠",
    layout="wide",
)

render_css()

pdf_count = count_pdf_files()
indexed_chunks = count_indexed_chunks()

render_sidebar(pdf_count, indexed_chunks)
render_hero()

metric_col_1, metric_col_2, metric_col_3 = st.columns(3)

with metric_col_1:
    st.metric("Documentos PDF", pdf_count)

with metric_col_2:
    st.metric("Chunks indexados", indexed_chunks)

with metric_col_3:
    st.metric("Gate coseno", f"≤ {settings.rag_max_cosine_distance:.2f}")

query_col, config_col = st.columns([2.35, 1])

with query_col:
    selected_example = render_example_questions()

    question = st.text_area(
        "Pregunta para la base de conocimiento",
        value=selected_example,
        placeholder="Ejemplo: ¿Cuáles son los tres pilares filosóficos del front-end?",
        height=130,
        max_chars=settings.max_question_chars,
    )

with config_col:
    st.markdown("### Parámetros")
    top_k = st.slider(
        "Fuentes candidatas",
        min_value=1,
        max_value=8,
        value=min(settings.rag_top_k, 8),
    )

    st.markdown(
        f"""
        <div class="hint-card">
            <strong>Filtro activo:</strong><br>
            solo se envían al LLM fuentes con distancia coseno ≤
            <code>{settings.rag_max_cosine_distance:.2f}</code>.
        </div>
        """,
        unsafe_allow_html=True,
    )

run_query = st.button("Ejecutar consulta RAG", type="primary")

if run_query:
    if indexed_chunks == 0:
        st.error("No hay chunks indexados. Ejecuta `python scripts/build_index.py`.")
    else:
        with st.spinner("Recuperando evidencia y evaluando relevancia..."):
            try:
                result = answer_question(
                    question=question,
                    persist_dir=settings.vectorstore_dir,
                    top_k=top_k,
                )
            except Exception as exc:
                st.error(f"No se pudo procesar la consulta: {exc}")
                st.stop()

        st.divider()
        st.markdown("## Respuesta del agente")

        if result.abstained:
            st.warning(result.answer)
        else:
            with st.chat_message("assistant"):
                st.markdown(result.answer)

        render_sources(result)
