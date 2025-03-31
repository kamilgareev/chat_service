from pydantic import Field

from app.config.base import BaseConfig
from app.config.env_config import DatabaseConfig


class Settings(BaseConfig):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

settings = Settings()
