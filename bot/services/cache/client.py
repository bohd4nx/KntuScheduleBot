from redis import exceptions as redis_errors
from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff

from bot.core import settings

from .constants import REDIS_RETRIES, REDIS_TIMEOUT_SECONDS

redis: Redis = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=REDIS_TIMEOUT_SECONDS,
    socket_connect_timeout=REDIS_TIMEOUT_SECONDS,
    # Після рестарту Redis у пулі лишаються мертві з'єднання: без повтору перший запит падає повз кеш.
    retry=Retry(ExponentialBackoff(cap=1, base=0.1), REDIS_RETRIES),
    retry_on_error=[redis_errors.ConnectionError],
)


async def close() -> None:
    await redis.aclose()
