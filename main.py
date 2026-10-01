import asyncio

from bot.app import run
from bot.core import logger, setup_logging


def main() -> None:
    setup_logging()
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        logger.exception("Unexpected error")


if __name__ == "__main__":
    main()
