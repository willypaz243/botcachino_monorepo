import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseModel):
    provider: str = "nebius"
    name: str = "openai/gpt-oss-120b-fast"
    temperature: float = 0.3
    api_key: str | None = None
    base_url: str | None = None


class RouterModelConfig(BaseModel):
    provider: str = "nebius"
    name: str = "openai/gpt-oss-120b-fast"
    temperature: float = 0.1
    api_key: str | None = None
    base_url: str | None = None


class AgentSettings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    university_name: str = "la universidad"
    model: ModelConfig = ModelConfig()
    router_model: RouterModelConfig = RouterModelConfig()
    max_search_retries: int = 5
    default_search_limit: int = 5
    max_response_tokens: int = 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        env_nested_max_split=2,
        extra="ignore",
    )


def _get_env_file() -> str:
    match os.getenv("ENV"):
        case "prod":
            return "prod.env"
        case "dev":
            return "dev.env"
        case _:
            return ".env"


agent_settings = AgentSettings(_env_file=_get_env_file())
