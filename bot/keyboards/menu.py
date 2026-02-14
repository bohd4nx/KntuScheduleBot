from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext


def get_main_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=i18n.get("btn-today"),
                icon_custom_emoji_id="5258226313285607065",
                callback_data="schedule_today",
            ),
            InlineKeyboardButton(
                text=i18n.get("btn-tomorrow"),
                icon_custom_emoji_id="5253959125838090076",
                callback_data="schedule_tomorrow",
            ),
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("btn-week"),
                icon_custom_emoji_id="5258123337149717894",
                style=ButtonStyle.PRIMARY,
                callback_data="schedule_week",
            ),
        ],

    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(i18n: I18nContext, target: str = "back_to_menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=i18n.get("btn-back"),
                icon_custom_emoji_id="5257963315258204021",
                style=ButtonStyle.DANGER,
                callback_data=target,
            )
        ]
    ])
