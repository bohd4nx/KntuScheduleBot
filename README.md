<div align="center">

# KNTU Schedule Bot

Telegram-бот для перегляду розкладу занять студентів [Центральноукраїнського національного технічного університету](https://kntu.kr.ua/) (ЦНТУ).

**[Повідомити про баг](https://github.com/bohd4nx/KntuScheduleBot/issues)** · **[Запропонувати функцію](https://github.com/bohd4nx/KntuScheduleBot/issues)**

</div>

---

## Можливості

- Розклад на сьогодні, завтра та весь тиждень
- Автоматичне визначення типу тижня (чисельник / знаменник)
- На вихідних «тиждень» показує наступний навчальний тиждень
- Відображення посилань на онлайн-заняття
- Підсвічування державних свят та кураторських годин

---

## Запуск

**Вимоги:** Python 3.12+, Docker + Docker Compose, PostgreSQL

```bash
git clone https://github.com/bohd4nx/KntuScheduleBot.git
cd KntuScheduleBot
cp .env.example .env   # заповніть BOT_TOKEN, POSTGRES_*
```

```bash
# Docker (рекомендовано)
docker compose up -d

# або локально
pip install .
python main.py
```

---

## Завантаження розкладу в БД

```bash
docker compose exec bot python parse.py              # всі групи
docker compose exec bot python parse.py --group КН-25  # одна група
docker compose exec bot python parse.py --list         # список груп
```

---

## Налаштування семестру

Дати задаються в `bot/core/constants.py`:

```python
SEMESTER_START_DATE = datetime.strptime("16.02.2026", DATE_FORMAT)
SEMESTER_END_DATE   = datetime.strptime("01.07.2026", DATE_FORMAT)
```
