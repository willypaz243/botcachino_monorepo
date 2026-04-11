# Agents

## Dev environment

- Python 3.13 via `uv`. Run `uv sync` to install, `uv run python -m <module>` to execute.
- Frontend (`web/`) uses Bun. `cd web && bun install` first, then `bun run dev` (http://localhost:5173).

## Package layout

- `src/api/server.py` — FastAPI app (the real entry point; `main.py` imports and runs it via uvicorn).
- `src/db/` — SQLModel models and database setup.
- `src/agent/` — Agent logic (placeholder).
- `web/` — React 19 + Vite frontend (plain JSX, no TypeScript, no tests).

## Commands

```bash
# Python
uv sync
uv run python -m src.api.server    # run API directly
uv run python main.py              # run via uvicorn on port 8000

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
