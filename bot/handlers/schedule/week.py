from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.services.schedule import get_week
from bot.utils.constants import WORK_DAYS
from bot.utils.dates import get_week_monday
from bot.utils.formatters import format_week_schedule

from .views import ScheduleView, answer_callback, answer_message

router = Router(name=__name__)


async def build_week(i18n: I18nContext) -> ScheduleView:
    week = await get_week(get_week_monday().date())
    working_days = {day: lessons for day, lessons in week.items() if day.weekday() < len(WORK_DAYS)}
    if not working_days:
        return ScheduleView(notice="no-lessons-week")
    return ScheduleView(text=format_week_schedule(i18n, working_days))


@router.message(Command("week"))
async def week_command(message: Message, i18n: I18nContext) -> None:
    await answer_message(message, i18n, await build_week(i18n))


@router.callback_query(F.data == "schedule_week")
async def week_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    await answer_callback(callback, i18n, await build_week(i18n))
