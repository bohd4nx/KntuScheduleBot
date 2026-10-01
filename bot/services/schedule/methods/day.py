from datetime import date

from ..schemas import Lesson
from .week import get_week


async def get_day(day: date) -> list[Lesson]:
    return (await get_week(day)).get(day, [])
