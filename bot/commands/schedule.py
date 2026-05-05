from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import SEMESTER_START_DATE
from bot.services import holiday_service, schedule_service
from bot.utils import format_day_schedule, format_week_schedule

router = Router(name=__name__)


@router.message(Command("today"))
async def today_command(message: Message, i18n: I18nContext, session: AsyncSession) -> None:
    if datetime.now() < SEMESTER_START_DATE:
        await message.answer(i18n.get("semester-not-started"))
        return

    day, lessons, date = await schedule_service.get_today_schedule(session)

    if not lessons:
        await message.answer(i18n.get("no-lessons-today"))
        return

    await holiday_service.ensure_loaded(date.year)
    holiday = holiday_service.get_name(date.date())
    await message.answer(format_day_schedule(i18n, day, lessons, date, holiday))


@router.message(Command("tomorrow"))
async def tomorrow_command(message: Message, i18n: I18nContext, session: AsyncSession) -> None:
    if datetime.now() + timedelta(days=1) < SEMESTER_START_DATE:
        await message.answer(i18n.get("semester-not-started"))
        return

    day, lessons, date = await schedule_service.get_tomorrow_schedule(session)

    if not lessons:
        await message.answer(i18n.get("no-lessons-tomorrow"))
        return

    await holiday_service.ensure_loaded(date.year)
    holiday = holiday_service.get_name(date.date())
    await message.answer(format_day_schedule(i18n, day, lessons, date, holiday))


@router.message(Command("week"))
async def week_command(message: Message, i18n: I18nContext, session: AsyncSession) -> None:
    if datetime.now() < SEMESTER_START_DATE:
        await message.answer(i18n.get("semester-not-started"))
        return

    week_schedule = await schedule_service.get_week_schedule(session)
    if week_schedule:
        sample_date = next(iter(week_schedule.values()))[1]
        await holiday_service.ensure_loaded(sample_date.year)
    holiday_names: dict[datetime, str] = {
        dt: name for _, (_, dt) in week_schedule.items() if (name := holiday_service.get_name(dt.date()))
    }
    await message.answer(format_week_schedule(i18n, week_schedule, holiday_names))
