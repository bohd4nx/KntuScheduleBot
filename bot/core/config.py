import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        if not env_path.exists():
            logger.error(".env file not found!")
            sys.exit(1)

        load_dotenv(env_path)

        if not os.getenv("BOT_TOKEN"):
            logger.error("Missing required env variable: BOT_TOKEN")
            sys.exit(1)

        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN")

        semester_start_str = os.getenv("SEMESTER_START_DATE", "16.02.2026")
        semester_end_str = os.getenv("SEMESTER_END_DATE", "01.07.2026")

        self.SEMESTER_START_DATE: datetime = datetime.strptime(semester_start_str, "%d.%m.%Y")
        self.SEMESTER_END_DATE: datetime = datetime.strptime(semester_end_str, "%d.%m.%Y")


config = Config()
