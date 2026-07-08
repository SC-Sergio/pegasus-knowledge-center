import streamlit as st

st.set_page_config(
    page_title="Pegasus Engineering Knowledge Center",
    page_icon="🧠",
    layout="wide"
)

st.title("Pegasus Engineering Knowledge Center")
st.caption("Copiloto interno de documentación técnica para equipos de ingeniería, SRE y DevOps.")

st.info("Paso 1 completado: la aplicación base está funcionando localmente.")

question = st.text_input("Haz una pregunta de prueba:")

if question:
    st.write("Pregunta recibida:", question)
    st.warning("El motor RAG todavía no está implementado. Este paso solo valida la app base.")
