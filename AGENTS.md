# Agents

## Dev environment

- Python 3.13 via `uv`. Run `uv sync` to install, `uv run python -m <module>` to execute.
- Frontend (`web/`) uses Bun. `cd web && bun install` first, then `bun run dev` (http://localhost:5173).

## Package layout

- `src/api/server.py` — FastAPI app (the real entry point; `main.py` imports and runs it via uvicorn).
- `src/api/routes/` — Routers (content_router.py, agent_router.py) and query param schemas (schemas.py).
- `src/api/services/` — Business logic (content_service.py, embedding_service.py).
- `src/api/dependencies.py` — Dependency injection for services.
- `src/db/` — SQLModel models and database setup.
- `src/agent/` — University information agent implementation.
- `data/` — Seed data files (scholarship.json, news.json, announcements.json).
- `scripts/seed_data.py` — Script to populate database from data files.
- `command.py` — CLI interface for seeding (python command.py --fill).
- `web/` — React 19 + Vite frontend (plain JSX, no TypeScript, no tests).

## Semantic Search

- `src/api/services/content_service.py` — `search(query_text, limit, offset)` method performs semantic search using cosine distance (`<=>`).
- `src/api/routes/content_router.py` — `GET /content/search/` endpoint.
- `src/api/routes/schemas.py` — `SearchParams` class with `q`, `limit`, `offset` query parameters.

## University Information Agent

### Overview

An AI agent powered by LangGraph that answers questions about the university using semantic search. The agent:

- Classifies user queries to determine if they're related to the university
- Performs semantic search to find relevant content
- Evaluates search results to identify truly relevant information
- Retrieves full content by IDs when relevant content is found
- Generates informative responses with a maximum of 1024 tokens
- Streams responses via Server-Sent Events (SSE)
- Supports conversation threads via `thread_id`

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     POST /api/agent/chat                         │
│                  (StreamingResponse via SSE)                     │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LANGGRAPH AGENT                             │
│                                                                   │
│  ┌──────────────┐    (off-topic)                                 │
│  │   ROUTER     │──────────────────────────────────────────────▶┤ OFF-TOPIC
│  │  (analizar)  │                                                │
│  └──────────────┘                                                │
│         │                                                        │
│    (relevant)                                                    │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   SEARCH    │───▶│  FETCH_IDS   │───▶│   RESPOND    │      │
│  │  (evaluar)   │    │ (recuperar) │    │  (generar)   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                                    ▲                   │
│         │ (reintentar)                       │                   │
│         └────────────────────────────────────┘                   │
│                      (hasta 5 intentos)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Components

- `src/agent/config.py` — Configuration for model providers, university name, and limits
- `src/agent/constants.py` — System prompts and info messages
- `src/agent/state.py` — LangGraph state schema
- `src/agent/exceptions.py` — Custom exception classes
- `src/agent/tools.py` — Semantic search tool definition
- `src/agent/nodes/` — Individual graph nodes (router, search, off_topic, fetch_ids, respond, retry)
- `src/agent/graph.py` — LangGraph construction and compilation
- `src/agent/agent.py` — High-level agent interface with streaming support
- `src/agent/streaming.py` — SSE formatting utilities
- `src/api/routes/agent_router.py` — FastAPI endpoint for agent chat

### Configuration

Environment variables (prefix: `AGENT_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_UNIVERSITY_NAME` | `"la universidad"` | Name of the university |
| `AGENT_MODEL__PROVIDER` | `"nebius"` | LLM provider for chat |
| `AGENT_MODEL__NAME` | `"Qwen/Qwen3-30B-A3B"` | Model name |
| `AGENT_MODEL__TEMPERATURE` | `0.3` | Model temperature |
| `AGENT_ROUTER_MODEL__NAME` | `"Qwen/Qwen3-30B-A3B"` | Router model name |
| `AGENT_ROUTER_MODEL__TEMPERATURE` | `0.1` | Router temperature |
| `AGENT_MAX_SEARCH_RETRIES` | `5` | Max retry attempts |
| `AGENT_DEFAULT_SEARCH_LIMIT` | `5` | Default search results limit |
| `AGENT_MAX_RESPONSE_TOKENS` | `1024` | Max tokens in response |

### API Endpoint

**POST /api/agent/chat**

Query parameters:
- `message` (required): User message (1-2000 chars)
- `thread_id` (required): Conversation thread ID (1-100 chars)

Response: Server-Sent Events (SSE) stream

Event format:
```json
{
  "content": "string",
  "type": "text" | "error" | "info",
  "done": boolean
}
```

Info messages:
- `"Iniciando conversación..."` — Agent starting
- `"Analizando consulta..."` — Router analyzing query
- `"Buscando información..."` — Search in progress
- `"Evaluando resultados..."` — Evaluating search results
- `"Recuperando contenido..."` — Fetching content by IDs
- `"Generando respuesta..."` — Generating final response
- `"Respuesta completada"` — Response complete
- `"Reintentando búsqueda..."` — Retrying search
- `"No encontré información relevante..."` — No relevant content found

## Commands

```bash
# Python
uv sync
uv run python -m src.api.server    # run API directly
uv run python main.py              # run via uvicorn on port 8000

# Seed database
python command.py --fill           # populate database from data/

# Frontend
cd web && bun install
bun run dev
bun run build
bun run lint      # ESLint flat config

# Database (Docker)
docker compose up -d       # start PostgreSQL + Adminer
docker compose down       # stop services
```

## Database

- PostgreSQL 16 with `pgvector` extension for vector search support.
- Default: `postgresql://postgres:postgres@localhost:5432/botcachino`
- Override with `DATABASE_URL` env var (see `.env.example`).
- Adminer UI: http://localhost:8080 (server: `db`, user: `postgres`).

## Conventions

- ESLint rule `varsIgnorePattern: '^[A-Z_]'` — uppercase-prefixed vars are allowed as unused (e.g., `const _unused = ...`).
- `pyproject.toml` requires `>=3.13`. Do not add deps pinned to older Python.
- No test framework, no lint tooling, no pre-commit hooks yet.
- `.venv/` is gitignored but present locally.
- Content categories: INFO, NEW, SCHOLARSH, ANN.
