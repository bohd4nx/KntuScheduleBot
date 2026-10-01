from .client import close as close_schedule_client
from .client import start_keepalive
from .exceptions import PortalError
from .methods import get_day, get_week
from .schemas import Lesson

__all__ = [
    "Lesson",
    "PortalError",
    "close_schedule_client",
    "get_day",
    "get_week",
    "start_keepalive",
]
