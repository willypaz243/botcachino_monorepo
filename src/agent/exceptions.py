from typing import Any


class AgentError(Exception):
    pass


class ModelError(AgentError):
    pass


class SearchError(AgentError):
    pass


class ContentNotFoundError(AgentError):
    pass


def format_error_response(error: Exception) -> dict[str, Any]:
    if isinstance(error, ModelError):
        return {
            "type": "error",
            "content": f"Error en el modelo: {str(error)}",
        }
    elif isinstance(error, SearchError):
        return {
            "type": "error",
            "content": f"Error en la búsqueda: {str(error)}",
        }
    elif isinstance(error, ContentNotFoundError):
        return {
            "type": "error",
            "content": f"Contenido no encontrado: {str(error)}",
        }
    else:
        return {
            "type": "error",
            "content": f"Error inesperado: {str(error)}",
        }
