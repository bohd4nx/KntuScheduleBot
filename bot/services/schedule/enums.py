from enum import IntEnum


class LessonKind(IntEnum):
    LECTURE = 1
    PRACTICE = 2
    SEMINAR = 3
    LAB = 4

    @property
    def label(self) -> str:
        return {
            LessonKind.LECTURE: "Лекція",
            LessonKind.PRACTICE: "Практична",
            LessonKind.SEMINAR: "Семінар",
            LessonKind.LAB: "Лабораторна",
        }[self]
