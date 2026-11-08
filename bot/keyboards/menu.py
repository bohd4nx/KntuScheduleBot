from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from .callbacks import MainMenuCallback


def get_main_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=i18n.get("btn-today"),
                icon_custom_emoji_id="5226513232549664618",
                callback_data=MainMenuCallback.SCHEDULE_TODAY,
            ),
            InlineKeyboardButton(
                text=i18n.get("btn-tomorrow"),
                icon_custom_emoji_id="5226513232549664618",
                callback_data=MainMenuCallback.SCHEDULE_TOMORROW,
            ),
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("btn-week"),
                icon_custom_emoji_id="5258105663359294787",
                callback_data=MainMenuCallback.SCHEDULE_WEEK,
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("btn-back"),
                    icon_custom_emoji_id="5960671702059848143",
                    callback_data=MainMenuCallback.BACK_TO_MENU,
                )
            ]
        ]
    )
