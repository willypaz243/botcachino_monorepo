# Agente IA

## Universidad Botcachino

El agente utiliza LangGraph para responder preguntas sobre la universidad usando búsqueda semántica.

## Configuración

Variables de entorno:

```bash
AGENT__UNIVERSITY_NAME="Universidad Mayor de San Simon (UMSS)"
AGENT_MODEL__PROVIDER="nebius"
AGENT_MODEL__NAME="Qwen/Qwen3-30B-A3B"
AGENT_MODEL__TEMPERATURE=0.3

AGENT_ROUTER_MODEL__NAME="Qwen/Qwen3-30B-A3B"
AGENT_ROUTER_MODEL__TEMPERATURE=0.1

AGENT_MAX_SEARCH_RETRIES=5
AGENT_DEFAULT_SEARCH_LIMIT=5
AGENT_MAX_RESPONSE_TOKENS=1024
```

## Graph Nodes

- **router**: Clasifica consultas como relevantes o off-topic
- **search**: Realiza búsqueda semántica
- **fetch_ids**: Recupera el contenido por IDs
- **respond**: Genera la respuesta final
- **retry**: Reintenta la búsqueda si no hay resultados relevantes
- **off_topic**: Responde cuando la consulta no es relevante

## Chat Endpoint

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

## SSE Events

| Evento | Descripción |
|--------|-------------|
| `text` | Fragmento de respuesta |
| `error` | Mensaje de error |
| `info` | Mensaje informativo |

Mensajes info:
- "Iniciando conversación..."
- "Analizando consulta..."
- "Buscando información..."
- "Evaluando resultados..."
- "Recuperando contenido..."
- "Generando respuesta..."
- "Respuesta completada"
- "Reintentando búsqueda..."
- "No encontré información relevante..."

## Desarrollo

```bash
uv run langgraph dev  # Servidor en puerto 2024
# Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```