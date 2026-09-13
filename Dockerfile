FROM python:3.12.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/pegasus

WORKDIR /app

RUN groupadd --gid 10001 pegasus \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin pegasus

COPY requirements.txt ./

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY --chown=pegasus:pegasus app ./app
COPY --chown=pegasus:pegasus data ./data
COPY --chown=pegasus:pegasus scripts ./scripts
COPY --chown=pegasus:pegasus .streamlit ./.streamlit

USER pegasus

RUN mkdir -p vectorstore/chroma \
    && python scripts/build_index.py

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)"

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
