"""
src/config.py

Centralized application settings, loaded from environment variables
(and a local .env file if present). Import `settings` anywhere you
need a config value instead of calling os.getenv() directly.
"""

import os
from functools import lru_cache

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    # --- App ---
    APP_NAME: str = os.getenv("APP_NAME", "Token2025 API")
    ENV: str = os.getenv("ENV", "development")          # development | staging | production
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # --- Database ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # --- Security / JWT ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # --- CORS ---
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance (loaded once per process)."""
    return Settings()


settings = get_settings()
