import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        self.ROOT_DIR: Path = Path(__file__).resolve().parents[2]
        self.LOCALES_DIR: Path = self.ROOT_DIR / "locales"
        self.DEFAULT_LOCALE: str = "uk"

        load_dotenv(self.ROOT_DIR / ".env", encoding="utf-8")

        self.BOT_TOKEN: str = self._require_env("BOT_TOKEN")

        # Refresh-токен порталу (cookie staffportal_refresh). Портал ротує його при кожному оновленні,
        # тож актуальний лежить у Redis, а змінна лише запускає перший старт.
        self.PORTAL_REFRESH_TOKEN: str = self._require_env("PORTAL_REFRESH_TOKEN")

        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if value and value.strip():
            return value

        logger.error("Missing required environment variable: %s", name)
        sys.exit(1)


config = Config()
