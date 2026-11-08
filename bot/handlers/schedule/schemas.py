from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScheduleView:
    """Результат запиту: готовий `text` або ключ локалі `notice` (алерт — `alert-<notice>`), чому показати нічого."""

    text: str | None = None
    notice: str | None = None
