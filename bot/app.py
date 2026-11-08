from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from bot.core import DEFAULT_LOCALE, LOCALES_PATH, settings
from bot.handlers import commands, errors, menu, schedule
from bot.lifecycle import on_shutdown, on_startup
from bot.scheduler import build_scheduler


def create_bot() -> Bot:
    return Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )


async def build_dispatcher(bot: Bot) -> Dispatcher:
    i18n_core = FluentCompileCore(path=LOCALES_PATH)
    await i18n_core.startup()

    dp = Dispatcher()
    dp.include_routers(errors.router, commands.router, menu.router, schedule.router)
    i18n = I18nMiddleware(core=i18n_core, default_locale=DEFAULT_LOCALE)
    i18n.setup(dispatcher=dp)

    dp["scheduler"] = build_scheduler(bot, i18n)
    dp["i18n_core"] = i18n_core
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


async def run() -> None:
    bot = create_bot()
    dp = await build_dispatcher(bot)
    await dp.start_polling(bot, close_bot_session=True)
