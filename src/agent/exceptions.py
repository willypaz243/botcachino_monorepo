from typing import Any


class AgentError(Exception):
    pass


class ModelError(AgentError):
    pass


class SearchError(AgentError):
    pass


class ContentNotFoundError(AgentError):
    pass


class RateLimitError(AgentError):
    """Excepción para rate limit (429 Too Many Requests)."""

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
    elif isinstance(error, RateLimitError):
        return {
            "type": "error",
            "content": "El servicio está muy ocupado. Espera al menos 1 minuto antes de intentar nuevamente. si sigue sin funcionar vuelve mas tarde",
        }
    else:
        return {
            "type": "error",
            "content": f"Error inesperado: {str(error)}",
        }
