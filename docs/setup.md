# Setup y Configuración

## Requisitos Previos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Gestor de Python
- [Bun](https://bun.sh/) - Gestor de frontend
- [Docker](https://www.docker.com/) y Docker Compose

## Estructura del Proyecto

```
botcachino_monorepo/
├── src/                      # Código Python
│   ├── api/                  # Endpoints y lógica de API
│   │   ├── routes/           # Routers FastAPI
│   │   ├── services/         # Lógica de negocio
│   │   ├── dependencies.py   # Inyección de dependencias
│   │   └── server.py         # App FastAPI
│   ├── db/                   # Configuración de base de datos
│   │   ├── database.py       # Engine async y session maker
│   │   └── models/           # Modelos SQLModel
│   └── agent/                # University Information Agent
│       ├── config.py
│       ├── constants.py
│       ├── state.py
│       ├── nodes/
│       └── graph.py
├── data/                     # Datos de ejemplo para seeding
│   ├── scholarship.json
│   ├── news.json
│   └── announcements.json
├── scripts/                  # Scripts de utilidad
│   └── seed_data.py
├── web/                      # Frontend React
├── main.py                   # Punto de entrada
├── commands.py               # CLI interface para seeding
├── pyproject.toml            # Dependencias Python
├── docker-compose.yaml       # PostgreSQL + Adminer
└── AGENTS.md               # Guía para agentes de IA
```

## Setup Detallado

### 1. Clonar y configurar entorno

```bash
# Clonar repositorio
git clone <repo-url>
cd botcachino_monorepo

# Crear entorno virtual e instalar dependencias Python
uv sync

# Copiar configuración de ejemplo
cp .env.example .env
```

### 2. Iniciar servicios de base de datos

```bash
# Iniciar PostgreSQL y Adminer
docker compose up -d

# Verificar que los servicios están corriendo
docker compose ps
```

### 3. Iniciar el proyecto

```bash
# Terminal 1: Backend API (puerto 8000)
uv run python main.py

# Terminal 2: Frontend (puerto 5173)
cd web && bun install  # solo la primera vez
bun run dev
```

### 4. Verificar instalación

```bash
# API respondiendo
curl http://127.0.0.1:8000/

# Documentación interactiva
open http://127.0.0.1:8000/docs

# Adminer (interfaz visual de DB)
open http://localhost:8080
# Server: db, User: postgres, Password: postgres
```

## Variables de Entorno

```bash
# Agent Configuration
AGENT__UNIVERSITY_NAME="Universidad Mayor de San Simon (UMSS)"
AGENT_MODEL__NAME="openai/gpt-oss-120b-fast"
AGENT_MODEL__API_KEY="[model-api-key]"
AGENT_ROUTER_MODEL__NAME="openai/gpt-oss-120b-fast"
AGENT_ROUTER_MODEL__API_KEY="[model-api-key]"
AGENT_MAX_SEARCH_RETRIES=5
AGENT_MAX_RESPONSE_TOKENS=1024

# IA Services
NEBIUS__API_KEY="[model-api-key]"

# Database
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino"
```

## Comandos Útiles

### Python / Backend

```bash
uv sync              # Instalar/actualizar dependencias
uv run python main.py # Ejecutar API
uv run uvicorn src.api.server:app --reload --port 8000  # Con hot-reload
uv run langgraph dev  # LangGraph dev server (puerto 2024)
```

### Frontend

```bash
cd web
bun install          # Instalar dependencias
bun run dev         # Servidor de desarrollo
bun run build       # Build de producción
bun run preview     # Previsualizar build
```

### Base de Datos

```bash
docker compose up -d       # Iniciar servicios
docker compose down        # Detener servicios
docker compose logs -f    # Ver logs
docker compose exec db psql -U postgres -d botcachino  # CLI de PostgreSQL
```

### Seed Data

```bash
python commands.py --fill        # Sembrar la base de datos
python commands.py --fill --dry-run  # Ver qué haría sin ejecutar
```

## Troubleshooting

### "Connection refused" al conectar a PostgreSQL

```bash
# Verificar que Docker está corriendo
docker compose ps

# Reiniciar servicios
docker compose restart
```

### Errores de importación en Python

```bash
# Asegurarse de que el entorno está sincronizado
uv sync
```

### Error al sembrar datos (401 Authentication)

```bash
# Verificar que la API Key de Nebius está configurada en .env
```

### Frontend no carga

```bash
cd web
rm -rf node_modules bun.lock
bun install
```

### Agente no responde correctamente

```bash
# Verificar que el servidor LangGraph está corriendo
uv run langgraph dev
```