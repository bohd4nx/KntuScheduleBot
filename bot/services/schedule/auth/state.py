import asyncio
from dataclasses import dataclass, field


@dataclass
class AuthState:
    access_expires_at: float = 0.0  # 0 — access-токена ще немає
    refresh_cookie_loaded: bool = False  # refresh із Redis підтягуємо при першому оновленні
    refresh_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    keepalive_task: "asyncio.Task[None] | None" = None


state = AuthState()
