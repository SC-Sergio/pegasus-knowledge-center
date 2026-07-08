from pathlib import Path
import os
import sys

from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash")

    if not api_key or api_key == "your_api_key_here":
        raise RuntimeError("Falta configurar GEMINI_API_KEY en el archivo .env")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents="Responde en una sola frase y en español: ¿qué es un sistema RAG?",
    )

    print("Modelo usado:", model_name)
    print("Respuesta de Gemini:")
    print(response.text)


if __name__ == "__main__":
    main()