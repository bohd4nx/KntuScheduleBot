from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import config
from bot.keyboards import get_main_menu_keyboard
from bot.utils import escape_html

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    user = message.from_user
    name = escape_html(user.full_name or user.first_name)

    await message.answer(
        i18n.get("start", name=name,
                 semester_start=config.SEMESTER_START_DATE,
                 semester_end=config.SEMESTER_END_DATE),
        reply_markup=get_main_menu_keyboard(i18n),
    )
