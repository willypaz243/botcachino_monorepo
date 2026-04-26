# API Reference

## Endpoints

### Content

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/content/` | Listar todo el contenido |
| GET | `/content/search/` | Búsqueda semántica por texto |
| GET | `/content/{id}` | Obtener contenido por ID |
| POST | `/content/` | Crear nuevo contenido |
| PATCH | `/content/{id}` | Actualizar contenido |
| DELETE | `/content/{id}` | Eliminar contenido |

### Búsqueda Semántica

El endpoint `/content/search/` permite realizar búsquedas semánticas usando embeddings vectoriales:

| Parámetro | Tipo | Default | Descripción |
|------------|------|---------|-------------|
| `q` | string | requerido | Texto de búsqueda (1-500 chars) |
| `limit` | int | 5 | Número máximo de resultados (1-100) |
| `offset` | int | 0 | Desplazamiento para paginación |

**Ejemplo:**

```bash
# Buscar contenido semánticamente
curl "http://127.0.0.1:8000/content/search/?q=becas%20para%20estudiantes&limit=3"

# Con offset para paginación
curl "http://127.0.0.1:8000/content/search/?q=noticias&limit=10&offset=10"
```

La búsqueda usa distancia coseno (`<=>`) para comparar el embedding de la consulta con los embeddings almacenados.

### Content Model

El modelo `Content` incluye:

- **id**: UUID único
- **title**: Título (2-200 caracteres)
- **summary**: Resumen (2-500 caracteres)
- **category**: Categoría (INFO, NEW, SCHOLARSH, ANN)
- **content**: Cuerpo del contenido
- **post_date**: Fecha de publicación
- **embedding**: Vector de 4096 dimensiones
- **created_at**: Timestamp de creación
- **updated_at**: Timestamp de actualización

#### Categorías Disponibles

| Categoría | Descripción |
|-----------|-------------|
| INFO | Información general del campus |
| NEW | Novedades institucionales |
| SCHOLARSH | Becas y movilidad internacional |
| ANN | Anuncios y actividades universitarias |

### University Information Agent

**POST /api/agent/chat**

Query parameters:
- `message` (required): User message (1-2000 chars)
- `thread_id` (required): Conversation thread ID (1-100 chars)

Response: Server-Sent Events (SSE) stream

```json
{
  "content": "string",
  "type": "text" | "error" | "info",
  "done": boolean
}
```

## Agregar Datos

### Datos de Ejemplo

Los archivos JSON en `data/` deben tener esta estructura:

```json
[
  {
    "title": "Título del contenido",
    "content": "Contenido completo...",
    "summary": "Resumen breve",
    "post_date": "2025-04-12"
  }
]
```

**Categorías:**
- `scholarship.json` → SCHOLARSH
- `news.json` → NEW
- `announcements.json` → ANN

```bash
python commands.py --fill
```