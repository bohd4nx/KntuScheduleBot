from zoneinfo import ZoneInfo

# Не покладаємось на TZ системи: поза Docker «сьогодні» теж має рахуватися за Києвом.
KYIV_TZ: ZoneInfo = ZoneInfo("Europe/Kyiv")

WORK_DAYS_COUNT: int = 5
