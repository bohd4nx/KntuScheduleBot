import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from bot.commands import start_router, help_router, schedule_router
from bot.core import logger, setup_logging, config
from bot.handlers import menu, schedule
from bot.middlewares import LocaleMiddleware


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🏠 Головне меню"),
        BotCommand(command="today", description="🗓️  Розклад на сьогодні"),
        BotCommand(command="tomorrow", description="🗓️  Розклад на завтра"),
        BotCommand(command="week", description="🗓️  Розклад на тиждень"),
        BotCommand(command="help", description="❓ Як користуватися"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    setup_logging()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )

    await set_bot_commands(bot)

    i18n_core = FluentRuntimeCore(path="locales/{locale}")
    await i18n_core.startup()
    i18n = I18nMiddleware(core=i18n_core, default_locale="uk")

    dp = Dispatcher()

    for router in [start_router, help_router, schedule_router, menu.router, schedule.router]:
        dp.include_router(router)

    dp.update.middleware(LocaleMiddleware())
    dp.callback_query.middleware(LocaleMiddleware())
    dp.message.middleware(LocaleMiddleware())

    i18n.setup(dispatcher=dp)

    try:
        await dp.start_polling(
            bot,
            polling_timeout=30,
            handle_as_tasks=True,
            tasks_concurrency_limit=100,
            close_bot_session=True,
        )
    finally:
        await i18n.core.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
