import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter, TelegramServerError
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.scheduler.constants import DAILY_SCHEDULE_ATTEMPTS, DAILY_SCHEDULE_RETRY_SECONDS
from bot.services.schedule import PortalError, get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule

TRANSIENT_ERRORS = (PortalError, TelegramNetworkError, TelegramRetryAfter, TelegramServerError)


async def send_daily_schedule(bot: Bot, i18n: I18nContext, chat_id: int) -> None:
    today = now()
    for attempt in range(1, DAILY_SCHEDULE_ATTEMPTS + 1):
        try:
            lessons = await get_day(today.date())
            if lessons:
                await bot.send_message(chat_id, format_day_schedule(i18n, lessons, today))
            return
        except TRANSIENT_ERRORS as exc:
            if attempt == DAILY_SCHEDULE_ATTEMPTS:
                raise
            logger.warning("Daily schedule attempt %d/%d failed: %s", attempt, DAILY_SCHEDULE_ATTEMPTS, exc)
            await asyncio.sleep(DAILY_SCHEDULE_RETRY_SECONDS)
