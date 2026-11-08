import json
import time
from datetime import date
from typing import Any

from redis.exceptions import RedisError

from bot.core import logger
from bot.services.cache.client import redis
from bot.services.cache.constants import SCHEDULE_STORAGE_TTL_SECONDS
from bot.services.cache.keys import schedule_week_key
from bot.services.cache.schemas import CachedWeek


async def get_week(monday: date) -> CachedWeek | None:
    """Кеш тижня або None (немає запису чи Redis недоступний — для бота це те саме)."""
    try:
        raw = await redis.get(schedule_week_key(monday))
        if raw:
            entry = json.loads(raw)
            return CachedWeek(fetched_at=float(entry["fetched_at"]), payload=entry["payload"])
    except (RedisError, ValueError, KeyError) as exc:
        logger.warning("Cannot read schedule cache for week %s: %s", monday, exc)
    return None


async def set_week(monday: date, payload: Any) -> None:
    entry = json.dumps({"fetched_at": time.time(), "payload": payload})
    try:
        await redis.set(schedule_week_key(monday), entry, ex=SCHEDULE_STORAGE_TTL_SECONDS)
    except RedisError as exc:
        logger.warning("Cannot write schedule cache for week %s: %s", monday, exc)
