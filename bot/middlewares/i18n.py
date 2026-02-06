from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext | None = data.get("i18n")

        if i18n:
            await i18n.set_locale("uk")

        return await handler(event, data)


__all__ = ["LocaleMiddleware"]
