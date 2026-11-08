from datetime import datetime, timedelta

from .constants import KYIV_TZ, WORK_DAYS_COUNT
from .enums import WeekType


def now() -> datetime:
    """Поточний київський час без tzinfo (як і решта дат у проєкті)."""
    return datetime.now(KYIV_TZ).replace(tzinfo=None)


def get_week_monday() -> datetime:
    """Понеділок поточного тижня; у суботу й неділю — наступного."""
    today = now()
    if today.weekday() >= WORK_DAYS_COUNT:
        return today + timedelta(days=7 - today.weekday())
    return today - timedelta(days=today.weekday())


def get_week_dates() -> tuple[datetime, datetime]:
    """Межі робочого тижня: понеділок і п'ятниця."""
    monday = get_week_monday()
    return monday, monday + timedelta(days=WORK_DAYS_COUNT - 1)


def get_week_type(date: datetime) -> WeekType:
    """Парний ISO-тиждень — чисельник, непарний — знаменник."""
    return WeekType.NUMERATOR if date.isocalendar()[1] % 2 == 0 else WeekType.DENOMINATOR
