from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CachedWeek:
    fetched_at: float
    payload: Any
