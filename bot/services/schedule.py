from datetime import datetime, timedelta
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import config
from bot.core.constants import DAYS, WORK_DAYS, get_week_monday, get_week_type
from bot.database.crud import get_lessons
from bot.database.models import Lesson


class ScheduleService:
    async def get_day_schedule(
        self,
        session: AsyncSession,
        day: str,
        week_type: Literal["numerator", "denominator"] | None = None,
    ) -> list[Lesson]:
        group = config.SCHEDULE_GROUP or ""
        wt = week_type or get_week_type(datetime.now())
        rows = await get_lessons(session, group, day, wt)
        return rows

    async def get_today_schedule(self, session: AsyncSession) -> tuple[str, list[Lesson], datetime]:
        today = datetime.now()
        day = DAYS[today.weekday()]
        return day, await self.get_day_schedule(session, day), today

    async def get_tomorrow_schedule(self, session: AsyncSession) -> tuple[str, list[Lesson], datetime]:
        tomorrow = datetime.now() + timedelta(days=1)
        day = DAYS[tomorrow.weekday()]
        return day, await self.get_day_schedule(session, day, get_week_type(tomorrow)), tomorrow

    async def get_week_schedule(
        self,
        session: AsyncSession,
        week_type: Literal["numerator", "denominator"] | None = None,
    ) -> dict[str, tuple[list[Lesson], datetime]]:
        monday = get_week_monday()
        wt = week_type or get_week_type(monday)
        result: dict[str, tuple[list[Lesson], datetime]] = {}
        for i, day in enumerate(WORK_DAYS):
            lessons = await self.get_day_schedule(session, day, wt)
            if lessons:
                result[day] = (lessons, monday + timedelta(days=i))
        return result


schedule_service = ScheduleService()
