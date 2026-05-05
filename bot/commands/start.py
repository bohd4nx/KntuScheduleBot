from html import escape

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core.constants import SEMESTER_END_DATE, SEMESTER_START_DATE
from bot.keyboards import get_main_menu_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    user = message.from_user
    name = escape(user.full_name or user.first_name or "User") if user else "User"

    await message.answer(
        i18n.get(
            "start",
            name=name,
            semester_start=SEMESTER_START_DATE,
            semester_end=SEMESTER_END_DATE,
        ),
        reply_markup=get_main_menu_keyboard(i18n),
    )
