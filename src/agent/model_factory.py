import asyncio
import os
import time

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from pydantic import SecretStr

load_dotenv()

_DEFAULT_REQUEST_DELAY = float(os.getenv("AGENT__REQUEST_DELAY", "0.5"))


_PROVIDER_API_KEY_ENV = {
    "cerebras": "CEREBRAS_API_KEY",
    "groq": "GROQ_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "nebius": "NEBIUS_API_KEY",
}


def _get_api_key(provider: str) -> SecretStr | None:
    """Cargar la API key del env var correspondiente al provider."""
    env_var = _PROVIDER_API_KEY_ENV.get(provider)
    if not env_var:
        return None
    value = os.environ.get(env_var)
    if not value:
        return None
    return SecretStr(value)


class _RateLimitedModel:
    """Wrapper que aplica delay entre requests para evitar rate limits."""

    def __init__(self, model: BaseChatModel, delay: float) -> None:
        self._model = model
        self._delay = delay
        self._last_call = 0.0
        self._lock = asyncio.Lock()

    async def _wait(self) -> None:
        async with self._lock:
            elapsed = time.monotonic() - self._last_call
            if elapsed < self._delay:
                await asyncio.sleep(self._delay - elapsed)
            self._last_call = time.monotonic()

    def bind_tools(self, tools, **kwargs):
        wrapped = self._model.bind_tools(tools, **kwargs)
        return _RateLimitedModel(wrapped, self._delay)  # type: ignore[return-value]

    def with_structured_output(self, schema, **kwargs):
        wrapped = self._model.with_structured_output(schema, **kwargs)
        return _RateLimitedModel(wrapped, self._delay)  # type: ignore[return-value]

    async def ainvoke(self, input, config=None, **kwargs):
        await self._wait()
        return await self._model.ainvoke(input, config, **kwargs)

    async def astream(self, input, config=None, **kwargs):
        await self._wait()
        async for chunk in self._model.astream(input, config, **kwargs):
            yield chunk


def get_chat_model(
    provider: str,
    model_name: str,
    temperature: float = 0.3,
    request_delay: float | None = None,
) -> BaseChatModel:
    """Create a chat model instance based on provider config.

    Providers: "nebius", "openai", "anthropic", "cerebras", "groq", "google"
    Falls back to "nebius" for any unrecognized provider.

    API key se carga dinámicamente desde la variable de entorno según el provider:
      - cerebras → CEREBRAS_API_KEY
      - groq     → GROQ_API_KEY
      - google   → GOOGLE_API_KEY
      - openai   → OPENAI_API_KEY
      - anthropic→ ANTHROPIC_API_KEY
      - nebius   → NEBIUS__API_KEY

    Args:
        provider: Provider del modelo LLM
        model_name: Nombre del modelo
        temperature: Temperatura de generación
        request_delay: Delay en segundos entre requests (default: 0.5s, configurable con AGENT__REQUEST_DELAY)
    """

    api_key = _get_api_key(provider)
    delay = request_delay if request_delay is not None else _DEFAULT_REQUEST_DELAY

    raw_model: BaseChatModel
    if provider == "openai":
        from langchain_openai import ChatOpenAI  # type: ignore[no-redef]

        raw_model = ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)  # type: ignore[arg-type]
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic  # type: ignore[import-not-found, no-redef]

        raw_model = ChatAnthropic(model=model_name, temperature=temperature, api_key=api_key)  # type: ignore[arg-type]
    elif provider == "cerebras":
        from langchain_cerebras import ChatCerebras

        raw_model = ChatCerebras(model=model_name, temperature=temperature, api_key=api_key)
    elif provider == "groq":
        from langchain_groq import ChatGroq

        raw_model = ChatGroq(
            model=model_name,  # type: ignore[arg-type]
            temperature=temperature,
            api_key=api_key,
            reasoning_effort="low",
        )
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        raw_model = ChatGoogleGenerativeAI(
            model=model_name,  # type: ignore[arg-type]
            temperature=temperature,
        )
    else:
        from langchain_nebius import ChatNebius

        raw_model = ChatNebius(model=model_name, api_key=api_key, temperature=temperature)

    if delay > 0:
        return _RateLimitedModel(raw_model, delay)  # type: ignore[return-value]
    return raw_model
