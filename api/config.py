import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API Configuration"""

    # API Settings
    api_title: str = "Panorama API"
    api_version: str = "1.0.0"
    api_description: str = "Market Intelligence Analysis API"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Database paths
    history_db_path: str = "data/history.db"
    cache_db_path: str = "data/cache.db"

    # Query limits
    max_query_length: int = 5000
    min_query_length: int = 3

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
