from pathlib import Path

from aiogram.types import BotCommand

ROOT_PATH: Path = Path(__file__).resolve().parents[2]
LOCALES_PATH: str = str(ROOT_PATH / "locales" / "{locale}" / "LC_MESSAGES")
DEFAULT_LOCALE: str = "uk"

# Необов'язковий і не в git: посилання на онлайн-заняття (формат — links.example.json).
LINKS_PATH: Path = ROOT_PATH / "links.json"

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
