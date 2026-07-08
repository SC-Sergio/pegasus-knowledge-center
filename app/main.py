from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.pipeline import answer_question
from app.rag.vector_store import get_or_create_collection

DATA_DIR = PROJECT_ROOT / "data" / "raw"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"


def count_pdf_files() -> int:
    return len(list(DATA_DIR.glob("*.pdf")))


def count_indexed_chunks() -> int:
    try:
        collection = get_or_create_collection(persist_dir=VECTORSTORE_DIR)
        return collection.count()
    except Exception:
        return 0


def get_relevance_label(distance: float) -> tuple[str, str]:
    if distance <= 0.80:
        return "Alta", "#34D399"

    if distance <= 1.10:
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
            gap: 0.35rem;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.02em;
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
            max-width: 880px;
            margin-bottom: 1rem;
        }

        .section-kicker {
            color: #7DD3FC;
            text-transform: uppercase;
            font-size: 0.75rem;
            font-weight: 900;
            letter-spacing: 0.11em;
            margin-bottom: 0.35rem;
        }

        .command-card {
            padding: 1.2rem 1.35rem;
            border-radius: 22px;
            background:
                linear-gradient(135deg, rgba(18, 26, 43, 0.96), rgba(15, 23, 42, 0.96));
            border: 1px solid rgba(125, 211, 252, 0.18);
            margin: 1rem 0 1.15rem 0;
        }

        .hint-card {
            padding: 1rem 1.15rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(92, 200, 255, 0.11), rgba(124, 92, 255, 0.10));
            border: 1px solid rgba(92, 200, 255, 0.22);
            color: #BFD5EA;
            margin-bottom: 1rem;
        }

        .evidence-header {
            padding: 0.75rem 0.9rem;
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.74);
            border: 1px solid rgba(125, 211, 252, 0.14);
            color: #D8EEFF;
            margin-bottom: 0.75rem;
        }

        .small-muted {
            color: #8EA4BB;
            font-size: 0.9rem;
            line-height: 1.55;
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

        textarea {
            border-radius: 16px !important;
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
        st.success("Índice vectorial listo")
        st.caption("Base documental técnica en `data/raw`")

        st.divider()

        st.markdown("### Estado")
        st.markdown("**Modo:** RAG generativo")
        st.markdown("**Vector store:** Chroma local")
        st.markdown("**LLM:** Gemini 2.5 Flash")
        st.markdown("**Embeddings:** Sentence Transformers")

        st.divider()

        st.markdown("### Inventario")
        st.metric("PDFs", pdf_count)
        st.metric("Chunks", indexed_chunks)

        st.divider()

        st.markdown("### Flujo")
        st.caption(
            "PDF → extracción → chunks → embeddings → Chroma → Gemini → respuesta con fuentes"
        )


def render_hero() -> None:
    st.markdown(
        """
        <div class="pegasus-shell">
            <div class="status-row">
                <span class="status-pill status-pill-ok">● Sistema RAG operativo</span>
                <span class="status-pill">Engineering Knowledge Center</span>
                <span class="status-pill">Gemini + Chroma</span>
            </div>
            <div class="main-title">Pegasus Engineering<br>Knowledge Center</div>
            <div class="subtitle">
                Copiloto interno para consultar documentación técnica de arquitectura, onboarding,
                ingeniería front-end, back-end e incidentes SRE. Recupera evidencia desde PDFs,
                genera una respuesta con IA y muestra trazabilidad por fuente.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_example_questions() -> str:
    example_questions = [
        "",
        "¿Qué debe hacer un nuevo desarrollador durante su primera semana?",
        "¿Qué responsabilidades tiene el Technical Lead durante un incidente?",
        "¿Cuáles son los tres pilares filosóficos del front-end?",
        "¿Qué significa aplicar privilegio mínimo en microservicios?",
        "¿Qué debe incluir un post-mortem?",
    ]

    return st.selectbox(
        "Pregunta sugerida",
        options=example_questions,
        index=0,
        help="Selecciona una pregunta de demo para probar el agente rápidamente.",
    )


def render_sources(result) -> None:
    st.markdown("## Evidencia documental")

    if not result.sources:
        st.error("No se encontraron fuentes relevantes.")
        return

    avg_distance = sum(source.distance for source in result.sources) / len(result.sources)
    best_source = min(result.sources, key=lambda item: item.distance)
    best_label, _ = get_relevance_label(best_source.distance)

    source_col_1, source_col_2, source_col_3 = st.columns(3)

    with source_col_1:
        st.metric("Fuentes recuperadas", len(result.sources))

    with source_col_2:
        st.metric("Distancia promedio", f"{avg_distance:.4f}")

    with source_col_3:
        st.metric("Mejor relevancia", best_label)

    st.markdown(
        """
        <div class="evidence-header">
            Las fuentes siguientes son los fragmentos recuperados desde Chroma.
            La relevancia se calcula de forma aproximada según la distancia semántica:
            menor distancia significa mayor similitud con la pregunta.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for index, source in enumerate(result.sources, start=1):
        relevance_label, relevance_color = get_relevance_label(source.distance)
        clean_title = format_source_title(source.source)

        label = (
            f"Fuente {index}: {clean_title} · "
            f"Página {source.page} · Relevancia {relevance_label}"
        )

        with st.expander(label, expanded=index == 1):
            st.markdown(
                f"""
                <div style="
                    padding: 0.85rem 1rem;
                    border-radius: 14px;
                    background: rgba(15, 23, 42, 0.65);
                    border: 1px solid rgba(125, 211, 252, 0.16);
                    margin-bottom: 0.75rem;
                ">
                    <div style="font-weight: 800; color: #F8FBFF; margin-bottom: 0.35rem;">
                        {clean_title}
                    </div>
                    <div style="color: #AFC2D8; font-size: 0.9rem;">
                        Página {source.page} · Chunk {source.chunk_index} ·
                        Distancia {source.distance:.4f}
                    </div>
                    <div style="
                        display: inline-block;
                        margin-top: 0.55rem;
                        padding: 0.22rem 0.55rem;
                        border-radius: 999px;
                        color: {relevance_color};
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        font-size: 0.82rem;
                        font-weight: 800;
                    ">
                        ● Relevancia {relevance_label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(source.text)

    with st.expander("Ver contexto completo enviado al LLM"):
        st.text_area(
            "Contexto RAG",
            value=result.context,
            height=340,
        )


st.set_page_config(
    page_title="Pegasus Engineering Knowledge Center",
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
    st.metric("Modelo activo", "Gemini 2.5 Flash")

st.markdown(
    """
    <div class="command-card">
        <div class="section-kicker">AI Command Console</div>
        <div class="small-muted">
            Formula una pregunta sobre la documentación interna. El sistema recuperará evidencia,
            construirá contexto RAG y generará una respuesta trazable.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

query_col, config_col = st.columns([2.35, 1])

with query_col:
    selected_example = render_example_questions()

    question = st.text_area(
        "Pregunta para la base de conocimiento",
        value=selected_example,
        placeholder="Ejemplo: ¿Cuáles son los tres pilares filosóficos del front-end?",
        height=130,
    )

with config_col:
    st.markdown("### Parámetros")
    top_k = st.slider(
        "Fuentes a recuperar",
        min_value=1,
        max_value=8,
        value=4,
    )

    st.markdown(
        """
        <div class="hint-card">
            <strong>Recomendación:</strong><br>
            Usa Top K = 4 para demo. Sube a 6 u 8 si la respuesta requiere más contexto.
        </div>
        """,
        unsafe_allow_html=True,
    )

run_query = st.button("Ejecutar consulta RAG", type="primary")

if run_query:
    if not question.strip():
        st.warning("Escribe una pregunta antes de consultar.")
    elif indexed_chunks == 0:
        st.error(
            "No hay chunks indexados en Chroma. Ejecuta primero: "
            "`python scripts/build_index.py`"
        )
    else:
        with st.spinner("Recuperando evidencia y generando respuesta con Gemini..."):
            try:
                result = answer_question(
                    question=question,
                    persist_dir=VECTORSTORE_DIR,
                    top_k=top_k,
                )
            except Exception as exc:
                st.error(f"No se pudo generar la respuesta: {exc}")
                st.stop()

        st.divider()

        st.markdown("## Respuesta del agente")

        with st.chat_message("assistant"):
            st.markdown(result.answer)

        render_sources(result)