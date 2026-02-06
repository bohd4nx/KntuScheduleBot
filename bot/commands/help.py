from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

router = Router(name=__name__)


@router.message(Command("help"))
async def help_command(message: Message, i18n: I18nContext) -> None:
    await message.answer(
        i18n.get("how-to-use")
    )


@router.callback_query(F.data == "how_to_use")
async def how_to_use_callback(callback: CallbackQuery, i18n: I18nContext) -> None:
    await callback.message.edit_text(
        i18n.get("how-to-use")
    )
    await callback.answer()
