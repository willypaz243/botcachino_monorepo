# Agents

## Dev environment

- Python 3.13 managed by `uv`. Use `uv sync` to install, `uv run` to execute.
- Frontend (`web/`) uses Bun. Run `bun install`, `bun run dev`, etc.

## Package layout

- `src/` — Python packages (`agent/`, `api/`, `db/`). No `__init__.py` files yet.
- `web/` — React 19 + Vite frontend. No TypeScript, no tests.
- Root `main.py` — placeholder entry point.

## Commands

### Python
```bash
uv sync            # install deps
uv run python -m <module>   # run a module
```

### Frontend
```bash
cd web && bun install
bun run dev       # dev server (http://localhost:5173)
bun run build     # production build
bun run lint      # ESLint
```

## Constraints

- `pyproject.toml` requires `>=3.13`. Do not add deps pinned to older Python versions.
- No test framework, no lint tooling, no pre-commit hooks yet. Add these as needed.
- `.venv/` is gitignored but present locally. Use `.venv/bin/python` for local venv runs.
