# src/config.py
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseModel):
    """Configuración del modelo LLM"""

    provider: str = "nebius"
    name: str = "openai/gpt-oss-120b-fast"
    temperature: float = 0.3
    api_key: SecretStr | None = None
    base_url: str | None = None


class AgentConfig(BaseModel):
    """Configuración del agente"""

    university_name: str = "la universidad"
    max_search_retries: int = 5
    default_search_limit: int = 5
    max_response_tokens: int = 1024

    model: ModelConfig
    router_model: ModelConfig

    # Configuración para que Pydantic lea variables de entorno anidadas
    model_config = SettingsConfigDict(
        env_nested_delimiter="_",  # Usar guion SIMPLE
        env_nested_max_split=1,
    )


class NebiusConfig(BaseModel):
    """Configuración de Nebius"""

    api_key: SecretStr
    emb_model: str = "Qwen/Qwen3-Embedding-8B"

    model_config = SettingsConfigDict(env_nested_delimiter="_")


class DatabaseConfig(BaseModel):
    """Configuración de la base de datos"""

    url: SecretStr = SecretStr("postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino")

    model_config = SettingsConfigDict(env_nested_delimiter="_")


class Settings(BaseSettings):
    """Clase principal de configuración"""

    nebius: NebiusConfig
    agent: AgentConfig
    database: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()  # type: ignore
