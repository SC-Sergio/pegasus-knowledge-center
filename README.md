# Pegasus Engineering Knowledge Center

Agente RAG para consultar documentación técnica interna usando **Python**, **Streamlit**, **ChromaDB**, **Sentence Transformers**, **Gemini** y **Docker**.

El proyecto fue construido como Challenge Final **Alura Agente**, simulando una solución empresarial para que equipos de ingeniería, SRE y DevOps puedan hacer preguntas en lenguaje natural sobre documentos internos y recibir respuestas trazables con fuentes.

La solución utiliza el corpus **Santos Pegasus Soluciones**, provisto como material sugerido por Alura para el challenge, y construye sobre ese corpus una aplicación RAG funcional, visual, dockerizada y preparada para despliegue en Oracle Cloud Infrastructure.

---

## Vista general

**Pegasus Engineering Knowledge Center** es un copiloto interno de documentación técnica construido sobre el corpus **Santos Pegasus Soluciones**, material sugerido por Alura para el Challenge Final **Alura Agente**.

El corpus representa una empresa tecnológica ficticia especializada en desarrollo de software escalable, arquitectura de microservicios, soluciones de inteligencia artificial, ingeniería front-end/back-end, prácticas SRE y estándares de seguridad en infraestructura de nube.

El sistema permite:

- Leer documentos PDF técnicos.
- Extraer texto por página.
- Dividir el contenido en chunks.
- Generar embeddings locales.
- Guardar los vectores en ChromaDB.
- Recuperar evidencia relevante según una pregunta.
- Generar una respuesta con Gemini.
- Mostrar fuentes, páginas, chunks y relevancia semántica.
- Ejecutar la aplicación localmente o mediante Docker.

---

## Caso de uso

En una empresa tecnológica, los equipos de ingeniería, SRE, DevOps y desarrollo suelen perder tiempo buscando información en manuales, guías técnicas, protocolos de incidentes y documentación interna.

Este agente resuelve ese problema permitiendo consultas como:

- ¿Qué debe hacer un nuevo desarrollador durante su primera semana?
- ¿Qué responsabilidades tiene el Technical Lead durante un incidente?
- ¿Cuáles son los tres pilares filosóficos del front-end?
- ¿Qué significa aplicar privilegio mínimo en microservicios?
- ¿Qué debe incluir un post-mortem?

El objetivo es reducir la fricción de búsqueda documental y entregar respuestas basadas en evidencia, mostrando siempre las fuentes utilizadas.

---

## Origen del corpus documental

Este proyecto utiliza el corpus **Santos Pegasus Soluciones**, provisto como material sugerido por Alura para el Challenge Final **Alura Agente**.

Santos Pegasus Soluciones representa una empresa ficticia de tecnología especializada en:

- desarrollo de software escalable;
- arquitectura de microservicios;
- soluciones de inteligencia artificial;
- ingeniería back-end;
- ingeniería front-end;
- respuesta a incidentes;
- prácticas SRE;
- seguridad y operación en infraestructura de nube.

> Nota: los documentos representan una empresa ficticia y se utilizan con fines educativos para demostrar una solución RAG funcional. No contienen información real ni confidencial de una empresa existente.

---

## Documentos utilizados

La base de conocimiento se construye a partir de documentos PDF técnicos ubicados en:

```text
data/raw/
```

Documentos incluidos:

```text
Arquitectura de Microservicios y Mapa de Dominios.pdf
Manual de Onboarding para nuevos desarrolladores.pdf
Protocolo de respuesta a incidentes.pdf
Santo pegasus soluciones guia oficial de ingenieria front end.pdf
Santo pegasus soluciones Guía Oficial de Ingeniería Backend.pdf
```

Estos documentos permiten que el agente responda preguntas sobre onboarding, arquitectura, incidentes, front-end, back-end, seguridad, observabilidad y buenas prácticas técnicas.

---

## Arquitectura de la solución

