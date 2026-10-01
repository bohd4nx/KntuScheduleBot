import json

from redis.exceptions import RedisError

from bot.core import logger

from ..client import PORTAL_REFRESH_TOKEN, redis


async def load_refresh_token(seed: str) -> str:
    """Збережений refresh-токен або `seed` із оточення.

    Стан чинний лише для того ж `seed`: якщо токен в оточенні замінили вручну, беремо його.
    """
    try:
        raw = await redis.get(PORTAL_REFRESH_TOKEN)
        if raw:
            state = json.loads(raw)
            if state["seed"] == seed:
                return str(state["refresh"])
    except (RedisError, ValueError, KeyError) as exc:
        logger.warning("Cannot load portal refresh token from cache, using the configured one: %s", exc)
    return seed


async def save_refresh_token(seed: str, refresh: str) -> None:
    try:
        await redis.set(PORTAL_REFRESH_TOKEN, json.dumps({"seed": seed, "refresh": refresh}))
    except RedisError as exc:
        # Сесія жива й у пам'яті; без запису бот лише не переживе рестарт.
        logger.error("Cannot persist portal refresh token: %s", exc)
