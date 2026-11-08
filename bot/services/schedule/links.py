from dataclasses import replace

from pydantic import TypeAdapter, ValidationError

from bot.core import LINKS_PATH, logger

from .schemas import Lesson, SubjectLinks, WeekSchedule


def load_links() -> dict[str, SubjectLinks]:
    if not LINKS_PATH.is_file():
        logger.info("%s not found; lessons are shown without online links", LINKS_PATH.name)
        return {}
    try:
        return TypeAdapter(dict[str, SubjectLinks]).validate_json(LINKS_PATH.read_bytes())
    except ValidationError as exc:
        # Битий файл посилань не має забирати в людей увесь розклад.
        logger.error("%s is invalid; lessons are shown without online links: %s", LINKS_PATH.name, exc)
        return {}


_LINKS = load_links()


def attach_link(lesson: Lesson) -> Lesson:
    links = _LINKS.get(lesson.subject)
    return replace(lesson, online_link=links.for_kind(lesson.kind)) if links else lesson


def attach_links(week: WeekSchedule) -> WeekSchedule:
    return {day: [attach_link(lesson) for lesson in lessons] for day, lessons in week.items()}
