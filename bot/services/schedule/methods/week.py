import asyncio
import time
from datetime import date, timedelta
from typing import Any

from pydantic import ValidationError

from bot.core import logger
from bot.services import cache
from bot.services.schedule.client import get_json
from bot.services.schedule.constants import CACHE_TTL_SECONDS
from bot.services.schedule.exceptions import PortalError
from bot.services.schedule.links import attach_links
from bot.services.schedule.schemas import Timetable, WeekSchedule

# Захист від паралельних однакових запитів до порталу в межах процесу.
_fetch_lock = asyncio.Lock()


def parse_week(payload: Any) -> WeekSchedule:
    try:
        week = Timetable.model_validate(payload).to_week()
    except ValidationError as exc:
        raise PortalError(f"Malformed timetable payload: {exc}") from exc
    return attach_links(week)


async def fetch_week(monday: date) -> Any:
    params = {"dateStart": monday.isoformat(), "dateEnd": (monday + timedelta(days=6)).isoformat()}
    return await get_json("student/me/timetable", params=params)


async def get_week(day: date) -> WeekSchedule:
    """Тиждень, що містить `day`. Кеш у Redis на 12 годин; якщо портал недоступний — віддає застарілий."""
    monday = day - timedelta(days=day.weekday())
    async with _fetch_lock:
        cached = await cache.schedule.get_week(monday)
        if cached and time.time() - cached.fetched_at < CACHE_TTL_SECONDS:
            try:
                return parse_week(cached.payload)
            except PortalError:
                cached = None  # формат змінився — запис непридатний, беремо з порталу

        try:
            payload = await fetch_week(monday)
            week = parse_week(payload)
        except PortalError:
            if cached:
                logger.warning("Portal unavailable, serving stale schedule for week %s", monday)
                return parse_week(cached.payload)
            raise

        # Кешуємо лише валідну відповідь; порожній тиждень теж валідний.
        await cache.schedule.set_week(monday, payload)
        return week
