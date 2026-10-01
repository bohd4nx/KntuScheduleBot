import time
from urllib.parse import urlparse

from curl_cffi.requests import AsyncSession, RequestsError, Response

from bot.core import config, logger
from bot.services import cache

from ..constants import (
    ACCESS_COOKIE,
    ACCESS_EXPIRY_MARGIN_SECONDS,
    ACCESS_FALLBACK_TTL_SECONDS,
    BASE_URL,
    CONNECT_TIMEOUT_SECONDS,
    REFRESH_COOKIE,
    REQUEST_TIMEOUT_SECONDS,
)
from ..exceptions import PortalError
from .jwt import jwt_expiry
from .state import state


def access_is_fresh() -> bool:
    return time.time() < state.access_expires_at - ACCESS_EXPIRY_MARGIN_SECONDS


async def refresh_session(session: AsyncSession[Response], *, force: bool = False) -> None:
    """Оновлює сесію порталу. Портал ротує refresh-токен, тому новий одразу йде в Redis."""
    async with state.refresh_lock:
        # Поки чекали на lock, сесію міг оновити інший запит.
        if not force and access_is_fresh():
            return

        if not state.refresh_cookie_loaded:
            token = await cache.token.load_refresh_token(seed=config.PORTAL_REFRESH_TOKEN)
            session.cookies.set(REFRESH_COOKIE, token, domain=urlparse(BASE_URL).hostname or "", path="/")
            state.refresh_cookie_loaded = True

        try:
            response = await session.post(
                f"{BASE_URL}/auth/refresh", timeout=(CONNECT_TIMEOUT_SECONDS, REQUEST_TIMEOUT_SECONDS)
            )
        except RequestsError as exc:
            raise PortalError(str(exc) or "refresh request failed") from exc

        access, refresh = response.cookies.get(ACCESS_COOKIE), response.cookies.get(REFRESH_COOKIE)
        if response.status_code >= 400 or not access or not refresh:
            raise PortalError(f"HTTP {response.status_code} for POST auth/refresh", status_code=response.status_code)

        state.access_expires_at = jwt_expiry(access) or time.time() + ACCESS_FALLBACK_TTL_SECONDS
        await cache.token.save_refresh_token(config.PORTAL_REFRESH_TOKEN, refresh)
        logger.info("Portal session refreshed")


async def ensure_access(session: AsyncSession[Response]) -> None:
    if not access_is_fresh():
        await refresh_session(session)
