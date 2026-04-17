FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Instalar dependencias del sistema para asyncpg y pgvector
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias primero (cache de Docker)
COPY pyproject.toml uv.lock ./

# Instalar dependencias de producción
RUN uv sync --frozen --no-dev

# Copiar código fuente
COPY src/ src/
COPY main.py .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
