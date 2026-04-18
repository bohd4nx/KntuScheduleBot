import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from bot.commands import help_router, schedule_router, start_router
from bot.core import DEFAULT_LOCALE, config, logger, setup_logging
from bot.handlers import menu, schedule


async def _setup_bot_info(bot: Bot) -> None:
    commands: list[BotCommand] = [
        BotCommand(command="start", description="🏠 Головне меню"),
        BotCommand(command="today", description="🗓️  Розклад на сьогодні"),
        BotCommand(command="tomorrow", description="🗓️  Розклад на завтра"),
        BotCommand(command="week", description="🗓️  Розклад на тиждень"),
        BotCommand(command="help", description="❓ Як користуватися"),
    ]
    await bot.set_my_commands(commands)

    await bot.set_my_name("ЦНТУ | Розклад занять")

    await bot.set_my_description(
        "📅 Актуальний розклад занять для студентів кафедри кібербезпеки та програмного забезпечення ЦНТУ.\n\n"
        "• Розклад на сьогодні, завтра або весь тиждень\n"
        "• Автоматичне визначення типу тижня (чисельник / знаменник)\n"
        "• Посилання на онлайн-заняття прямо в повідомленні"
    )

    await bot.set_my_short_description("Розклад занять для кафедри кібербезпеки та програмного забезпечення ЦНТУ")


async def main() -> None:
    setup_logging()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )

    await _setup_bot_info(bot)

    i18n_core = FluentCompileCore(path="locales/{locale}")
    await i18n_core.startup()
    i18n = I18nMiddleware(core=i18n_core, default_locale=DEFAULT_LOCALE)

    dp = Dispatcher()

    for router in [
        start_router,
        help_router,
        schedule_router,
        menu.router,
        schedule.router,
    ]:
        dp.include_router(router)

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
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
