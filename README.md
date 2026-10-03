<div align="center">

# KNTU Schedule Bot

Telegram-бот з розкладом занять для студентів [ЦНТУ](https://kntu.kr.ua/).

**[Повідомити про баг](https://github.com/bohd4nx/KntuScheduleBot/issues)** · **[Запропонувати функцію](https://github.com/bohd4nx/KntuScheduleBot/issues)**

</div>

---

## Що вміє

- Розклад на сьогодні, завтра і тиждень
- Тип заняття (ЛК / ПЗ / ЛАБ) та оголошення викладачів
- На вихідних «тиждень» показує наступний навчальний тиждень
- Щодня о 6:00 за Києвом надсилає розклад на день у чат `GROUP_ID` (на вихідних і в дні без занять мовчить)

Дані бот бере з порталу ЦНТУ (`portal.kntu.kr.ua`) від імені студента, групу портал визначає сам.

## Запуск

Потрібні Docker і Docker Compose (або Python 3.12+ та Redis для запуску без Docker).

```bash
git clone https://github.com/bohd4nx/KntuScheduleBot.git
cd KntuScheduleBot
cp .env.example .env   # впишіть BOT_TOKEN і PORTAL_REFRESH_TOKEN
docker compose up -d
```

Без Docker:

```bash
pip install .
python main.py
```

## Токен порталу

1. Увійдіть на [portal.kntu.kr.ua](https://portal.kntu.kr.ua).
2. У DevTools → Application → Cookies скопіюйте `staffportal_refresh`.
3. Вставте в `.env` як `PORTAL_REFRESH_TOKEN`.

Портал змінює токен при кожному оновленні сесії, тому бот зберігає актуальний у Redis. Значення з `.env` потрібне
лише для першого запуску. Бот оновлює сесію сам, тож токен не протухає.

Якщо в логах з'явилось `Portal refresh token rejected`, вставте свіжий токен у `.env` і перезапустіть бота.

## Кеш

Відповіді порталу лежать у Redis по тижнях. Протягом 12 годин бот віддає їх з кешу, потім під час наступного запиту
оновлює з порталу. Якщо портал недоступний, показує застарілий розклад (зберігається 7 днів). Якщо недоступний
Redis, бот працює без кешу.
