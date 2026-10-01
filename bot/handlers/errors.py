from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.services.schedule import PortalError

router = Router(name=__name__)


@router.errors(ExceptionTypeFilter(PortalError))
async def portal_error(event: ErrorEvent, i18n: I18nContext) -> None:
    """Збій порталу не валить бота: користувач отримує коротке повідомлення."""
    logger.error("Schedule fetch failed: %s", event.exception)
    update = event.update
    if update.callback_query:
        await update.callback_query.answer(i18n.get("alert-schedule-unavailable"), show_alert=True)
    elif update.message:
        await update.message.answer(i18n.get("schedule-unavailable"))
