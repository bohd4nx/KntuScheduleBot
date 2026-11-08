from aiogram import Bot
from aiogram_i18n import I18nContext, I18nMiddleware
from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.core import DEFAULT_LOCALE, logger, settings
from bot.utils.constants import KYIV_TZ

from .constants import DAILY_SCHEDULE_DAYS, DAILY_SCHEDULE_HOUR, DAILY_SCHEDULE_MISFIRE_GRACE_SECONDS
from .jobs import send_daily_schedule


def on_job_error(event: JobExecutionEvent) -> None:
    logger.error("Scheduled job %s failed", event.job_id, exc_info=event.exception)


def build_scheduler(bot: Bot, i18n: I18nMiddleware) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=KYIV_TZ)
    scheduler.add_listener(on_job_error, EVENT_JOB_ERROR)

    if settings.GROUP_ID is None:
        logger.info("GROUP_ID is not set — daily schedule is disabled")
        return scheduler

    # Поза хендлерами i18n-контексту немає — збираємо власний із дефолтною локаллю.
    context = I18nContext(locale=DEFAULT_LOCALE, core=i18n.core, manager=i18n.manager, data={})
    scheduler.add_job(
        send_daily_schedule,
        "cron",
        day_of_week=DAILY_SCHEDULE_DAYS,
        hour=DAILY_SCHEDULE_HOUR,
        id="send_daily_schedule",
        kwargs={"bot": bot, "i18n": context, "chat_id": settings.GROUP_ID},
        max_instances=1,
        coalesce=True,
        misfire_grace_time=DAILY_SCHEDULE_MISFIRE_GRACE_SECONDS,
    )
    return scheduler
