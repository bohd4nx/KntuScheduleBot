import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        load_dotenv(env_path, encoding="utf-8")

        self.BOT_TOKEN: str = self._require_env("BOT_TOKEN")

        self.POSTGRES_USER: str = self._require_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD: str = self._require_env("POSTGRES_PASSWORD")
        self.POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
        self.POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
        self.POSTGRES_DB: str = self._require_env("POSTGRES_DB")

        self.SCHEDULE_GROUP: str | None = os.getenv("SCHEDULE_GROUP") or None
        self.PARSER_SOURCE_URL: str | None = os.getenv("PARSER_SOURCE_URL") or None

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if value and value.strip():
            return value

        logger.error("Missing required environment variable: %s", name)
        sys.exit(1)


config = Config()
