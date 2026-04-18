from datetime import datetime, timedelta
from typing import Final, Literal

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


def get_week_type(date: datetime) -> Literal["numerator", "denominator"]:
    # Семестр стартував на 8-му ISO-тижні (16.02.2026) як чисельник.
    # 8-й тиждень — парний, тому: парний = чисельник, непарний = знаменник.
    return "numerator" if date.isocalendar()[1] % 2 == 0 else "denominator"


def get_week_monday() -> datetime:
    today = datetime.now()
    # Якщо сьогодні субота або неділя — переходимо до наступного понеділка.
    return today + timedelta(days=7 - today.weekday()) if today.weekday() >= 5 else today - timedelta(days=today.weekday())


def get_week_dates() -> tuple[datetime, datetime]:
    monday = get_week_monday()
    return monday, monday + timedelta(days=4)


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
