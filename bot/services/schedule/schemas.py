import datetime as dt
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from .enums import LessonKind


@dataclass(frozen=True, slots=True)
class Lesson:
    """Пара у вигляді, в якому її показує бот."""

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


# Дата → пари дня. Тиждень без пар — порожній словник, не помилка.
WeekSchedule = dict[dt.date, list[Lesson]]


class PortalModel(BaseModel):
    """База відповідей порталу: camelCase у JSON, snake_case у Python, зайві ключі ігноруються."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )


class Call(PortalModel):
    number: int
    time_start: str | None = None
    time_end: str | None = None


class Period(PortalModel):
    discipline_full_name: str | None = None
    discipline_short_name: str | None = None
    classroom: str | None = None
    time_start: str | None = None
    time_end: str | None = None
    type: LessonKind | None = None
    teachers_name: str | None = None
    teachers_name_full: str | None = None
    groups: str | None = None
    notice: str | None = None
    info: str | None = None

    @field_validator("type", mode="before")
    @classmethod
    def _known_kind(cls, value: Any) -> LessonKind | None:
        # Невідомий код типу не ламає розклад — просто без мітки.
        try:
            return LessonKind(value)
        except ValueError:
            return None

    @field_validator("notice", "info")
    @classmethod
    def _blank_to_none(cls, value: str | None) -> str | None:
        return (value or "").strip() or None

    def to_lesson(self, number: int, call: Call | None) -> Lesson:
        # Якщо в парі немає власного часу — беремо з розкладу дзвінків.
        return Lesson(
            number=number,
            subject=self.discipline_full_name or self.discipline_short_name or "—",
            kind=self.type,
            teacher=self.teachers_name_full or self.teachers_name or "",
            room=self.classroom,
            start=self.time_start or (call.time_start if call else None) or "",
            end=self.time_end or (call.time_end if call else None) or "",
            groups=self.groups or "",
            notice=self.notice,
            info=self.info,
        )


class Slot(PortalModel):
    number: int
    periods: list[Period]


class Day(PortalModel):
    date: dt.date
    lessons: list[Slot]


class Timetable(PortalModel):
    """Відповідь `GET /student/me/timetable`. `days` обов'язкове, але може бути порожнім (канікули)."""

    days: list[Day]
    calls: list[Call] = []

    def to_week(self) -> WeekSchedule:
        calls = {call.number: call for call in self.calls}
        week: WeekSchedule = {}
        for day in self.days:
            lessons = [period.to_lesson(slot.number, calls.get(slot.number)) for slot in day.lessons for period in slot.periods]
            if lessons:
                week[day.date] = sorted(lessons, key=lambda lesson: lesson.number)
        return week
