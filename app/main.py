from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.pipeline import build_rag_context

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
    st.markdown("**Modo actual:** recuperación documental")
    st.markdown("**Vector store:** Chroma local")
    st.markdown("**LLM:** pendiente de conectar")

st.info(
    "Esta versión recupera contexto desde los PDFs y muestra fuentes. "
    "La generación final con LLM se conectará en el siguiente paso."
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

if st.button("Buscar en documentación", type="primary"):
    if not question.strip():
        st.warning("Escribe una pregunta antes de buscar.")
    else:
        with st.spinner("Buscando evidencia en la documentación técnica..."):
            rag_context = build_rag_context(
                question=question,
                persist_dir=VECTORSTORE_DIR,
                top_k=top_k,
            )

        st.subheader("Contexto recuperado")
        st.write(
            "Estos son los fragmentos más relevantes encontrados en la documentación. "
            "En el próximo paso, un LLM usará este contexto para redactar la respuesta final."
        )

        if not rag_context.sources:
            st.error("No se encontraron fuentes relevantes.")
        else:
            for index, source in enumerate(rag_context.sources, start=1):
                with st.expander(
                    f"Fuente {index}: {source.source} · Página {source.page} · Chunk {source.chunk_index}",
                    expanded=index == 1,
                ):
                    st.caption(f"Distancia semántica: {source.distance:.4f}")
                    st.write(source.text)

            st.subheader("Prompt/contexto preparado para el LLM")
            st.text_area(
                "Contexto RAG",
                value=rag_context.context,
                height=320,
            )