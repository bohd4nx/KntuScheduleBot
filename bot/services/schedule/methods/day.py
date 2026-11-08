from datetime import date

from bot.services.schedule.schemas import Lesson

from .week import get_week


async def get_day(day: date) -> list[Lesson]:
    return (await get_week(day)).get(day, [])
