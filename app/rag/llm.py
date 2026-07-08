from pathlib import Path
import os
import sys

from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


DEFAULT_LLM_MODEL = "gemini-2.5-flash"


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        raise RuntimeError("Falta configurar GEMINI_API_KEY en el archivo .env")

    return genai.Client(api_key=api_key)


def generate_answer_with_gemini(
    question: str,
    context: str,
    model_name: str | None = None,
) -> str:
    model = model_name or os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)
    client = get_gemini_client()

    prompt = f"""
Eres Pegasus Engineering Knowledge Center, un agente RAG interno para equipos de
ingeniería, SRE, DevOps y desarrollo de software.

Debes responder la pregunta del usuario usando únicamente el contexto recuperado
desde la documentación interna.

REGLAS OBLIGATORIAS:
1. Responde siempre en español.
2. No inventes información.
3. No uses conocimiento externo.
4. Si el contexto no contiene información suficiente, dilo claramente.
5. Si una fuente no aporta evidencia directa para la pregunta, no la uses en la respuesta.
6. Cita las fuentes usadas con este formato:
   - Fuente N: Nombre del documento, página X.
7. No menciones chunks ni distancia semántica en la respuesta final, salvo que el usuario lo pida.
8. Mantén un tono técnico, claro y profesional.
9. Evita respuestas excesivamente largas.
10. Usa Markdown para ordenar la respuesta.

FORMATO DE RESPUESTA:
### Respuesta

Entrega la respuesta directa a la pregunta.

### Evidencia utilizada

Lista solo las fuentes que realmente respaldan la respuesta.

### Nota de alcance

Indica brevemente si la respuesta está totalmente respaldada por el contexto o si faltan datos.

PREGUNTA DEL USUARIO:
{question}

CONTEXTO RECUPERADO:
{context}

RESPUESTA FINAL:
""".strip()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text or "No se pudo generar una respuesta."