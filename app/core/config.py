import sys
from tkinter import BASELINE

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    GOOGLE_API_BASE: str = ""
    LLM_MODEL: str = "gemini-3.1-flash-lite-preview"

    # Video Settings
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # default: 50 mb
    TEMP_DIR: str = "temp_files"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

logger.remove()

logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)
