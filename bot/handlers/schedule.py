from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from bot.core import config
from bot.keyboards import get_back_keyboard
from bot.services.schedule import schedule_service
from bot.utils import format_day_schedule, format_week_schedule

router = Router(name=__name__)


@router.callback_query(F.data == "schedule_today")
async def schedule_today_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    if datetime.now() < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    day, lessons, date = schedule_service.get_today_schedule()

    if not lessons:
        await callback.answer(i18n.get("alert-no-lessons-today"), show_alert=True)
        return

    await callback.message.edit_text(
        format_day_schedule(i18n, day, lessons, date),
        reply_markup=get_back_keyboard(i18n)
    )
    await callback.answer()


@router.callback_query(F.data == "schedule_tomorrow")
async def schedule_tomorrow_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    if datetime.now() + timedelta(days=1) < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    day, lessons, date = schedule_service.get_tomorrow_schedule()

    if not lessons:
        await callback.answer(i18n.get("alert-no-lessons-tomorrow"), show_alert=True)
        return

    await callback.message.edit_text(
        format_day_schedule(i18n, day, lessons, date),
        reply_markup=get_back_keyboard(i18n)
    )
    await callback.answer()


@router.callback_query(F.data == "schedule_week")
async def schedule_week_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    if datetime.now() < config.SEMESTER_START_DATE:
        await callback.answer(i18n.get("alert-semester-not-started"), show_alert=True)
        return

    week_schedule = schedule_service.get_week_schedule()
    await callback.message.edit_text(
        format_week_schedule(i18n, week_schedule),
        reply_markup=get_back_keyboard(i18n)
    )
    await callback.answer()
