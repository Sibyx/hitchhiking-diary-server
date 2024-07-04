import tomllib
from datetime import timedelta
from pathlib import Path
from typing import Optional

from pydantic import computed_field, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: Optional[str] = Field(default="")
    PGPORT: Optional[int] = Field(default=5432)

    NAME: str
    DESCRIPTION: str
    VERSION: str
    BASE_DIR: Path
    DATA_DIR: Path
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=7)
    ACCESS_TOKEN_ALGORITHM: str = "HS256"

    def __init__(self, *args, **kwargs):
        base_dir = Path(__file__).resolve(strict=True).parent.parent.parent
        kwargs.setdefault("BASE_DIR", base_dir)

        with open(base_dir / "pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
            kwargs.setdefault("NAME", pyproject["tool"]["poetry"]["name"])
            kwargs.setdefault("DESCRIPTION", pyproject["tool"]["poetry"]["description"])
            kwargs.setdefault("VERSION", pyproject["tool"]["poetry"]["version"])

        super().__init__(*args, **kwargs)

    @computed_field
    def database_url(self) -> str:
        if self.PGPASSWORD:
            return (
                f"postgresql+psycopg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"
            )
        else:
            return f"postgresql+psycopg://{self.PGUSER}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
