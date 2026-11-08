from aiogram import Bot

from .constants import BOT_COMMANDS, BOT_DESCRIPTION, BOT_NAME, BOT_SHORT_DESCRIPTION


async def setup_bot_info(bot: Bot) -> None:
    """Виставляє команди й тексти профілю; Telegram жорстко лімітує їх зміну, тож пишемо лише відмінне."""
    await bot.set_my_commands(BOT_COMMANDS)
    if (await bot.get_my_name()).name != BOT_NAME:
        await bot.set_my_name(BOT_NAME)
    if (await bot.get_my_description()).description != BOT_DESCRIPTION:
        await bot.set_my_description(BOT_DESCRIPTION)
    if (await bot.get_my_short_description()).short_description != BOT_SHORT_DESCRIPTION:
        await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)
