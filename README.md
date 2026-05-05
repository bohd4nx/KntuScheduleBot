<div align="center">

  <h1>KNTU Schedule Bot</h1>

  <p>
    <b>Telegram-бот для перегляду розкладу занять студентів <a href="https://kntu.kr.ua/">Центральноукраїнського національного технічного університету</a> (ЦНТУ).</b>
  </p>

[Повідомити про баг](https://github.com/bohd4nx/KntuScheduleBot/issues) · [Запропонувати функцію](https://github.com/bohd4nx/KntuScheduleBot/issues)

</div>

---

## Можливості

- 📅 Розклад на сьогодні, завтра та весь тиждень
- 🔄 Автоматичне визначення типу тижня (чисельник / знаменник)
- 🧭 На вихідних «тиждень» показує наступний навчальний тиждень
- 🔗 Відображення посилань на онлайн-заняття
- 🗓️ Підсвічування державних свят та кураторських годин

-
## Вимоги

- Docker + Docker Compose
- Токен бота від [@BotFather](https://t.me/BotFather)

---

## Запуск

```bash
git clone https://github.com/bohd4nx/KntuScheduleBot.git
cd KntuScheduleBot
cp .env.example .env
```

Заповніть `.env`:

```bash
docker compose up -d
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

