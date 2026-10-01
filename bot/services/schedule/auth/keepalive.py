import asyncio

from curl_cffi.requests import AsyncSession, Response

from bot.core import logger

from ..constants import KEEPALIVE_INTERVAL_SECONDS
from ..exceptions import PortalError
from .refresh import refresh_session
from .state import state


async def _keepalive(session: AsyncSession[Response]) -> None:
    while True:
        try:
            await refresh_session(session, force=True)
        except PortalError as exc:
            if exc.is_auth_error:
                logger.error("Portal refresh token rejected — set a new PORTAL_REFRESH_TOKEN")
            else:
                logger.warning("Portal keepalive failed: %s", exc)
        await asyncio.sleep(KEEPALIVE_INTERVAL_SECONDS)


def start_keepalive(session: AsyncSession[Response]) -> None:
    """Одразу перевіряє токен і далі тримає refresh живим у фоні."""
    state.keepalive_task = asyncio.create_task(_keepalive(session))


def stop_keepalive() -> None:
    if state.keepalive_task:
        state.keepalive_task.cancel()
