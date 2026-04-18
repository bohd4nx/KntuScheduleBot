from datetime import datetime

from aiogram_i18n import I18nContext

from bot.core.constants import (
    CURATOR_CLASS_TIMES,
    CURATOR_HOUR_DATES,
    DATE_FORMAT,
    REGULAR_CLASS_TIMES,
    get_week_dates,
    get_week_type,
)
from bot.database.models.lesson import Lesson


def _is_curator_day(date: datetime) -> bool:
    """Перевіряє, чи є дана дата кураторською годиною."""
    return date.strftime(DATE_FORMAT) in CURATOR_HOUR_DATES


def _format_lesson(i18n: I18nContext, lesson: Lesson, curator_day: bool = False) -> str:
    """Форматує одну пару в локалізований рядок."""
    teachers_count = len(lesson.teacher.split(", "))
    times = (CURATOR_CLASS_TIMES if curator_day else REGULAR_CLASS_TIMES).get(lesson.lesson_number, {})

    # Спортзал виводиться інакше, будь-яка інша аудиторія — зі знаком кімнати.
    room_display = {"Спортзал": i18n.get("room-gym")}.get(lesson.room, i18n.get("room-regular", room=lesson.room))
    online_link_display = f"{i18n.get('online-link', url=lesson.online_link)}\n" if lesson.online_link else ""

    return i18n.get(
        "lesson-item",
        number=lesson.lesson_number,
        subject=lesson.subject,
        time=f"{times.get('start', '')} – {times.get('end', '')}",
        teachers_count=teachers_count,
        teacher=lesson.teacher,
        room_display=room_display,
        online_link_display=online_link_display,
    )


def format_day_schedule(
    i18n: I18nContext,
    day: str,
    lessons: list[Lesson],
    date: datetime,
    holiday_name: str | None = None,
) -> str:
    """Форматує розклад на один день."""
    week_type = i18n.get(f"week-{get_week_type(date)}")
    curator_day = _is_curator_day(date)
    header = i18n.get("day-schedule", day=day, week_type=week_type, date=date)
    if curator_day:
        header += f" {i18n.get('curator-hour')}"
    if holiday_name:
        header += f" {i18n.get('possible-holiday', holiday=holiday_name)}"
    parts = [header, ""]
    for i, lesson in enumerate(lessons):
        parts.append(_format_lesson(i18n, lesson, curator_day))
        if i < len(lessons) - 1:
            parts.append("")
    return "\n".join(parts)


def format_week_schedule(
    i18n: I18nContext,
    week_schedule: dict[str, tuple[list[Lesson], datetime]],
    holiday_names: dict[datetime, str] | None = None,
) -> str:
    """Форматує розклад на весь тиждень у вигляді блокцит, один день — один блок."""
    start_date, _ = get_week_dates()
    week_type = i18n.get(f"week-{get_week_type(start_date)}")

    parts = [
        i18n.get("week-schedule-header", week_type=week_type),
        "",
    ]
    for day, (lessons, day_date) in week_schedule.items():
        curator_day = _is_curator_day(day_date)
        header = i18n.get("week-day-header", day=day, date=day_date)
        if curator_day:
            header += f" {i18n.get('curator-hour-week')}"
        holiday = (holiday_names or {}).get(day_date)
        if holiday:
            header += f" {i18n.get('possible-holiday-week', holiday=holiday)}"
        parts.append(header)
        lessons_text = "\n\n".join(_format_lesson(i18n, lesson, curator_day) for lesson in lessons)
        parts.append(f"<blockquote expandable>{lessons_text}</blockquote>")
        parts.append("")

    return "\n".join(parts)
