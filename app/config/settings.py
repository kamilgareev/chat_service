from pydantic import Field

from base import BaseConfig
from env_config import DatabaseConfig


class Settings(BaseConfig):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

settings = Settings()
