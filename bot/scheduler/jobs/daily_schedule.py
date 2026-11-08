from aiogram import Bot
from aiogram_i18n import I18nContext

from bot.services.schedule import get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule


async def send_daily_schedule(bot: Bot, i18n: I18nContext, chat_id: int) -> None:
    today = now()
    lessons = await get_day(today.date())
    if lessons:
        await bot.send_message(chat_id, format_day_schedule(i18n, lessons, today))
