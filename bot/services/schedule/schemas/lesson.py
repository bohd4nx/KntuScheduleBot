import datetime as dt
from dataclasses import dataclass

from bot.services.schedule.enums import LessonKind


@dataclass(frozen=True, slots=True)
class Lesson:
    number: int
    subject: str
    kind: LessonKind | None
    teacher: str
    room: str | None
    start: str
    end: str
    groups: str
    notice: str | None
    info: str | None
    online_link: str | None = None


# Дата → пари дня. Тиждень без пар — порожній словник, не помилка.
WeekSchedule = dict[dt.date, list[Lesson]]
