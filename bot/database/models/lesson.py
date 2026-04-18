from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Ідентифікація слоту
    group_name: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    course: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    day: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    lesson_number: Mapped[str] = mapped_column(String(2), nullable=False)
    week_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "numerator" | "denominator"

    # Вміст
    subject: Mapped[str] = mapped_column(String(256), nullable=False)
    teacher: Mapped[str] = mapped_column(String(256), nullable=False, default="Невідомо")
    room: Mapped[str] = mapped_column(String(64), nullable=False, default="Невідомо")
    online_link: Mapped[str | None] = mapped_column(String(512), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
