from pydantic import BaseModel, ConfigDict

from bot.services.schedule.enums import LessonKind


class SubjectLinks(BaseModel):
    """Посилання предмета: окреме для типу пари або `default` для всіх інших."""

    # Друкарська помилка в ключі має впасти на старті, а не тихо сховати посилання.
    model_config = ConfigDict(extra="forbid", frozen=True)

    default: str | None = None
    lecture: str | None = None
    practice: str | None = None
    seminar: str | None = None
    lab: str | None = None

    def for_kind(self, kind: LessonKind | None) -> str | None:
        own: str | None = getattr(self, kind.name.lower()) if kind else None
        return own or self.default
