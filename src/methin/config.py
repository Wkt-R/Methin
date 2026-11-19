from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    discord_token: str = ""
    dev_guild_id: int | None = None
    database_url: str = "postgresql+asyncpg://methin:methin@localhost:5432/methin"
    test_database_url: str = "postgresql+asyncpg://methin:methin@localhost:5432/methin_test"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
