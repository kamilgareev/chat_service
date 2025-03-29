from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class DatabaseConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')

    DB_URL: str
