from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DATA_DIR: Path
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=7)
    ACCESS_TOKEN_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
