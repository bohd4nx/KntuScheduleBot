from dataclasses import dataclass

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.keyboards import get_back_keyboard


@dataclass(frozen=True, slots=True)
class ScheduleView:
    """Результат запиту: готовий `text` або ключ локалі `notice` (алерт — `alert-<notice>`), чому показати нічого."""

    text: str | None = None
    notice: str | None = None


async def answer_message(message: Message, i18n: I18nContext, view: ScheduleView) -> None:
    await message.answer(view.text or i18n.get(view.notice or "schedule-unavailable"))


async def answer_callback(callback: CallbackQuery, i18n: I18nContext, view: ScheduleView) -> None:
    if not isinstance(callback.message, Message):
        return
    # Немає що показати — короткий алерт замість редагування повідомлення.
    if view.text is None:
        await callback.answer(i18n.get(f"alert-{view.notice or 'schedule-unavailable'}"), show_alert=True)
        return
    await callback.message.edit_text(view.text, reply_markup=get_back_keyboard(i18n))
    await callback.answer()
