from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CachedWeek:
    """Сира відповідь порталу за тиждень і час, коли її отримали."""

    fetched_at: float
    payload: Any
