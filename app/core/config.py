"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    APP_TITLE: str = "Shipment API"
    APP_DESCRIPTION: str = "API for managing shipments"
    APP_VERSION: str = "1.0.0"
    
    DATABASE_PATH: str = "sqlite.db"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()