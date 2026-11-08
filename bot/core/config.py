import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import ROOT_PATH

logger = logging.getLogger(__name__)


def load_env() -> None:
    # override=False: змінні процесу завжди важливіші за .env.
    candidates = [
        Path(os.environ["ENV_FILE"]).resolve() if os.getenv("ENV_FILE") else None,
        ROOT_PATH / ".env",
    ]

    loaded = False
    for path in candidates:
        if path is not None and path.is_file():
            load_dotenv(path, override=False)
            loaded = True

    if not loaded:
        logger.info("No .env file found; using process environment.")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    BOT_TOKEN: SecretStr
    # Портал ротує refresh-токен при кожному оновленні, тож актуальний лежить у Redis,
    # а змінна лише запускає перший старт.
    PORTAL_REFRESH_TOKEN: SecretStr
    REDIS_URL: str = "redis://redis:6379/0"
    GROUP_ID: int | None = None

    @field_validator("BOT_TOKEN", "PORTAL_REFRESH_TOKEN", mode="before")
    @classmethod
    def validate_token(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("must not be empty")
        return value

    @field_validator("GROUP_ID", mode="before")
    @classmethod
    def normalize_group_id(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip() or None
        return value


def load_settings() -> Settings:
    load_env()
    try:
        # Обов'язкові поля BaseSettings бере з оточення під час запуску — mypy цього не бачить.
        return Settings()  # type: ignore[call-arg]
    except ValidationError as exc:
        for error in exc.errors():
            field = ".".join(map(str, error["loc"])) or "unknown"
            logger.error("Invalid configuration for %s: %s", field, error["msg"])
        raise SystemExit(1) from exc


settings = load_settings()
