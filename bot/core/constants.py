from datetime import datetime
from typing import Final

# Дні тижня у форматі, що використовується в schedule.json.
DAYS: Final[tuple[str, ...]] = (
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
)

# Робочі дні для виводу тижневого розкладу.
WORK_DAYS: Final[tuple[str, ...]] = DAYS[:5]

# Єдина локаль, яку використовує бот.
DEFAULT_LOCALE: Final[str] = "uk"

# Формат дат семестру у проєкті.
DATE_FORMAT: Final[str] = "%d.%m.%Y"

# Дата початку семестру.
SEMESTER_START_DATE: Final[datetime] = datetime.strptime("16.02.2026", DATE_FORMAT)

# Дата завершення семестру.
SEMESTER_END_DATE: Final[datetime] = datetime.strptime("01.07.2026", DATE_FORMAT)
