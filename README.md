# Botcachino

Sistema de gestión de noticias e información con interfaz web, construido con FastAPI y React.

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | Python 3.13, FastAPI, SQLModel, SQLAlchemy (async) |
| **Base de Datos** | PostgreSQL 16 + pgvector (vectores para búsqueda semántica) |
| **Frontend** | React 19, Vite, Bun |
| **ORM** | SQLModel + SQLAlchemy async |
| **Gestor de Paquetes** | uv (Python), Bun (frontend) |
| **Agente AI** | LangGraph (University Information Agent) |

## Requisitos Previos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (gestor de Python)
- [Bun](https://bun.sh/) (gestor de frontend)
- [Docker](https://www.docker.com/) y Docker Compose

## Setup Rápido

### 1. Clonar y configurar entorno

```bash
git clone <repo-url>
cd botcachino_monorepo
uv sync
cp .env.example .env
```

### 2. Iniciar servicios de base de datos

```bash
docker compose up -d
docker compose ps
```

### 3. Iniciar el proyecto

```bash
# Terminal 1: Backend API (puerto 8000)
uv run python main.py

# Terminal 2: Frontend (puerto 5173)
cd web && bun install
bun run dev
```

### 4. Verificar instalación

```bash
curl http://127.0.0.1:8000/
open http://127.0.0.1:8000/docs
open http://localhost:8080  # Adminer: server=db, user=postgres, password=postgres
```

## Rutas

- **Landing**: http://localhost:5173/
- **Chat**: http://localhost:5173/agent

## Documentación

- [Setup y Configuración](./docs/setup.md)
- [Arquitectura](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Frontend](./docs/frontend.md)
- [Agente IA](./docs/agent.md)

## Comandos Útiles

```bash
# Python
uv sync
uv run python main.py
uv run uvicorn src.api.server:app --reload --port 8000
uv run langgraph dev

# Frontend
cd web && bun install && bun run dev

# Base de datos
docker compose up -d
docker compose exec db psql -U postgres -d botcachino

# Seed data
python commands.py --fill
python commands.py --fill --dry-run
```

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [pgvector](https://github.com/pgvector/pgvector)
- [LangGraph](https://langchain-ai.github.io/langgraph/)