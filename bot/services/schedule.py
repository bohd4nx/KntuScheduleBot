# TODO: замінити на роботу з БД.
from datetime import datetime, timedelta
from typing import Any, Literal, TypedDict

from bot.core import DAYS, WORK_DAYS
from bot.core.constants import REGULAR_CLASS_TIMES


class Lesson(TypedDict):
    number: str
    start: str
    end: str
    subject: str
    teacher: str
    room: str
    online_link: str


class ScheduleService:
    """Сервіс для роботи з розкладом. Поки що заглушка — дані беруться з парсера."""

    def __init__(self) -> None:
        # Поки заглушка: порожній розклад. Буде замінено на БД.
        self._schedule: dict[str, dict[str, Any]] = {}

    @staticmethod
    def get_week_type(date: datetime) -> Literal["numerator", "denominator"]:
        # Семестр стартував на 8-му ISO-тижні (16.02.2026) як чисельник.
        # 8-й тиждень — парний, тому: парний = чисельник, непарний = знаменник.
        return "numerator" if date.isocalendar()[1] % 2 == 0 else "denominator"

    def get_day_schedule(self, day: str, week_type: Literal["numerator", "denominator"] | None = None) -> list[Lesson]:
        week_type = week_type or self.get_week_type(datetime.now())
        day_data = self._schedule.get(day, {})

        lessons: list[Lesson] = []
        for lesson_num, lesson_data in day_data.items():
            if not isinstance(lesson_data, dict):
                continue

            lesson_info = lesson_data.get(week_type)
            if not lesson_info:
                continue

            time = REGULAR_CLASS_TIMES[lesson_num]
            lessons.append(
                {
                    "number": lesson_num,
                    "start": time["start"],
                    "end": time["end"],
                    "subject": lesson_info.get("subject", "Невідомо"),
                    "teacher": lesson_info.get("teacher", "Невідомо"),
                    "room": lesson_info.get("room", "Невідомо"),
                    "online_link": lesson_info.get("online_link", ""),
                }
            )

        return sorted(lessons, key=lambda lesson: int(lesson["number"]))

    def get_today_schedule(self) -> tuple[str, list[Lesson], datetime]:
        day = DAYS[datetime.now().weekday()]
        return day, self.get_day_schedule(day), datetime.now()

    def get_tomorrow_schedule(self) -> tuple[str, list[Lesson], datetime]:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_day = DAYS[tomorrow.weekday()]
        week_type = self.get_week_type(tomorrow)
        return tomorrow_day, self.get_day_schedule(tomorrow_day, week_type), tomorrow

    @staticmethod
    def _get_week_monday() -> datetime:
        today = datetime.now()
        # Якщо сьогодні субота або неділя — переходимо до наступного понеділка.
        return today + timedelta(days=7 - today.weekday()) if today.weekday() >= 5 else today - timedelta(days=today.weekday())

    def get_week_schedule(
        self, week_type: Literal["numerator", "denominator"] | None = None
    ) -> dict[str, tuple[list[Lesson], datetime]]:
        monday = self._get_week_monday()
        week_type = week_type or self.get_week_type(monday)
        schedule: dict[str, tuple[list[Lesson], datetime]] = {}
        for day_index, day in enumerate(WORK_DAYS):
            lessons = self.get_day_schedule(day, week_type)
            if lessons:
                day_date = monday + timedelta(days=day_index)
                schedule[day] = (lessons, day_date)
        return schedule

    def get_week_dates(self) -> tuple[datetime, datetime]:
        monday = self._get_week_monday()
        friday = monday + timedelta(days=4)
        return monday, friday


schedule_service = ScheduleService()
