import asyncio
from datetime import datetime, time, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram_i18n import I18nContext

from bot.core import config, logger
from bot.services.schedule import PortalError, get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule

DIGEST_TIME = time(6, 0)
# Спимо шматками: «київська» доба може мати 23/25 годин, тож залишок щоразу рахуємо заново.
MAX_SLEEP_SECONDS = 10 * 60


def _next_run() -> datetime:
    current = now()
    run = datetime.combine(current.date(), DIGEST_TIME)
    return run if run > current else run + timedelta(days=1)


async def _send_today(bot: Bot, i18n: I18nContext, chat_id: int) -> None:
    today = now()
    lessons = await get_day(today.date())
    if not lessons:
        return
    await bot.send_message(chat_id, format_day_schedule(i18n, lessons, today))


async def _digest_loop(bot: Bot, i18n: I18nContext, chat_id: int) -> None:
    while True:
        run = _next_run()
        while (left := (run - now()).total_seconds()) > 0:
            await asyncio.sleep(min(left, MAX_SLEEP_SECONDS))

        if now().weekday() >= 5:  # на вихідних розклад не надсилаємо
            continue
        try:
            await _send_today(bot, i18n, chat_id)
        except (PortalError, TelegramAPIError) as exc:
            logger.error("Daily schedule was not sent: %s", exc)


def start_digest(bot: Bot, i18n: I18nContext) -> asyncio.Task[None] | None:
    """Щоденна розсилка в `GROUP_ID`; без нього нічого не запускає."""
    if config.GROUP_ID is None:
        return None
    return asyncio.create_task(_digest_loop(bot, i18n, config.GROUP_ID))
