import asyncio

from bot.app import run
from bot.core import logger, setup_logging


def main() -> None:
    setup_logging()
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:  # noqa: BLE001 - top-level guard, log and exit instead of a raw traceback
        logger.exception("Unexpected error")


if __name__ == "__main__":
    main()
