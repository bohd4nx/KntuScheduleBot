import asyncio
from typing import Any

from curl_cffi.requests import AsyncSession, RequestsError, Response

from bot.core import logger
from bot.utils.http import backoff, read_json, retry_delay

from . import auth
from .constants import (
    BASE_URL,
    CONNECT_TIMEOUT_SECONDS,
    MAX_ATTEMPTS,
    MAX_RETRY_WAIT_SECONDS,
    PORTAL_MAX_CONNECTIONS,
    REQUEST_TIMEOUT_SECONDS,
    RETRYABLE_STATUS_CODES,
)
from .exceptions import PortalError

TIMEOUT = (CONNECT_TIMEOUT_SECONDS, REQUEST_TIMEOUT_SECONDS)

session: AsyncSession[Response] = AsyncSession(max_clients=PORTAL_MAX_CONNECTIONS, impersonate="chrome")


def start_keepalive() -> None:
    auth.start_keepalive(session)


async def close() -> None:
    auth.stop_keepalive()
    await session.close()


async def get_json(path: str, *, params: dict[str, Any] | None = None) -> Any:
    """GET до API порталу: 401 → оновлення сесії, мережеві збої та 429/5xx → повтор із паузою."""
    await auth.ensure_access(session)

    reauthenticated = False
    for attempt in range(1, MAX_ATTEMPTS + 1):
        is_last = attempt == MAX_ATTEMPTS

        try:
            response = await session.get(f"{BASE_URL}/{path}", params=params, timeout=TIMEOUT)
        except RequestsError as exc:
            if is_last:
                raise PortalError(str(exc) or "request failed") from exc
            logger.warning("Portal GET %s failed (attempt %d/%d): %s", path, attempt, MAX_ATTEMPTS, exc)
            await asyncio.sleep(backoff(attempt, max_wait=MAX_RETRY_WAIT_SECONDS))
            continue

        status = response.status_code

        # Портал може скасувати сесію раніше за `exp` токена.
        if status == 401 and not reauthenticated:
            reauthenticated = True
            await auth.refresh_session(session, force=True)
            continue

        if status in RETRYABLE_STATUS_CODES and not is_last:
            await asyncio.sleep(retry_delay(response, attempt, max_wait=MAX_RETRY_WAIT_SECONDS))
            continue

        if status != 200:
            raise PortalError(f"HTTP {status} for GET {path}", status_code=status)
        try:
            return read_json(response)
        except ValueError as exc:
            raise PortalError(f"Response of GET {path} is not valid JSON") from exc

    raise PortalError("request retries exhausted")  # цикл завжди повертає або кидає
