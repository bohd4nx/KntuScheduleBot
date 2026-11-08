from redis.asyncio import Redis

from bot.core import settings

from .constants import REDIS_TIMEOUT_SECONDS

redis: Redis = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=REDIS_TIMEOUT_SECONDS,
    socket_connect_timeout=REDIS_TIMEOUT_SECONDS,
)


async def close() -> None:
    await redis.aclose()
