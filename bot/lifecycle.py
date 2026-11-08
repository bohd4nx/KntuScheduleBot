from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram_i18n.cores import BaseCore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.core import logger, setup_bot_info
from bot.services import cache
from bot.services.schedule import close_schedule_client, start_keepalive


async def on_startup(bot: Bot, scheduler: AsyncIOScheduler) -> None:
    try:
        await setup_bot_info(bot)
    except TelegramRetryAfter as error:
        # Профіль не критичний для роботи: бот стартує й без його оновлення.
        logger.warning("Bot profile update skipped: retry in %s s", error.retry_after)
    start_keepalive()
    scheduler.start()
    logger.info("Bot started")


async def on_shutdown(scheduler: AsyncIOScheduler, i18n_core: BaseCore[object]) -> None:
    scheduler.shutdown()
    await close_schedule_client()
    await cache.close()
    await i18n_core.shutdown()
    logger.info("Bot stopped")
