from html import escape

from aiogram_i18n import I18nContext

from bot.services.schedule import Lesson


def format_lesson(i18n: I18nContext, lesson: Lesson) -> str:
    teachers_count = len(lesson.teacher.split(",")) if lesson.teacher else 0

    room = lesson.room or "Невідомо"
    room_display = {"спортзал": i18n.get("room-gym")}.get(room.lower(), i18n.get("room-regular", room=escape(room)))
    notes_display = "".join(
        f"{i18n.get(key, text=escape(text))}\n"
        for key, text in (("lesson-notice", lesson.notice), ("lesson-info", lesson.info))
        if text
    )
    online_link_display = f"{i18n.get('online-link', url=escape(lesson.online_link))}\n" if lesson.online_link else ""

    return i18n.get(
        "lesson-item",
        number=lesson.number,
        subject=escape(lesson.subject),
        kind_display=f" · {i18n.get(f'lesson-kind-{lesson.kind.name.lower()}')}" if lesson.kind else "",
        time=f"{lesson.start} – {lesson.end}",
        teachers_count=teachers_count,
        teacher=escape(lesson.teacher),
        room_display=room_display,
        notes_display=notes_display,
        online_link_display=online_link_display,
    )
