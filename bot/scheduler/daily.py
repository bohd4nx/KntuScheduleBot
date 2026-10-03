import asyncio
from datetime import date, datetime, time, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram_i18n import I18nContext, I18nMiddleware

from bot.core import config, logger
from bot.services.schedule import PortalError, get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule

from .constants import DIGEST_TIME, MAX_SLEEP_SECONDS, SATURDAY


def _next_run() -> datetime:
    """Найближчі 6:00 за Києвом у будній день."""
    current = now()
    day = current.date()
    if datetime.combine(day, DIGEST_TIME) <= current:
        day += timedelta(days=1)
    while day.weekday() >= SATURDAY:
        day += timedelta(days=1)
    return datetime.combine(day, DIGEST_TIME)


async def _sleep_until(moment: datetime) -> None:
    while (left := (moment - now()).total_seconds()) > 0:
        await asyncio.sleep(min(left, MAX_SLEEP_SECONDS))


async def _send_schedule(bot: Bot, i18n: I18nContext, chat_id: int, day: date) -> None:
    lessons = await get_day(day)
    if lessons:
        await bot.send_message(chat_id, format_day_schedule(i18n, lessons, datetime.combine(day, time())))


async def _digest_loop(bot: Bot, i18n: I18nContext, chat_id: int) -> None:
    while True:
        run = _next_run()
        await _sleep_until(run)
        try:
            await _send_schedule(bot, i18n, chat_id, run.date())
        except (PortalError, TelegramAPIError) as exc:
            logger.error("Daily schedule was not sent: %s", exc)


_task: asyncio.Task[None] | None = None


def start_daily_digest(bot: Bot, i18n: I18nMiddleware) -> None:
    """Щоденна розсилка в `GROUP_ID`; без нього нічого не запускає."""
    global _task
    if config.GROUP_ID is None:
        return
    # Поза хендлерами i18n-контексту немає — збираємо власний із дефолтною локаллю.
    context = I18nContext(locale=config.DEFAULT_LOCALE, core=i18n.core, manager=i18n.manager, data={})
    _task = asyncio.create_task(_digest_loop(bot, context, config.GROUP_ID))


def stop_daily_digest() -> None:
    if _task:
        _task.cancel()
