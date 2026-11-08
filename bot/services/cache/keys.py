from datetime import date

from .constants import KEY_PREFIX

PORTAL_REFRESH_TOKEN_KEY: str = f"{KEY_PREFIX}:portal:refresh_token"


def schedule_week_key(monday: date) -> str:
    return f"{KEY_PREFIX}:schedule:week:{monday.isoformat()}"
