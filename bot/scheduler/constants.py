DAILY_SCHEDULE_HOUR: int = 6
DAILY_SCHEDULE_DAYS: str = "mon-fri"

# APScheduler за замовчуванням пропускає запуск, що запізнився більш ніж на 1 с (зайнятий цикл, рестарт).
DAILY_SCHEDULE_MISFIRE_GRACE_SECONDS: int = 60 * 60

DAILY_SCHEDULE_ATTEMPTS: int = 3
DAILY_SCHEDULE_RETRY_SECONDS: int = 5 * 60