```text
PDFs técnicos
    ↓
Extracción de texto con pypdf
    ↓
Limpieza y normalización
    ↓
Chunking por tamaño
    ↓
Embeddings locales con Sentence Transformers
    ↓
Índice vectorial persistente en ChromaDB
    ↓
Búsqueda semántica por pregunta
    ↓
Construcción de contexto RAG
    ↓
Generación de respuesta con Gemini
    ↓
Interfaz Streamlit con fuentes y evidencia
```

---

## Tecnologías utilizadas

| Área | Tecnología |
|---|---|
| Lenguaje principal | Python 3.12 |
| Interfaz web | Streamlit |
| Lectura de PDF | pypdf |
| Embeddings | Sentence Transformers |
| Vector store | ChromaDB |
| LLM | Gemini 2.5 Flash |
| Variables de entorno | python-dotenv |
| Contenedores | Docker |
| Control de versiones | Git + GitHub |
| Nube objetivo | Oracle Cloud Infrastructure |

---

## Estructura del proyecto

```text
pegasus-knowledge-center/
├─ app/
│  ├─ loaders/
│  │  └─ pdf_loader.py
│  ├─ rag/
│  │  ├─ chunking.py
│  │  ├─ embeddings.py
│  │  ├─ llm.py
│  │  ├─ pipeline.py
│  │  └─ vector_store.py
│  └─ main.py
├─ data/
│  └─ raw/
├─ docs/
│  └─ test-questions.md
├─ scripts/
│  ├─ build_index.py
│  ├─ check_chunks.py
│  ├─ check_embeddings.py
│  ├─ check_gemini.py
│  ├─ check_pdfs.py
│  ├─ check_rag_answer.py
│  ├─ check_rag_context.py
│  └─ check_search.py
├─ .streamlit/
│  └─ config.toml
├─ Dockerfile
├─ .dockerignore
├─ .env.example
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## Requisitos

Para ejecución local:

- Python 3.12.
- Git.
- Docker Desktop, opcional para ejecución en contenedor.
- Una API key de Gemini configurada en `.env`.

---

## Variables de entorno

Copia el archivo de ejemplo:

```powershell
copy .env.example .env
```

Edita `.env` y configura tu clave:

```env
APP_NAME=Pegasus Engineering Knowledge Center
APP_ENV=dev

DATA_DIR=./data/raw
VECTORSTORE_DIR=./vectorstore/chroma

LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
GEMINI_API_KEY=your_api_key_here
```

Importante:

```text
.env no debe subirse a GitHub.
```

El repositorio incluye `.env.example`, pero excluye `.env` mediante `.gitignore`.

---

## Ejecución local

### 1. Crear entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Construir índice vectorial

```powershell
python scripts\build_index.py
```

Este comando:

- carga los PDFs desde `data/raw`;
- divide el contenido en chunks;
- genera embeddings;
- crea el índice persistente en `vectorstore/chroma`.

### 4. Ejecutar la app

```powershell
streamlit run app\main.py
```

Abrir en navegador:

```text
http://localhost:8501
```

---

## Ejecución con Docker

### 1. Construir imagen

```powershell
docker build -t pegasus-knowledge-center:local .
```

Durante el build se instala el entorno Python y se construye el índice vectorial.

### 2. Ejecutar contenedor

```powershell
docker run --rm --name pegasus-kc -p 8501:8501 --env-file .env pegasus-knowledge-center:local
```

Abrir en navegador:

```text
http://localhost:8501
```

Si el puerto 8501 está ocupado:

```powershell
docker run --rm --name pegasus-kc -p 8502:8501 --env-file .env pegasus-knowledge-center:local
```

Abrir:

```text
http://localhost:8502
```

---

## Scripts de validación

| Script | Propósito |
|---|---|
| `scripts/check_pdfs.py` | Verifica lectura de PDFs |
| `scripts/check_chunks.py` | Verifica generación de chunks |
| `scripts/check_embeddings.py` | Verifica embeddings locales |
| `scripts/build_index.py` | Construye el índice Chroma |
| `scripts/check_search.py` | Prueba búsqueda semántica |
| `scripts/check_rag_context.py` | Muestra contexto recuperado |
| `scripts/check_gemini.py` | Verifica conexión con Gemini |
| `scripts/check_rag_answer.py` | Prueba respuesta RAG completa |

---

## Ejemplos de preguntas y respuestas

### Pregunta 1

```text
¿Cuáles son los tres pilares filosóficos del front-end?
```

Respuesta esperada:

```text
Los tres pilares filosóficos que guían las decisiones de front-end son:

