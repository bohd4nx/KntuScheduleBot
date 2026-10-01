<div align="center">

# KNTU Schedule Bot

Telegram-бот для перегляду розкладу занять студентів [Центральноукраїнського національного технічного університету](https://kntu.kr.ua/) (ЦНТУ).

**[Повідомити про баг](https://github.com/bohd4nx/KntuScheduleBot/issues)** · **[Запропонувати функцію](https://github.com/bohd4nx/KntuScheduleBot/issues)**

</div>

---

## Можливості

- Розклад на сьогодні, завтра та весь тиждень
- Розклад береться напряму з порталу ЦНТУ (`portal.kntu.kr.ua`), відповіді кешуються в Redis на добу
- Тип заняття (ЛК / ПЗ / ЛАБ), оголошення від викладачів
- На вихідних «тиждень» показує наступний навчальний тиждень

---

## Запуск

**Вимоги:** Python 3.12+, Docker + Docker Compose, Redis

```bash
git clone https://github.com/bohd4nx/KntuScheduleBot.git
cd KntuScheduleBot
cp .env.example .env   # заповніть BOT_TOKEN, PORTAL_REFRESH_TOKEN
```

```bash
# Docker (рекомендовано)
docker compose up -d

# або локально
pip install .
python main.py
```

---

## Доступ до порталу

Бот ходить на портал від імені студента: `GET /api/student/me/timetable`. Групу портал визначає сам.

1. Увійти на [portal.kntu.kr.ua](https://portal.kntu.kr.ua), у DevTools → Application → Cookies скопіювати `staffportal_refresh`.
2. Записати в `.env` як `PORTAL_REFRESH_TOKEN`.

Портал ротує refresh-токен при кожному оновленні, тому актуальний бот зберігає в **Redis** (`kntu:portal:refresh_token`),
а змінна `.env` потрібна лише для першого запуску. Redis має бути з персистентністю (в `docker-compose.yml` — AOF + volume):
без неї після рестарту бот спробує вже недійсний токен із `.env`.

Сесію бот оновлює сам: заздалегідь за терміном access-токена, після 401 і фоновим циклом раз на 12 годин
(тримає refresh-токен живим). Якщо в логах `Portal refresh token rejected` — вставте свіжий токен у `.env`:
змінене значення бот підхоплює при старті.

## Кеш

Відповіді порталу кешуються в Redis по тижнях: свіжі 24 години, зберігаються 7 днів. Якщо портал недоступний,
бот віддає застарілий запис. Недоступність самого Redis не валить бота — кеш просто пропускається.
