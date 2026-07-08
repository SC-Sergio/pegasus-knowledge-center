from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.pipeline import answer_question

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "chroma"

st.set_page_config(
    page_title="Pegasus Engineering Knowledge Center",
    page_icon="🧠",
    layout="wide",
)

st.title("Pegasus Engineering Knowledge Center")
st.caption(
    "Copiloto interno de documentación técnica para equipos de ingeniería, SRE y DevOps."
)

with st.sidebar:
    st.header("Knowledge Base")
    st.success("Índice vectorial listo")
    st.caption("Fuente: PDFs técnicos en data/raw")
    st.divider()
    st.markdown("**Modo actual:** RAG con respuesta generativa")
    st.markdown("**Vector store:** Chroma local")
    st.markdown("**LLM:** Gemini 2.5 Flash")
    st.divider()
    st.caption("Pipeline: PDF → chunks → embeddings → Chroma → Gemini")

st.info(
    "Esta versión recupera contexto desde los PDFs, genera una respuesta con Gemini "
    "y muestra las fuentes utilizadas."
)

question = st.text_area(
    "Pregunta para la base de conocimiento",
    placeholder="Ejemplo: ¿Qué principios arquitectónicos guían los microservicios?",
    height=120,
)

top_k = st.slider(
    "Cantidad de fuentes a recuperar",
    min_value=1,
    max_value=8,
    value=4,
)

if st.button("Responder con IA", type="primary"):
    if not question.strip():
        st.warning("Escribe una pregunta antes de buscar.")
    else:
        with st.spinner("Consultando documentación y generando respuesta con Gemini..."):
            result = answer_question(
                question=question,
                persist_dir=VECTORSTORE_DIR,
                top_k=top_k,
            )

        st.subheader("Respuesta del agente")
        st.markdown(result.answer)

        st.subheader("Fuentes utilizadas")

        if not result.sources:
            st.error("No se encontraron fuentes relevantes.")
        else:
            for index, source in enumerate(result.sources, start=1):
                with st.expander(
                    f"Fuente {index}: {source.source} · Página {source.page} · Chunk {source.chunk_index}",
                    expanded=index == 1,
                ):
                    st.caption(f"Distancia semántica: {source.distance:.4f}")
                    st.write(source.text)

            with st.expander("Ver contexto completo enviado al LLM"):
                st.text_area(
                    "Contexto RAG",
                    value=result.context,
                    height=320,
                )