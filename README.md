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
- 🔗 Відображення посилання на онлайн-заняття з `schedule.json`

---

## Встановлення

```bash
git clone https://github.com/bohd4nx/KntuScheduleBot.git
cd KntuScheduleBot
pip install -e .
```

---

## Налаштування

Створіть `.env` файл:

```bash
cp .env.example .env
```

| Змінна      | Обов'язково | Опис                                                |
| ----------- | ----------- | --------------------------------------------------- |
| `BOT_TOKEN` | Так         | Токен бота від [@BotFather](https://t.me/BotFather) |

Дати семестру задаються в `bot/core/constants.py`:

```python
SEMESTER_START_DATE = datetime.strptime("16.02.2026", DATE_FORMAT)
SEMESTER_END_DATE   = datetime.strptime("01.07.2026", DATE_FORMAT)
```

---

## Налаштування розкладу

Відредагуйте `schedule.json` з розкладом вашої групи.

Для дистанційних занять додайте `online_link`:

```json
"numerator": {
    "subject": "Предмет",
    "teacher": "Викладач",
    "room": "1",
    "online_link": "https://us02web.zoom.us/j/..."
}
```

---

## Запуск

```bash
python main.py
```
