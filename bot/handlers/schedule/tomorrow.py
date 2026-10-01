from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.services.schedule import get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule

from .views import ScheduleView, answer_callback, answer_message

router = Router(name=__name__)


async def build_tomorrow(i18n: I18nContext) -> ScheduleView:
    tomorrow = now() + timedelta(days=1)
    lessons = await get_day(tomorrow.date())
    if not lessons:
        return ScheduleView(notice="no-lessons-tomorrow")
    return ScheduleView(text=format_day_schedule(i18n, lessons, tomorrow))


@router.message(Command("tomorrow"))
async def tomorrow_command(message: Message, i18n: I18nContext) -> None:
    await answer_message(message, i18n, await build_tomorrow(i18n))


@router.callback_query(F.data == "schedule_tomorrow")
async def tomorrow_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    await answer_callback(callback, i18n, await build_tomorrow(i18n))
