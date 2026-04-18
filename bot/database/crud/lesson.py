from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.lesson import Lesson


async def upsert_group(
    session: AsyncSession,
    group_name: str,
    course: str,
    schedule: dict[str, Any],
) -> None:
    """Замінює всі пари групи. schedule — словник вигляду {день: {номер: {тип: {...}}}}."""
    await session.execute(delete(Lesson).where(Lesson.group_name == group_name))

    rows: list[dict[str, Any]] = []
    for day, day_data in schedule.items():
        for lesson_number, week_data in day_data.items():
            for week_type, info in week_data.items():
                if not isinstance(info, dict):
                    continue
                rows.append(
                    {
                        "group_name": group_name,
                        "course": course,
                        "day": day,
                        "lesson_number": lesson_number,
                        "week_type": week_type,
                        "subject": info.get("subject", "Невідомо"),
                        "teacher": info.get("teacher", "Невідомо"),
                        "room": info.get("room", "Невідомо"),
                        "online_link": info.get("online_link") or None,
                    }
                )

    if rows:
        await session.execute(insert(Lesson), rows)

    await session.commit()


async def get_lessons(
    session: AsyncSession,
    group_name: str,
    day: str,
    week_type: str,
) -> list[Lesson]:
    """Повертає відсортовані пари для групи на конкретний день і тип тижня."""
    result = await session.execute(
        select(Lesson)
        .where(
            Lesson.group_name == group_name,
            Lesson.day == day,
            Lesson.week_type == week_type,
        )
        .order_by(Lesson.lesson_number)
    )
    return list(result.scalars())


async def get_groups(session: AsyncSession) -> list[str]:
    """Повертає відсортований список унікальних назв груп."""
    result = await session.execute(select(Lesson.group_name).distinct())
    return sorted(result.scalars())
