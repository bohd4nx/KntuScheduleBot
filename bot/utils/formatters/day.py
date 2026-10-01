from datetime import datetime

from aiogram_i18n import I18nContext

from bot.services.schedule import Lesson
from bot.utils.constants import DAYS
from bot.utils.dates import get_week_type

from .lesson import format_lesson


def format_day_schedule(i18n: I18nContext, lessons: list[Lesson], date: datetime) -> str:
    parts = [
        i18n.get("day-schedule", day=DAYS[date.weekday()], date=date, week_type=i18n.get(f"week-{get_week_type(date)}")),
        "",
    ]
    for i, lesson in enumerate(lessons):
        parts.append(format_lesson(i18n, lesson))
        if i < len(lessons) - 1:
            parts.append("")
    return "\n".join(parts)
