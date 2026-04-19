from pydantic import SecretStr

from langchain_core.language_models import BaseChatModel


def get_chat_model(
    provider: str = "nebius",
    model_name: str | None = None,
    temperature: float = 0.3,
    api_key: SecretStr | str | None = None,
) -> BaseChatModel:
    """Create a chat model instance based on provider config.

    Providers: "nebius", "openai", "anthropic"
    Falls back to "nebius" for any unrecognized provider.
    """
    if provider == "openai":
        from langchain_openai import ChatOpenAI  # type: ignore[no-redef]

        return ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)  # type: ignore[arg-type]
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic  # type: ignore[import-not-found, no-redef]

        return ChatAnthropic(model=model_name, temperature=temperature, api_key=api_key)  # type: ignore[arg-type]
    else:
        from langchain_nebius import ChatNebius

        return ChatNebius(model=model_name, api_key=api_key, temperature=temperature)  # type: ignore[arg-type]
