import json
from datetime import datetime, timedelta
from pathlib import Path

from bot.core import config


class ScheduleService:
    DAYS: list[str] = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]

    def __init__(self) -> None:
        self._schedule_data = self._load_schedule()

    @staticmethod
    def _load_schedule() -> dict:
        schedule_path = Path(__file__).resolve().parents[2] / "schedule.json"
        with open(schedule_path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_week_type() -> str:
        weeks_passed = (datetime.now() - config.SEMESTER_START_DATE).days // 7
        return "numerator" if weeks_passed % 2 == 0 else "denominator"

    def get_current_day(self) -> str:
        return self.DAYS[datetime.now().weekday()]

    def get_day_schedule(self, day: str, week_type: str | None = None) -> list[dict[str, str]]:
        week_type = week_type or self.get_week_type()
        day_data = self._schedule_data["schedule"].get(day, {})

        lessons = []
        for lesson_num, lesson_data in day_data.items():
            if not isinstance(lesson_data, dict):
                continue

            lesson_info = lesson_data.get(week_type)
            if not lesson_info:
                continue

            time = self._schedule_data["class_times"][lesson_num]
            lessons.append({
                "number": lesson_num,
                "start": time["start"],
                "end": time["end"],
                "subject": lesson_info.get("subject", "Невідомо"),
                "teacher": lesson_info.get("teacher", "Невідомо"),
                "room": lesson_info.get("room", "Невідомо"),
            })

        return sorted(lessons, key=lambda x: int(x["number"]))

    def get_today_schedule(self) -> tuple[str, list[dict[str, str]], datetime]:
        day = self.get_current_day()
        return day, self.get_day_schedule(day), datetime.now()

    def get_tomorrow_schedule(self) -> tuple[str, list[dict[str, str]], datetime]:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_day = self.DAYS[tomorrow.weekday()]

        week_type = self.get_week_type()
        if tomorrow.weekday() == 0 and datetime.now().weekday() == 6:
            week_type = "denominator" if week_type == "numerator" else "numerator"

        return tomorrow_day, self.get_day_schedule(tomorrow_day, week_type), tomorrow

    def get_week_schedule(self, week_type: str | None = None) -> dict[str, tuple[list[dict[str, str]], datetime]]:
        week_type = week_type or self.get_week_type()
        today = datetime.now()
        workdays = self.DAYS[:5]

        schedule = {}
        for day in workdays:
            lessons = self.get_day_schedule(day, week_type)
            if lessons:
                day_index = workdays.index(day)
                offset = day_index - today.weekday()
                day_date = datetime.now() + timedelta(days=offset)
                schedule[day] = (lessons, day_date)

        return schedule

    @staticmethod
    def get_week_dates() -> tuple[datetime, datetime]:
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        friday = monday + timedelta(days=4)
        return monday, friday


schedule_service = ScheduleService()
