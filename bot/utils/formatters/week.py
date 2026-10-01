from datetime import date, datetime, time

from aiogram_i18n import I18nContext

from bot.services.schedule import Lesson
from bot.utils.constants import DAYS
from bot.utils.dates import get_week_dates, get_week_type

from .lesson import format_lesson


def format_week_schedule(i18n: I18nContext, week: dict[date, list[Lesson]]) -> str:
    start_date, end_date = get_week_dates()

    parts = [
        i18n.get(
            "week-schedule-header", start=start_date, end=end_date, week_type=i18n.get(f"week-{get_week_type(start_date)}")
        ),
        "",
    ]
    for day, lessons in sorted(week.items()):
        parts.append(i18n.get("week-day-header", day=DAYS[day.weekday()], date=datetime.combine(day, time())))
        lessons_text = "\n\n".join(format_lesson(i18n, lesson) for lesson in lessons)
        parts.append(f"<blockquote expandable>{lessons_text}</blockquote>")
        parts.append("")

    return "\n".join(parts)
