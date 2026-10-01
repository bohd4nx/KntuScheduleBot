from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.keyboards import get_main_menu_keyboard
from bot.utils.formatters import quote_html

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    user = message.from_user
    name = quote_html(user.full_name or user.first_name or "User") if user else "User"

    await message.answer(
        i18n.get(
            "start",
            name=name,
        ),
        reply_markup=get_main_menu_keyboard(i18n),
    )
