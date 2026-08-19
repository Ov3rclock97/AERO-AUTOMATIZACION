from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    DEFAULT_USERNAME: str = "admin"
    DEFAULT_PASSWORD: str = "secret"
    DEFAULT_ENABLE: str = "secret"

    BACKUP_DIR: Path = Path("backups/")
    TEMPLATE_DIR: Path = Path("templates/")
    INVENTORY_DB: str = "inventory.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
