from datetime import datetime, timedelta
from typing import Final

# Дні тижня (використовуються у всьому проєкті)
DAYS: Final = (
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
)

WORK_DAYS: Final = DAYS[:5]
DEFAULT_LOCALE: Final = "uk"
DATE_FORMAT: Final = "%d.%m.%Y"

SEMESTER_START_DATE: Final = datetime.strptime("16.02.2026", DATE_FORMAT)
SEMESTER_END_DATE: Final = datetime.strptime("01.07.2026", DATE_FORMAT)

# Дати кураторських годин
CURATOR_HOUR_DATES: Final = (
    "03.03.2026",
    "07.04.2026",
    "05.05.2026",
    "02.06.2026",
)

REGULAR_CLASS_TIMES: Final = {
    "1": {"start": "08:30", "end": "09:50"},
    "2": {"start": "10:00", "end": "11:20"},
    "3": {"start": "11:30", "end": "12:50"},
    "4": {"start": "13:20", "end": "14:40"},
    "5": {"start": "14:50", "end": "16:10"},
    "6": {"start": "16:20", "end": "17:40"},
}

# З 3-ї пари розклад зсувається на 40 хв через кураторську годину.
CURATOR_SHIFT_FROM = 3
CURATOR_DELTA = timedelta(minutes=40)


def _shift(slot: dict[str, str]) -> dict[str, str]:
    fmt = "%H:%M"
    return {
        "start": (datetime.strptime(slot["start"], fmt) + CURATOR_DELTA).strftime(fmt),
        "end": (datetime.strptime(slot["end"], fmt) + CURATOR_DELTA).strftime(fmt),
    }


CURATOR_CLASS_TIMES: Final = {k: (_shift(v) if int(k) >= CURATOR_SHIFT_FROM else v) for k, v in REGULAR_CLASS_TIMES.items()}

# Нормалізація назв днів із XLS (капс -> нормальний регістр)
PARSER_DAY_ALIASES: Final = {
    "ПОНЕДІЛОК": "Понеділок",
    "ВІВТОРОК": "Вівторок",
    "СЕРЕДА": "Середа",
    "ЧЕТВЕР": "Четвер",
    "П'ЯТНИЦЯ": "П'ятниця",
}

# Визначення курсу із заголовка XLS («ТРЕТІЙ КУРС» -> '3 курс')
PARSER_COURSE_LABELS: Final = {
    "ПЕРШИЙ": "1 курс",
    "ДРУГИЙ": "2 курс",
    "ТРЕТІЙ": "3 курс",
    "ЧЕТВЕРТИЙ": "4 курс",
    "П'ЯТИЙ": "5 курс",
    "ШОСТИЙ": "6 курс",
}
