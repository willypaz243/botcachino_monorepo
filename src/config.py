import os

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class NebiusConfig(BaseModel):
    api_key: SecretStr
    emb_model: str = "Qwen/Qwen3-Embedding-8B"


class DatabaseConfig(BaseModel):
    url: SecretStr = SecretStr("postgresql+asyncpg://postgres:postgres@localhost:5432/botcachino")


class Settings(BaseSettings):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    nebius: NebiusConfig
    database: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        env_nested_max_split=1,
        extra="ignore",
    )


_env_file = ".env"

match os.getenv("ENV"):
    case "prod":
        _env_file = "prod.env"
    case "dev":
        _env_file = "dev.env"
    case _:
        _env_file = ".env"


settings = Settings(_env_file=_env_file)
