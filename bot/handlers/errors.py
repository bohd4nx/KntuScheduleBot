from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Update
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.services.schedule import PortalError

router = Router(name=__name__)

# Повторне натискання тієї ж кнопки або натискання, що чекало під час рестарту, — не збої.
HARMLESS_BAD_REQUESTS = ("message is not modified", "query is too old")


async def notify_user(update: Update, i18n: I18nContext, key: str) -> None:
    # Відповідь на старий callback теж може впасти — користувачу тоді вже нічого не показати.
    with suppress(TelegramAPIError):
        if update.callback_query:
            await update.callback_query.answer(i18n.get(f"alert-{key}"), show_alert=True)
        elif update.message:
            await update.message.answer(i18n.get(key))


@router.errors(ExceptionTypeFilter(PortalError))
async def portal_error(event: ErrorEvent, i18n: I18nContext) -> None:
    logger.error("Schedule fetch failed: %s", event.exception)
    await notify_user(event.update, i18n, "schedule-unavailable")


@router.errors(ExceptionTypeFilter(TelegramBadRequest))
async def telegram_bad_request(event: ErrorEvent, i18n: I18nContext) -> None:
    if any(text in str(event.exception) for text in HARMLESS_BAD_REQUESTS):
        if event.update.callback_query:
            with suppress(TelegramAPIError):
                await event.update.callback_query.answer()
        return
    logger.error("Telegram rejected a request", exc_info=event.exception)
    await notify_user(event.update, i18n, "unexpected-error")


@router.errors()
async def unexpected_error(event: ErrorEvent, i18n: I18nContext) -> None:
    logger.error("Unhandled error while processing an update", exc_info=event.exception)
    await notify_user(event.update, i18n, "unexpected-error")
