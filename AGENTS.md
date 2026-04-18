# Agents

## Dev environment

- Python 3.13 via `uv`. Run `uv sync` to install.
- Frontend (`web/`) uses **TypeScript** (TSX), Vite, and Bun. `cd web && bun install` then `bun run dev` (http://localhost:5173).
- LangGraph CLI for agent dev: `uv run langgraph dev` (port 2024, requires `docker compose up -d`).

## Package layout

- `src/api/server.py` — FastAPI app with lifespan (creates DB tables on startup). `main.py` just imports and runs it via uvicorn.
- `src/api/routes/__init__.py` — mounts `content_router`, `agent_router`, `history_router` under `/api`.
- `src/api/services/` — `content_service.py` (CRUD + semantic search), `embedding_service.py`.
- `src/api/dependencies.py` — DI for services.
- `src/db/` — `database.py` (async engine, session maker), `models/` (SQLModel: `content.py`, `history.py`).
- `src/agent/` — LangGraph university agent. Key files: `graph.py` (graph construction), `agent.py` (high-level interface + streaming), `streaming.py` (SSE formatting), `nodes/` (router, search, off_topic, fetch_ids, respond, retry).
- `data/` — seed JSON (`scholarship.json`, `news.json`, `announcements.json`).
- `scripts/seed_data.py` — populates DB from `data/`.
- `commands.py` — CLI wrapper for seeding (`python commands.py --fill`, `--dry-run`).
- `web/` — React 19 + TypeScript + Vite. Build runs `tsc --noEmit` before `vite build`.

## Commands

```bash
# Python
uv sync
uv run python main.py              # API on port 8000
uv run uvicorn src.api.server:app --reload --port 8000   # hot-reload

# Agent dev
uv run langgraph dev               # port 2024, requires docker compose up -d
                                   # Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

# Seed
uv run python commands.py --fill
uv run python commands.py --fill --dry-run

# Frontend (cd web first)
bun install
bun run dev
bun run build
bun run typecheck
bun run lint

# Database
docker compose up -d
docker compose exec db psql -U postgres -d botcachino
```

## Testing

- `pyproject.toml` has `[tool.pytest.ini_options]` with `pythonpath = ["."]`.
- `tests/` directory exists (`tests/agent/`, `tests/api/`) but no test runner command is defined in `pyproject.toml`. Run `uv run pytest` directly.
- Dev deps include `pytest`, `pytest-asyncio`.

## API endpoints

- `GET /` — health check
- `GET /content/` — list all content
- `GET /content/search/?q=...&limit=5&offset=0` — semantic search (cosine distance via pgvector `<=>`)
- `GET /content/{id}` — get by ID
- `POST /content/` — create
- `PATCH /content/{id}` — update
- `DELETE /content/{id}` — delete
- `POST /api/agent/chat?message=...&thread_id=...` — agent chat (SSE stream)

## Database

- PostgreSQL 16 + pgvector (4096-dim embeddings).
- Default: `postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino` (override with `DATABASE_URL`).
- Adminer: http://localhost:8080 (server: `db`, user: `postgres`, password: `postgres`).
- Content categories: `INFO`, `NEW`, `SCHOLARSH`, `ANN`.

## Agent configuration

Env vars prefixed `AGENT_`:

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_UNIVERSITY_NAME` | `"la universidad"` | University name |
| `AGENT_MODEL__PROVIDER` | `"nebius"` | LLM provider |
| `AGENT_MODEL__NAME` | `"Qwen/Qwen3-30B-A3B"` | Model name |
| `AGENT_MODEL__TEMPERATURE` | `0.3` | Model temperature |
| `AGENT_ROUTER_MODEL__NAME` | `"Qwen/Qwen3-30B-A3B"` | Router model |
| `AGENT_ROUTER_MODEL__TEMPERATURE` | `0.1` | Router temperature |
| `AGENT_MAX_SEARCH_RETRIES` | `5` | Max search retries |
| `AGENT_DEFAULT_SEARCH_LIMIT` | `5` | Default search limit |
| `AGENT_MAX_RESPONSE_TOKENS` | `1024` | Max response tokens |

Agent SSE event types: `text`, `error`, `info`. Info messages include `"Iniciando conversación..."`, `"Analizando consulta..."`, `"Buscando información..."`, `"Evaluando resultados..."`, `"Recuperando contenido..."`, `"Generando respuesta..."`, `"Respuesta completada"`, `"Reintentando búsqueda..."`, `"No encontré información relevante..."`.

## Gotchas

- `commands.py` (plural) — not `command.py`.
- `pyproject.toml` requires `>=3.13`. Do not add deps pinned to older Python.
- `web/` uses TypeScript (TSX), not plain JSX. ESLint flat config in `eslint.config.ts`.
- `uv run` is required for all Python commands (no system Python).
- DB tables are auto-created on FastAPI startup via lifespan hook.
- `langgraph.json` references `./src/agent/langgraph_app.py:graph` as the graph entry point.
