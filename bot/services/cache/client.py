from datetime import date

from redis.asyncio import Redis

from bot.core import config

from .constants import KEY_PREFIX, REDIS_TIMEOUT_SECONDS

redis: Redis = Redis.from_url(
    config.REDIS_URL,
    decode_responses=True,
    socket_timeout=REDIS_TIMEOUT_SECONDS,
    socket_connect_timeout=REDIS_TIMEOUT_SECONDS,
)

# Ключі кешу
PORTAL_REFRESH_TOKEN = f"{KEY_PREFIX}:portal:refresh_token"


def schedule_week(monday: date) -> str:
    """Відповідь порталу за тиждень, що починається в `monday`."""
    return f"{KEY_PREFIX}:schedule:week:{monday.isoformat()}"


async def close() -> None:
    await redis.aclose()
