from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import config
from bot.keyboards import get_back_keyboard
from bot.services.holidays import holiday_service
from bot.services.schedule import schedule_service
from bot.utils import format_day_schedule, format_week_schedule

router = Router(name=__name__)


@router.callback_query(F.data == "schedule_today")
async def schedule_today_callback(callback: CallbackQuery, i18n: I18nContext, session: AsyncSession) -> None:
    if not isinstance(callback.message, Message):
        return
    if datetime.now() < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    day, lessons, date = await schedule_service.get_today_schedule(session)

    if not lessons:
        await callback.answer(i18n.get("alert-no-lessons-today"), show_alert=True)
        return

    await holiday_service.ensure_loaded(date.year)
    holiday = holiday_service.get_name(date.date())
    await callback.message.edit_text(
        format_day_schedule(i18n, day, lessons, date, holiday),
        reply_markup=get_back_keyboard(i18n),
    )
    await callback.answer()


@router.callback_query(F.data == "schedule_tomorrow")
async def schedule_tomorrow_callback(callback: CallbackQuery, i18n: I18nContext, session: AsyncSession) -> None:
    if not isinstance(callback.message, Message):
        return
    if datetime.now() + timedelta(days=1) < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    day, lessons, date = await schedule_service.get_tomorrow_schedule(session)

    if not lessons:
        await callback.answer(i18n.get("alert-no-lessons-tomorrow"), show_alert=True)
        return

    await holiday_service.ensure_loaded(date.year)
    holiday = holiday_service.get_name(date.date())
    await callback.message.edit_text(
        format_day_schedule(i18n, day, lessons, date, holiday),
        reply_markup=get_back_keyboard(i18n),
    )
    await callback.answer()


@router.callback_query(F.data == "schedule_week")
async def schedule_week_callback(callback: CallbackQuery, i18n: I18nContext, session: AsyncSession) -> None:
    if not isinstance(callback.message, Message):
        return
    if datetime.now() < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    week_schedule = await schedule_service.get_week_schedule(session)
    if week_schedule:
        sample_date = next(iter(week_schedule.values()))[1]
        await holiday_service.ensure_loaded(sample_date.year)
    holiday_names: dict[datetime, str] = {
        dt: name for _, (_, dt) in week_schedule.items() if (name := holiday_service.get_name(dt.date()))
    }
    await callback.message.edit_text(
        format_week_schedule(i18n, week_schedule, holiday_names),
        reply_markup=get_back_keyboard(i18n),
    )
    await callback.answer()
