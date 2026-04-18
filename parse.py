"""
Парсер розкладу ЦНТУ (інтерфейс командного рядка).

Використання:
    python parse.py                      # завантажити і зберегти всі групи у schedules/
    python parse.py --list               # вивести список доступних груп
    python parse.py --group "КН-25"      # зберегти одну конкретну групу
    python parse.py --db                 # зберегти всі групи у БД (з XLS)
    python parse.py --group "КН-25" --db # зберегти одну групу у БД (з XLS)
    python parse.py --json schedule.json # зберегти групу у БД з JSON-файлу (зі збереженням посилань)
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from bot.database import init_db
from bot.database.base import SessionLocal
from bot.database.crud import upsert_group
from bot.services import run_parser, save_schedules

OUTPUT_DIR = Path(__file__).resolve().parent / "schedules"


async def _save_to_db(schedules: dict[str, Any], group: str | None) -> None:
    await init_db()
    targets = {group: schedules[group]} if group else schedules
    async with SessionLocal() as session:
        for name, data in targets.items():
            await upsert_group(session, name, data.get("course", ""), data["schedule"])
            print(f"  DB: saved {name}")
    print(f"Saved {len(targets)} group(s) to DB.")


async def _save_json_to_db(path: Path) -> None:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    group = data.get("group", path.stem)
    await init_db()
    async with SessionLocal() as session:
        await upsert_group(session, group, data.get("course", ""), data["schedule"])
    print(f"DB: saved {group} from {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KNTU schedule parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--group", metavar="NAME", help="Group name to save (e.g. 'КН-25')")
    parser.add_argument("--list", action="store_true", help="List all available groups")
    parser.add_argument("--db", action="store_true", help="Save schedule to DB (from XLS)")
    parser.add_argument("--json", metavar="FILE", help="Load schedule from JSON file into DB")
    args = parser.parse_args()

    if args.json:
        asyncio.run(_save_json_to_db(Path(args.json)))
        return

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

    if args.db:
        asyncio.run(_save_to_db(schedules, group))
        return

    if group:
        data = schedules[group]
        safe = group.replace(" ", "-").replace("/", "-").replace("'", "")
        out_file = OUTPUT_DIR / f"{safe}.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {"group": group, "course": data.get("course", ""), "schedule": data["schedule"]}
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_file}")
        return

    save_schedules(schedules, OUTPUT_DIR)


if __name__ == "__main__":
    main()
