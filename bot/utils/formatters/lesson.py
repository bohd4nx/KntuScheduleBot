from aiogram_i18n import I18nContext

from bot.services.schedule import Lesson

from .text import quote_html


def format_lesson(i18n: I18nContext, lesson: Lesson) -> str:
    teachers_count = len(lesson.teacher.split(",")) if lesson.teacher else 0

    # Спортзал показуємо окремим текстом, решту — як аудиторію.
    room = lesson.room or "Невідомо"
    room_display = {"спортзал": i18n.get("room-gym")}.get(room.lower(), i18n.get("room-regular", room=quote_html(room)))
    notes_display = "".join(
        f"{i18n.get(key, text=quote_html(text))}\n"
        for key, text in (("lesson-notice", lesson.notice), ("lesson-info", lesson.info))
        if text
    )

    return i18n.get(
        "lesson-item",
        number=lesson.number,
        subject=quote_html(lesson.subject),
        kind_display=f" · {lesson.kind.label}" if lesson.kind else "",
        time=f"{lesson.start} – {lesson.end}",
        teachers_count=teachers_count,
        teacher=quote_html(lesson.teacher),
        room_display=room_display,
        notes_display=notes_display,
    )
