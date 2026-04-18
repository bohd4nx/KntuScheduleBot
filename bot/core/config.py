import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .constants import SEMESTER_END_DATE, SEMESTER_START_DATE

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        if not env_path.exists():
            logger.error(".env file not found! Please create one from .env.example")
            sys.exit(1)

        load_dotenv(env_path)

        self.BOT_TOKEN: str = self._require_env("BOT_TOKEN")
        self.PARSER_SOURCE_URL: str | None = os.getenv("PARSER_SOURCE_URL", "").strip() or None
        self.SCHEDULE_GROUP: str | None = os.getenv("SCHEDULE_GROUP", "").strip() or None
        self.SEMESTER_START_DATE = SEMESTER_START_DATE
        self.SEMESTER_END_DATE = SEMESTER_END_DATE

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if value and value.strip():
            return value

        logger.error("Missing required environment variable: %s", name)
        sys.exit(1)
        raise RuntimeError  # unreachable, satisfies mypy


config = Config()
