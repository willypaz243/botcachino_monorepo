from typing import Annotated

from pydantic import BaseModel, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class ModelConfig(BaseModel):
    """Configuración del modelo LLM"""

    provider: str = "nebius"
    name: str = "openai/gpt-oss-120b-fast"
    temperature: float = 0.3
    base_url: str | None = None


class AgentConfig(BaseModel):
    """Configuración del agente"""

    university_name: str = "la universidad"
    max_search_retries: int = 5
    default_search_limit: int = 20
    max_response_tokens: int = 1024

    model: ModelConfig
    router_model: ModelConfig


class DatabaseConfig(BaseModel):
    """Configuración de la base de datos"""

    url: SecretStr = SecretStr("postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino")

    model_config = SettingsConfigDict(env_nested_delimiter="_")


class ApiConfig(BaseModel):
    """Configuración del servidor API"""

    key: str = ""
    allowed_origins: Annotated[list[str], NoDecode]
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    model_config = SettingsConfigDict(env_nested_delimiter="_")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def decode_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [origin.strip() for origin in value.split(",")]


class Settings(BaseSettings):
    """Clase principal de configuración"""

    agent: AgentConfig
    database: DatabaseConfig
    api: ApiConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()  # type: ignore
