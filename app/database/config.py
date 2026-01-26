from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root: two levels up from app/database/config.py
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"


class DatabaseSettings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        extra="ignore"
    )

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# Settings loaded from .env file - type checker can't verify .env contents
settings = DatabaseSettings()  # type: ignore[call-arg]

print(settings)
print(__file__) # absolute path to current file 