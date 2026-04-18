"""
Парсер розкладу ЦНТУ (інтерфейс командного рядка).

Використання:
    python parse.py                  # завантажити і зберегти всі групи у schedules/
    python parse.py --list           # вивести список доступних груп
    python parse.py --group "КН-25"  # зберегти одну конкретну групу
    python parse.py --out /tmp/out   # вказати вихідну директорію
"""

import argparse
import json
import sys
from pathlib import Path

from bot.services import run_parser, save_schedules


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KNTU schedule parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--group", metavar="NAME", help="Назва групи для збереження (e.g. 'КН-25')")
    parser.add_argument("--list", action="store_true", help="Вивести всі доступні групи")
    parser.add_argument(
        "--out",
        metavar="DIR",
        default="schedules",
        help="Вихідна директорія (default: schedules/)",
    )
    args = parser.parse_args()

    print("Downloading schedule...")
    schedules = run_parser()
    print(f"Found {len(schedules)} groups")

    if args.list:
        for name in sorted(schedules):
            print(f"  {name} — {schedules[name].get('course', '?')}")
        return

    if args.group:
        # Приймаємо і «КН-25», і «КН 25» — нормалізуємо до пробілу.
        group = args.group.strip().replace("-", " ", 1)
        data = schedules.get(group)
        if data is None:
            print(f"Group '{args.group}' not found. Run --list to see available groups.", file=sys.stderr)
            sys.exit(1)

        safe = group.replace(" ", "-").replace("/", "-").replace("'", "")
        out_file = Path(args.out) / f"{safe}.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {"group": group, "course": data.get("course", ""), "schedule": data["schedule"]}
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_file}")
        return

    save_schedules(schedules, Path(args.out))


if __name__ == "__main__":
    main()
