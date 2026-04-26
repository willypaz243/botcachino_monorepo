# Arquitectura del Sistema

## Visión General

Botcachino es un sistema de gestión de información universitaria que combina:

- **Backend**: FastAPI con PostgreSQL + pgvector para búsqueda semántica
- **Frontend**: React 19 con Vite
- **Agente IA**: LangGraph para responder preguntas sobre la universidad

## Servicios Principales

### ContentService

Maneja operaciones CRUD sobre el modelo `Content`:

- `create_content()` - Crear nuevo contenido
- `get_content()` - Obtener contenido por ID
- `list_content()` - Listar todo el contenido
- `update_content()` - Actualizar contenido
- `delete_content()` - Eliminar contenido
- `search_content()` - Búsqueda semántica

### EmbeddingService

Genera embeddings para búsqueda semántica usando modelos de langchain (NebiusEmbeddings):

- `generate_embedding()` - Genera embedding para un texto
- `batch_generate_embeddings()` - Genera embeddings para múltiples textos

### UniversityAgent

Agente LangGraph que responde preguntas sobre la universidad:

- Clasifica consultas como relevantes o off-topic
- Realiza búsqueda semántica
- Evalúa resultados
- Genera respuestas con streaming

## Flujo de Embeddings

1. Los datos se cargan desde JSON en el directorio `data/`
2. Se procesan y normalizan (`pre_process_text`)
3. Se generan embeddings vectoriales de 4096 dimensiones
4. Se almacenan junto con el contenido en PostgreSQL con pgvector

## Agent Architecture

El agente utiliza LangGraph con los siguientes nodes:

- **Router**: Clasifica consultas como relevantes o off-topic
- **Search**: Realiza búsqueda semántica
- **Fetch IDs**: Recupera el contenido por IDs
- **Respond**: Genera la respuesta final
- **Retry**: Reintenta la búsqueda si no se encuentran resultados relevantes

## Convenciones de Código

### Python

- **Async**: Todas las operaciones de base de datos son asíncronas (`async/await`)
- **Modelos**: Usar SQLModel con las variantes `*Base`, `*Create`, `*Update`, `*Read`
- **Timestamps**: Usar `datetime.now(UTC)` para mantener consistencia con PostgreSQL
- **Sesiones**: Inyectar vía `Depends()` en los routers
- **Python 3.13**: `pyproject.toml` requiere `>=3.13`

### Frontend

- **TypeScript**: Usar `.tsx` para componentes
- **Estado**: hooks personalizados en `src/hooks/`
- **Estilos**: CSS Modules en `*.module.css`

### Git

```bash
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"
```