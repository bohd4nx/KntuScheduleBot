import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import BotCommand
from aiogram_i18n import I18nContext, I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from bot.core import config, logger
from bot.handlers import commands, errors, menu, schedule
from bot.services import cache
from bot.services.digest import start_digest
from bot.services.schedule import close_schedule_client, start_keepalive

BOT_COMMANDS = [
    BotCommand(command="start", description="🏠 Головне меню"),
    BotCommand(command="today", description="🗓️  Розклад на сьогодні"),
    BotCommand(command="tomorrow", description="🗓️  Розклад на завтра"),
    BotCommand(command="week", description="🗓️  Розклад на тиждень"),
    BotCommand(command="help", description="❓ Як користуватися"),
]

BOT_NAME = "ЦНТУ | Розклад занять"
BOT_DESCRIPTION = (
    "📅 Актуальний розклад занять для студентів кафедри кібербезпеки та програмного забезпечення ЦНТУ.\n\n"
    "• Розклад на сьогодні, завтра або весь тиждень\n"
    "• Розклад береться напряму з порталу ЦНТУ та оновлюється раз на добу"
)
BOT_SHORT_DESCRIPTION = "Розклад занять для кафедри кібербезпеки та програмного забезпечення ЦНТУ"


def build_bot() -> Bot:
    return Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )


async def setup_bot_info(bot: Bot) -> None:
    """Виставляє команди й тексти профілю; Telegram жорстко лімітує їх зміну, тож пишемо лише відмінне."""
    await bot.set_my_commands(BOT_COMMANDS)
    if (await bot.get_my_name()).name != BOT_NAME:
        await bot.set_my_name(BOT_NAME)
    if (await bot.get_my_description()).description != BOT_DESCRIPTION:
        await bot.set_my_description(BOT_DESCRIPTION)
    if (await bot.get_my_short_description()).short_description != BOT_SHORT_DESCRIPTION:
        await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)


async def build_dispatcher(bot: Bot) -> Dispatcher:
    i18n_core = FluentCompileCore(path=str(config.LOCALES_DIR / "{locale}" / "LC_MESSAGES"))
    await i18n_core.startup()

    dp = Dispatcher()
    dp.include_routers(errors.router, commands.router, menu.router, schedule.router)
    i18n = I18nMiddleware(core=i18n_core, default_locale=config.DEFAULT_LOCALE)
    i18n.setup(dispatcher=dp)
    digest_task: asyncio.Task[None] | None = None

    @dp.startup()
    async def on_startup() -> None:
        try:
            await setup_bot_info(bot)
        except TelegramRetryAfter as error:
            # Профіль не критичний для роботи: бот стартує й без його оновлення.
            logger.warning("Bot profile update skipped: retry in %s s", error.retry_after)
        start_keepalive()  # фонове оновлення сесії порталу
        # Поза хендлерами i18n-контексту немає — збираємо власний із дефолтною локаллю.
        nonlocal digest_task
        digest_task = start_digest(
            bot, I18nContext(locale=config.DEFAULT_LOCALE, core=i18n.core, manager=i18n.manager, data={})
        )
        logger.info("Bot started")

    @dp.shutdown()
    async def on_shutdown() -> None:
        if digest_task:
            digest_task.cancel()
        await close_schedule_client()
        await cache.close()
        await i18n.core.shutdown()
        logger.info("Bot stopped")

    return dp


async def run() -> None:
    bot = build_bot()
    dp = await build_dispatcher(bot)
    await dp.start_polling(bot, close_bot_session=True)
