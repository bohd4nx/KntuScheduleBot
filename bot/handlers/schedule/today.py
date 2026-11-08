from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.keyboards import MainMenuCallback
from bot.services.schedule import get_day
from bot.utils.dates import now
from bot.utils.formatters import format_day_schedule

from .schemas import ScheduleView
from .views import answer_callback, answer_message

router = Router(name=__name__)


async def build_today(i18n: I18nContext) -> ScheduleView:
    today = now()
    lessons = await get_day(today.date())
    if not lessons:
        return ScheduleView(notice="no-lessons-today")
    return ScheduleView(text=format_day_schedule(i18n, lessons, today))


@router.message(Command("today"))
async def today_command(message: Message, i18n: I18nContext) -> None:
    await answer_message(message, i18n, await build_today(i18n))


@router.callback_query(F.data == MainMenuCallback.SCHEDULE_TODAY)
async def today_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    await answer_callback(callback, i18n, await build_today(i18n))
