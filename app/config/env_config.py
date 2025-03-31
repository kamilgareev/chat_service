from pydantic_settings import SettingsConfigDict

from app.config.base import BaseConfig


class DatabaseConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')

    db_url: str
