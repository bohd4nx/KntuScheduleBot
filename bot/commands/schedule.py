from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import config
from bot.services.schedule import schedule_service
from bot.utils import format_day_schedule, format_week_schedule

router = Router(name=__name__)


@router.message(Command("today"))
async def today_command(message: Message, i18n: I18nContext) -> None:
    if datetime.now() < config.SEMESTER_START_DATE:
        await message.answer(i18n.get("alert-semester-not-started"))
        return

    day, lessons, date = schedule_service.get_today_schedule()

    if not lessons:
        await message.answer(i18n.get("alert-no-lessons-today"))
        return

    await message.answer(format_day_schedule(i18n, day, lessons, date))


@router.message(Command("tomorrow"))
async def tomorrow_command(message: Message, i18n: I18nContext) -> None:
    if datetime.now() < config.SEMESTER_START_DATE:
        await message.answer(i18n.get("alert-semester-not-started"))
        return

    day, lessons, date = schedule_service.get_tomorrow_schedule()

    if not lessons:
        await message.answer(i18n.get("alert-no-lessons-tomorrow"))
        return

    await message.answer(format_day_schedule(i18n, day, lessons, date))


@router.message(Command("week"))
async def week_command(message: Message, i18n: I18nContext) -> None:
    if datetime.now() < config.SEMESTER_START_DATE:
        await message.answer(i18n.get("alert-semester-not-started"))
        return

    week_schedule = schedule_service.get_week_schedule()
    await message.answer(format_week_schedule(i18n, week_schedule))
