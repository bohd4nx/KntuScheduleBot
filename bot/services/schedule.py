from datetime import datetime, timedelta
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import DAYS, WORK_DAYS, config
from bot.core.constants import REGULAR_CLASS_TIMES
from bot.database.crud import get_lessons
from bot.database.models import Lesson


class ScheduleService:
    @staticmethod
    def get_week_type(date: datetime) -> Literal["numerator", "denominator"]:
        # Семестр стартував на 8-му ISO-тижні (16.02.2026) як чисельник.
        # 8-й тиждень — парний, тому: парний = чисельник, непарний = знаменник.
        return "numerator" if date.isocalendar()[1] % 2 == 0 else "denominator"

    @staticmethod
    def _get_week_monday() -> datetime:
        today = datetime.now()
        # Якщо сьогодні субота або неділя — переходимо до наступного понеділка.
        return today + timedelta(days=7 - today.weekday()) if today.weekday() >= 5 else today - timedelta(days=today.weekday())

    async def get_day_schedule(
        self,
        session: AsyncSession,
        day: str,
        week_type: Literal["numerator", "denominator"] | None = None,
    ) -> list[Lesson]:
        group = config.SCHEDULE_GROUP or ""
        wt = week_type or self.get_week_type(datetime.now())
        rows = await get_lessons(session, group, day, wt)
        # Час пари не зберігається в БД — додаємо з констант на льоту.
        for row in rows:
            times = REGULAR_CLASS_TIMES.get(row.lesson_number, {})
            row.__dict__.setdefault("start", times.get("start", ""))
            row.__dict__.setdefault("end", times.get("end", ""))
        return rows

    async def get_today_schedule(self, session: AsyncSession) -> tuple[str, list[Lesson], datetime]:
        now = datetime.now()
        day = DAYS[now.weekday()]
        return day, await self.get_day_schedule(session, day), now

    async def get_tomorrow_schedule(self, session: AsyncSession) -> tuple[str, list[Lesson], datetime]:
        tomorrow = datetime.now() + timedelta(days=1)
        day = DAYS[tomorrow.weekday()]
        return day, await self.get_day_schedule(session, day, self.get_week_type(tomorrow)), tomorrow

    async def get_week_schedule(
        self,
        session: AsyncSession,
        week_type: Literal["numerator", "denominator"] | None = None,
    ) -> dict[str, tuple[list[Lesson], datetime]]:
        monday = self._get_week_monday()
        wt = week_type or self.get_week_type(monday)
        result: dict[str, tuple[list[Lesson], datetime]] = {}
        for i, day in enumerate(WORK_DAYS):
            lessons = await self.get_day_schedule(session, day, wt)
            if lessons:
                result[day] = (lessons, monday + timedelta(days=i))
        return result

    def get_week_dates(self) -> tuple[datetime, datetime]:
        monday = self._get_week_monday()
        return monday, monday + timedelta(days=4)


schedule_service = ScheduleService()
