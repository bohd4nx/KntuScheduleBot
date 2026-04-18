from html import escape

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.core import config
from bot.keyboards import get_main_menu_keyboard

router = Router(name=__name__)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    if not isinstance(callback.message, Message):
        return
    name = escape(callback.from_user.full_name or callback.from_user.first_name or "User")

    await callback.message.edit_text(
        i18n.get(
            "start",
            name=name,
            semester_start=config.SEMESTER_START_DATE,
            semester_end=config.SEMESTER_END_DATE,
        ),
        reply_markup=get_main_menu_keyboard(i18n),
    )
    await callback.answer()
