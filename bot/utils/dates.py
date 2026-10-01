from datetime import datetime, timedelta
from typing import Final, Literal
from zoneinfo import ZoneInfo

# Контейнер працює в UTC, а «сьогодні» має рахуватися за Києвом
KYIV_TZ: Final = ZoneInfo("Europe/Kyiv")


def now() -> datetime:
    """Поточний київський час без tzinfo (як і решта дат у проєкті)."""
    return datetime.now(KYIV_TZ).replace(tzinfo=None)


def get_week_monday() -> datetime:
    """Понеділок поточного тижня; у суботу й неділю — наступного."""
    today = now()
    if today.weekday() >= 5:
        return today + timedelta(days=7 - today.weekday())
    return today - timedelta(days=today.weekday())


def get_week_dates() -> tuple[datetime, datetime]:
    """Межі робочого тижня: понеділок і п'ятниця."""
    monday = get_week_monday()
    return monday, monday + timedelta(days=4)


def get_week_type(date: datetime) -> Literal["numerator", "denominator"]:
    """Тип тижня: парний ISO-тиждень — чисельник, непарний — знаменник."""
    return "numerator" if date.isocalendar()[1] % 2 == 0 else "denominator"
