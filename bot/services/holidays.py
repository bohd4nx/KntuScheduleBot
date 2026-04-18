import logging
from datetime import date, timedelta
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)

API_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/UA"


class HolidayService:
    def __init__(self) -> None:
        self._cache: dict[int, dict[date, str]] = {}

    async def ensure_loaded(self, year: int) -> None:
        """Завантажує свята для вказаного року (один раз)."""
        if year in self._cache:
            return
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(
                    API_URL.format(year=year),
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status != 200:
                        logger.warning("Nager.at returned %d for year %d", resp.status, year)
                        self._cache[year] = {}
                        return
                    data: list[dict[str, Any]] = await resp.json()
        except Exception as exc:
            logger.warning("Failed to load holidays for %d: %s", year, exc)
            self._cache[year] = {}
            return

        holidays: dict[date, str] = {}
        for item in data:
            d = date.fromisoformat(item["date"])
            name: str = item["localName"]
            holidays[d] = name
            # Якщо свято випало на неділю — понеділок теж вихідний (перенесення)
            if d.weekday() == 6:
                holidays[d + timedelta(days=1)] = name

        self._cache[year] = holidays
        logger.info("Loaded %d holiday entries for %d", len(holidays), year)

    def get_name(self, d: date) -> str | None:
        """Повертає локалізовану назву свята для дати або None."""
        return self._cache.get(d.year, {}).get(d)


holiday_service = HolidayService()
