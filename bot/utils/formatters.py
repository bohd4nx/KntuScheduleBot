from datetime import datetime

from aiogram_i18n import I18nContext

from bot.services import schedule_service


def _format_lesson(i18n: I18nContext, lesson: dict[str, str]) -> str:
    teachers_count = len(lesson["teacher"].split(", "))

    room_display = {
        "Спортзал": i18n.get("room-gym")
    }.get(lesson["room"], i18n.get("room-regular", room=lesson["room"]))

    return i18n.get(
        "lesson-item",
        number=lesson["number"],
        subject=lesson["subject"],
        time=f"{lesson['start']}–{lesson['end']}",
        teachers_count=teachers_count,
        teacher=lesson["teacher"],
        room_display=room_display
    )


def format_day_schedule(i18n: I18nContext, day: str, lessons: list[dict[str, str]], date: datetime) -> str:
    week_type = i18n.get(f"week-{schedule_service.get_week_type()}")

    parts = [i18n.get("day-schedule", day=day, week_type=week_type, date=date), ""]

    for i, lesson in enumerate(lessons):
        parts.append(_format_lesson(i18n, lesson))
        if i < len(lessons) - 1:
            parts.append("")

    return "\n".join(parts)


def format_week_schedule(i18n: I18nContext, week_schedule: dict) -> str:
    week_type = i18n.get(f"week-{schedule_service.get_week_type()}")
    start_date, end_date = schedule_service.get_week_dates()

    parts = [
        i18n.get("week-schedule-header", week_type=week_type, start_date=start_date, end_date=end_date),
        ""
    ]

    for day, (lessons, day_date) in week_schedule.items():
        parts.append(i18n.get("week-day-header", day=day, date=day_date) + "\n")
        parts.append("<blockquote expandable>")

        for i, lesson in enumerate(lessons):
            parts.append(_format_lesson(i18n, lesson))
            if i < len(lessons) - 1:
                parts.append("")

        parts.append("</blockquote>")
        parts.append("")

    return "\n".join(parts)
