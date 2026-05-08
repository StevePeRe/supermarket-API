from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Supermarket API"
    api_prefix: str = "/api/v1"
    debug: bool = False

    database_url: str | None = None
    use_postgres: bool = False
    db_driver: str = "postgresql+psycopg"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "supermarket"
    db_user: str = "root"
    db_password: str = "password"
    db_echo: bool = False

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if self.use_postgres:
            encoded = quote_plus(self.db_password)
            return (
                f"{self.db_driver}://{self.db_user}:{encoded}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return "sqlite:///./supermarket.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
