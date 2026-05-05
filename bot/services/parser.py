import logging
import os
from typing import Any, cast
from urllib.request import Request, urlopen

import xlrd

from bot.utils import ScheduleParser, SheetView

logger = logging.getLogger(__name__)


def _resolve_url(url: str | None) -> str:
    resolved = url or os.getenv("PARSER_SOURCE_URL", "").strip()
    if not resolved:
        raise RuntimeError("Schedule URL is not set. Pass a URL directly or set the PARSER_SOURCE_URL environment variable.")
    return resolved


def _fetch_xls(url: str) -> bytes:
    logger.debug("Fetching XLS from %s", url)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        data = cast(bytes, response.read())
    logger.debug("Downloaded %d bytes", len(data))
    return data


def run_parser(url: str | None = None) -> dict[str, dict[str, Any]]:
    """Завантажує і парсить XLS-розклад. Повертає словник груп."""
    raw = _fetch_xls(_resolve_url(url))
    workbook = xlrd.open_workbook(file_contents=raw, formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    result = ScheduleParser(SheetView(sheet)).parse()
    logger.info("Parsed %d groups", len(result))
    return result
