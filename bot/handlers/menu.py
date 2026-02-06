from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from bot.core import config
from bot.keyboards import get_main_menu_keyboard
from bot.utils import escape_html

router = Router(name=__name__)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    user = callback.from_user
    name = escape_html(user.full_name or user.first_name)

    await callback.message.edit_text(
        i18n.get("start", name=name,
                 semester_start=config.SEMESTER_START_DATE,
                 semester_end=config.SEMESTER_END_DATE),
        reply_markup=get_main_menu_keyboard(i18n)
    )
    await callback.answer()