1. Experiencia del Usuario como Métrica Técnica.
2. Componentes como Contratos.
3. Seguridad en la Capa de Presentación.
```

Fuente principal:

```text
Santo pegasus soluciones guia oficial de ingenieria front end.pdf, página 2.
```

---

### Pregunta 2

```text
¿Qué responsabilidades tiene el Technical Lead durante un incidente?
```

Respuesta esperada:

```text
El Technical Lead lidera la investigación técnica del incidente, dirige el diagnóstico,
propone hipótesis, coordina a los SMEs y ejecuta o autoriza acciones de mitigación
y rollback.
```

Fuente principal:

```text
Protocolo de respuesta a incidentes.pdf, página 6.
```

---

### Pregunta 3

```text
¿Qué debe hacer un nuevo desarrollador durante su primera semana?
```

Respuesta esperada:

```text
Durante la primera semana, el nuevo desarrollador debe configurar su entorno,
conocer al equipo y avanzar en su onboarding técnico. No se espera productividad
plena al finalizar la semana 1.
```

Fuente principal:

```text
Manual de Onboarding para nuevos desarrolladores.pdf, página 31.
```

---

## Características principales

- Interfaz tipo **Engineering Command Center**.
- Modo oscuro profesional.
- Métricas de documentos y chunks.
- Preguntas sugeridas para demo.
- Respuestas generadas con Gemini.
- Evidencia documental desplegable.
- Badges de relevancia semántica.
- Contexto completo enviado al LLM.
- Ejecución local y con Docker.
- Historial de commits claro y progresivo.
- Preparado para despliegue en OCI Compute.

---

## Capturas de pantalla

Pendiente de agregar capturas finales para la entrega.

Capturas recomendadas:

```text
1. Vista principal de la app.
2. Respuesta generada por el agente.
3. Fuentes documentales desplegadas.
4. App ejecutándose en Docker.
5. App desplegada en OCI.
```

---

## Deploy en OCI

Estado actual:

```text
Pendiente.
```

La aplicación ya fue preparada para ejecución con Docker, lo que facilita su posterior despliegue en una instancia **OCI Compute**.

Evidencia requerida para el challenge:

- URL pública de la aplicación desplegada.
- Captura de la app ejecutándose en OCI.
- Comando o proceso usado para levantar el contenedor.
- Variables de entorno configuradas de forma segura.

---

## Seguridad

Buenas prácticas aplicadas:

- `.env` excluido del repositorio.
- `.env.example` incluido como plantilla.
- API key de Gemini inyectada mediante variable de entorno.
- Índice vectorial generado localmente.
- Vectorstore excluido del repositorio y reconstruible con script.
- Docker recibe secretos mediante `--env-file`.

---

## Limitaciones actuales

- Solo procesa PDFs de texto extraíble.
- No implementa OCR.
- El índice vectorial debe reconstruirse si cambian los documentos.
- La relevancia se calcula de forma aproximada usando distancia semántica.
- La calidad de respuesta depende de los chunks recuperados.
- El deploy OCI todavía está pendiente.

---

## Roadmap

- [x] Crear app base con Streamlit.
- [x] Leer documentos PDF.
- [x] Implementar loader reutilizable.
- [x] Crear pipeline de chunking.
- [x] Generar embeddings locales.
- [x] Persistir índice en ChromaDB.
- [x] Implementar búsqueda semántica.
- [x] Conectar Gemini.
- [x] Crear interfaz visual profesional.
- [x] Agregar Dockerfile.
- [x] Subir repositorio a GitHub.
- [x] Mejorar README.
- [ ] Mejorar README con capturas.
- [ ] Desplegar en OCI Compute.
- [ ] Agregar evidencia pública del deploy.

---

## Autor

**Sergio Carey**

Ingeniero en Informática  
Arica, Chile

---

## Licencia

Proyecto desarrollado con fines educativos para el Challenge Final **Alura Agente**.