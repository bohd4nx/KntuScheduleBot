from html import escape

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.keyboards import MainMenuCallback, get_main_menu_keyboard

router = Router(name=__name__)


@router.callback_query(F.data == MainMenuCallback.BACK_TO_MENU)
async def back_to_menu_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return
    name = escape(callback.from_user.full_name or callback.from_user.first_name or "User")

    await callback.message.edit_text(
        i18n.get(
            "start",
            name=name,
        ),
        reply_markup=get_main_menu_keyboard(i18n),
    )
    await callback.answer()
