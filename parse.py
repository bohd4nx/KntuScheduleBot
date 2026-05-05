"""
Парсер розкладу ЦНТУ (інтерфейс командного рядка).

Використання:
    python parse.py              # зберегти всі групи у БД
    python parse.py --list       # вивести список доступних груп
    python parse.py --group КН-25  # зберегти одну групу у БД
"""

import argparse
import asyncio
import sys
from typing import Any

from bot.database import init_db
from bot.database.base import SessionLocal
from bot.database.crud import upsert_group
from bot.services import run_parser


async def _save_to_db(schedules: dict[str, Any], group: str | None) -> None:
    await init_db()
    targets = {group: schedules[group]} if group else schedules
    async with SessionLocal() as session:
        for name, data in targets.items():
            await upsert_group(session, name, data.get("course", ""), data["schedule"])
            print(f"  DB: saved {name}")
    print(f"Saved {len(targets)} group(s) to DB.")


def main() -> None:
    parser = argparse.ArgumentParser(description="KNTU schedule parser")
    parser.add_argument("--group", metavar="NAME", help="Group name to save (e.g. 'КН-25')")
    parser.add_argument("--list", action="store_true", help="List all available groups")
    args = parser.parse_args()

    print("Downloading schedule...")
    schedules = run_parser()
    print(f"Found {len(schedules)} groups")

    if args.list:
        for name in sorted(schedules):
            print(f"  {name} — {schedules[name].get('course', '?')}")
        return

    group: str | None = args.group.strip() if args.group else None

    if group and group not in schedules:
        print(f"Group '{args.group}' not found. Run --list to see available groups.", file=sys.stderr)
        sys.exit(1)

    asyncio.run(_save_to_db(schedules, group))


if __name__ == "__main__":
    main()
