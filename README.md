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

## Requisitos Previos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (gestor de Python)
- [Bun](https://bun.sh/) (gestor de frontend)
- [Docker](https://www.docker.com/) y Docker Compose

## Setup Rápido (Día 1)

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
# Iniciar PostgreSQL y Adminer (interfaz visual de DB)
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

# Adminer (visualizar DB)
open http://localhost:8080
# Server: db, User: postgres, Password: postgres
```

## Estructura del Proyecto

```
botcachino_monorepo/
├── src/                      # Código Python
│   ├── api/                  # Endpoints y lógica de API
│   │   ├── routes/           # Routers FastAPI
│   │   │   ├── content_router.py
│   │   │   └── __init__.py
│   │   ├── services/         # Lógica de negocio
│   │   │   └── content_service.py
│   │   ├── dependencies.py   # Inyección de dependencias
│   │   └── server.py         # App FastAPI
│   ├── db/                   # Configuración de base de datos
│   │   ├── database.py       # Engine async y session maker
│   │   ├── init-db/          # Scripts de inicialización de DB
│   │   │   └── init.sql
│   │   └── models/           # Modelos SQLModel
│   │       └── content.py
│   └── agent/                # Lógica de agente (placeholder)
├── web/                      # Frontend React
│   ├── src/                  # Componentes React
│   ├── eslint.config.js      # Configuración ESLint
│   └── vite.config.js        # Configuración Vite
├── main.py                   # Punto de entrada (importa src/api/server.py)
├── pyproject.toml            # Dependencias Python
├── docker-compose.yaml       # PostgreSQL + Adminer
└── AGENTS.md                 # Guía para agentes de IA
```

## API Endpoints

### Content

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/content/` | Listar todo el contenido |
| GET | `/content/{id}` | Obtener contenido por ID |
| POST | `/content/` | Crear nuevo contenido |
| PATCH | `/content/{id}` | Actualizar contenido |
| DELETE | `/content/{id}` | Eliminar contenido |

### Content Model

El modelo `Content` incluye:
- **title**: Título (2-200 caracteres)
- **summary**: Resumen (2-500 caracteres)
- **category**: Categoría (INFO, NEW)
- **content**: Cuerpo del contenido
- **post_date**: Fecha de publicación
- **embedding**: Vector de 4096 dimensiones para búsqueda semántica
- **created_at**: Timestamp de creación
- **updated_at**: Timestamp de actualización

### Ejemplo de uso

```bash
# Crear contenido
curl -X POST http://127.0.0.1:8000/content/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Título del contenido",
    "summary": "Resumen breve",
    "category": "INFO",
    "content": "Contenido completo del artículo...",
    "post_date": "2026-01-01T10:00:00"
  }'

# Listar contenido
curl http://127.0.0.1:8000/content/

# Obtener por ID
curl http://127.0.0.1:8000/content/1

# Actualizar
curl -X PATCH http://127.0.0.1:8000/content/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Título actualizado",
    "summary": "Resumen actualizado"
  }'

# Eliminar
curl -X DELETE http://127.0.0.1:8000/content/1
```

## Comandos Útiles

### Python / Backend

```bash
uv sync              # Instalar/actualizar dependencias
uv run python main.py              # Ejecutar API
uv run python -m src.api.server    # Ejecutar módulo específico

# Con hot-reload (desarrollo)
uv run uvicorn src.api.server:app --reload --port 8000
```

### Frontend

```bash
cd web
bun install          # Instalar dependencias
bun run dev          # Servidor de desarrollo (hot-reload)
bun run build        # Build de producción
bun run lint         # Verificar código
bun run preview      # Previsualizar build
```

### Base de Datos

```bash
docker compose up -d       # Iniciar servicios
docker compose down        # Detener servicios
docker compose logs -f    # Ver logs
docker compose exec db psql -U postgres -d botcachino  # CLI de PostgreSQL
```

## Convenciones de Código

### Python

- **Async**: Todas las operaciones de base de datos son asíncronas (`async/await`)
- **Modelos**: Usar SQLModel con las variantes `*Base`, `*Create`, `*Update`, `*Read`
- **Timestamps**: Usar `datetime.now(UTC)` para mantener consistencia con PostgreSQL
- **Sesiones**: Inyectar vía `Depends()` en los routers

### Frontend

- **TypeScript**: No usado actualmente (JSX plano)
- **Estado**: Sin framework de state management aún
- **Linting**: ESLint con `varsIgnorePattern: '^[A-Z_]'` (vars uppercase permitidas)

### Git

```bash
# Conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"
```

## Configuración de Entorno

Variables de entorno (ver `.env.example`):

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino
```

## Recursos Adicionales

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [pgvector](https://github.com/pgvector/pgvector) (búsqueda vectorial)
- [React Docs](https://react.dev/)
- [Vite](https://vitejs.dev/)

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

### Frontend no carga

```bash
cd web
rm -rf node_modules bun.lock
bun install
```