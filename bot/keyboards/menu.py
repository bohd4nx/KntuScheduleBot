from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext


def get_main_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=i18n.get("btn-today"), callback_data="schedule_today"),
            InlineKeyboardButton(text=i18n.get("btn-tomorrow"), callback_data="schedule_tomorrow"),
        ],
        [
            InlineKeyboardButton(text=i18n.get("btn-week"), callback_data="schedule_week"),
        ],

    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(i18n: I18nContext, target: str = "back_to_menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i18n.get("btn-back"), callback_data=target)]
    ])
