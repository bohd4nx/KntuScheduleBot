from dataclasses import replace

from pydantic import TypeAdapter

from bot.core import LINKS_PATH, logger

from .schemas import Lesson, SubjectLinks, WeekSchedule


def load_links() -> dict[str, SubjectLinks]:
    if not LINKS_PATH.is_file():
        logger.info("%s not found; lessons are shown without online links", LINKS_PATH.name)
        return {}
    return TypeAdapter(dict[str, SubjectLinks]).validate_json(LINKS_PATH.read_bytes())


_LINKS = load_links()


def attach_link(lesson: Lesson) -> Lesson:
    links = _LINKS.get(lesson.subject)
    return replace(lesson, online_link=links.for_kind(lesson.kind)) if links else lesson


def attach_links(week: WeekSchedule) -> WeekSchedule:
    return {day: [attach_link(lesson) for lesson in lessons] for day, lessons in week.items()}
