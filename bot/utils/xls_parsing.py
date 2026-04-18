import re
from typing import Any

from bot.core.constants import PARSER_COURSE_LABELS

# Шаблони ПІБ викладача: «Прізвище І. Б.» або «Прізвище Ім'я По-батькові».
TEACHER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^(?P<subject>.+?)\s+(?P<teacher>[А-ЯІЇЄҐ][а-яіїєґ''`-]+\s+[А-ЯІЇЄҐ]\.\s*[А-ЯІЇЄҐ]\.)$"),
    re.compile(
        r"^(?P<subject>.+?)\s+(?P<teacher>[А-ЯІЇЄҐ][а-яіїєґ''`-]+\s+[А-ЯІЇЄҐ][а-яіїєґ''`-]+\s+[А-ЯІЇЄҐ][а-яіїєґ''`-]+)$"
    ),
)

# Шаблон аудиторії — використовується і для .search(), і для .fullmatch().
ROOM_PATTERN = re.compile(r"(?i)(спортзал|онлайн|\d+[\w\-]*\s*[а-яА-Яa-zA-Z]?)$")

UNKNOWN = "Невідомо"
WIDE_SPLIT = re.compile(r"\s{2,}")


def compact_spaces(value: str) -> str:
    """Стискає будь-яку послідовність пробілів до одного."""
    return re.sub(r"\s+", " ", value).strip()


def clean_multiline(value: str) -> str:
    """Нормалізує переноси рядків, прибирає порожні рядки та нерозривні пробіли."""
    lines = value.replace("\r", "\n").replace("\xa0", " ").split("\n")
    return "\n".join(line.strip() for line in lines if line.strip())


def normalize_group_names(raw: str) -> list[str]:
    """Розбиває «КБ 25(30), КІ 22-1(9)» -> ['КБ-25', 'КІ-22 (1)']."""
    names = [name for part in raw.split(",") if (name := compact_spaces(re.sub(r"\(\d+\)", "", part)))]
    result = []
    for name in names:
        # «КН 25» -> «КН-25»
        name = re.sub(r"(?<=[А-ЯІЇЄҐа-яіїєґA-Za-z])\s+(?=\d)", "-", name)
        # «КІ-22-1» -> «КІ-22 (1)»
        name = re.sub(r"(?<=\d)-(\d+)$", r" (\1)", name)
        result.append(name)
    return result


def course_from_group_name(group: str, enrollment_year: int = 2025) -> str | None:
    """Визначає курс за роком вступу в назві групи ('КН 25' -> '1 курс')."""
    m = re.search(r"(?<!\d)(\d{2})(?!\d)", group)
    course = enrollment_year - (2000 + int(m.group(1))) + 1 if m else None
    return f"{course} курс" if course and 1 <= course <= 6 else None


def course_from_header(header: str) -> str | None:
    """Визначає курс із заголовка XLS ('ПЕРШИЙ КУРС' -> '1 курс')."""
    upper = header.upper()
    found = next((label for marker, label in PARSER_COURSE_LABELS.items() if marker in upper), None)
    return found or ("Аспірантура" if "АСПІРАНТ" in upper else None)


def _wide_split(text: str) -> list[str]:
    """Розбиває рядок за двома і більше пробілами."""
    return [p for p in WIDE_SPLIT.split(text) if p.strip()]


def _try_recover_teacher(subject: str) -> tuple[str, str | None]:
    """Відокремлює ПІБ викладача, якщо він склеєний із назвою предмета."""
    cleaned = compact_spaces(subject)
    m = next((p.match(cleaned) for p in TEACHER_PATTERNS if p.match(cleaned)), None)
    return (compact_spaces(m.group("subject")), compact_spaces(m.group("teacher"))) if m else (cleaned, None)


def _from_3(lines: list[str]) -> tuple[str, str, str]:
    """Стандартний формат: предмет / викладач / аудиторія."""
    return lines[0], lines[1], lines[2]


def _from_2(lines: list[str]) -> tuple[str, str, str]:
    """Предмет + «Викладач  Аудиторія» через подвійний пробіл."""
    parts = _wide_split(lines[1])
    teacher, room = (parts[0], parts[-1]) if len(parts) >= 2 else (lines[1], UNKNOWN)
    return lines[0], teacher, room


def _from_1(lines: list[str]) -> tuple[str, str, str]:
    """Компактний рядок: «Предмет  Викладач Аудиторія»."""
    one = lines[0]
    m = ROOM_PATTERN.search(one)
    room = m.group(1).strip() if m else UNKNOWN
    payload = one[: m.start()].strip(" ,;") if m else one
    parts = _wide_split(payload)
    subject, teacher = (parts[0], " ".join(parts[1:])) if len(parts) >= 2 else (parts[0] if parts else UNKNOWN, UNKNOWN)
    return subject, teacher, room


# Диспетчер рядкових обробників (fallback -> _from_3 для 3+ рядків).
LINE_PARSERS: dict[int, Any] = {1: _from_1, 2: _from_2}


def parse_lesson(raw: str) -> dict[str, str] | None:
    """Розбирає текст клітинки на {subject, teacher, room}, або None якщо порожньо."""
    text = clean_multiline(raw)
    if not text:
        return None

    lines = text.split("\n")
    subject, teacher, room = LINE_PARSERS.get(len(lines), _from_3)(lines)
    subject = compact_spaces(subject) or UNKNOWN
    teacher = compact_spaces(teacher) or UNKNOWN
    room = compact_spaces(room) or UNKNOWN

    # Аудиторія потрапила в поле викладача — виправляємо.
    if teacher != UNKNOWN and ROOM_PATTERN.fullmatch(teacher):
        room, teacher = (teacher if room == UNKNOWN else room), UNKNOWN

    # Предмет і викладач склеєні широким пробілом — розбиваємо.
    if teacher == UNKNOWN and len(parts := _wide_split(subject)) >= 2:
        subject, teacher = parts[0], " ".join(parts[1:])

    # Лінгвістичний розбір ПІБ як останній засіб.
    if teacher == UNKNOWN:
        subject, recovered = _try_recover_teacher(subject)
        teacher = recovered or UNKNOWN

    return {"subject": subject, "teacher": teacher, "room": room}
