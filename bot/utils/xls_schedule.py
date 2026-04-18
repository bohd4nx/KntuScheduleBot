from typing import Any

import xlrd

from bot.core.constants import PARSER_DAY_ALIASES
from bot.utils.xls_parsing import (
    course_from_group_name,
    course_from_header,
    normalize_group_names,
    parse_lesson,
)


class SheetView:
    def __init__(self, sheet: xlrd.sheet.Sheet) -> None:
        self.sheet = sheet
        self._anchors: dict[tuple[int, int], tuple[int, int]] = {
            (row, col): (rlo, clo)
            for rlo, rhi, clo, chi in sheet.merged_cells
            for row in range(rlo, rhi)
            for col in range(clo, chi)
        }

    def text(self, row: int, col: int) -> str:
        """Повертає текст клітинки, враховуючи об'єднання."""
        r, c = self._anchors.get((row, col), (row, col))
        v = self.sheet.cell_value(r, c)
        return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


class ScheduleParser:
    """Парсер повного розкладу ЦНТУ у форматі XLS. Повертає словник груп."""

    LESSONS_PER_DAY = 6

    def __init__(self, view: SheetView) -> None:
        self.view = view

    def parse(self) -> dict[str, dict[str, Any]]:
        """Парсить весь аркуш і повертає розклад для кожної групи."""
        day_rows = self._find_day_rows()
        group_columns = self._find_group_columns(day_rows["Понеділок"] - 2)
        course_labels = self._find_course_labels()
        groups_data: dict[str, dict[str, Any]] = {}

        for day_name, day_start_row in day_rows.items():
            for n in range(1, self.LESSONS_PER_DAY + 1):
                num_row = day_start_row + (n - 1) * 2
                den_row = num_row + 1
                key = str(n)

                for col, groups in group_columns.items():
                    numerator = parse_lesson(self.view.text(num_row, col))
                    denominator = parse_lesson(self.view.text(den_row, col))
                    if not numerator and not denominator:
                        continue

                    for group in groups:
                        if group not in groups_data:
                            course = course_labels.get(col) or course_from_group_name(group) or "Невідомий курс"
                            groups_data[group] = {
                                "group": group,
                                "course": course,
                                "schedule": {day: {} for day in PARSER_DAY_ALIASES.values()},
                            }
                        groups_data[group]["schedule"][day_name][key] = {
                            "numerator": numerator,
                            "denominator": denominator,
                        }

        return groups_data

    def _find_day_rows(self) -> dict[str, int]:
        """Знаходить перший рядок кожного дня тижня (шукає в колонці 0)."""
        rows: dict[str, int] = {}
        for row in range(self.view.sheet.nrows):
            day = PARSER_DAY_ALIASES.get(self.view.text(row, 0).strip().upper())
            if day and day not in rows:
                rows[day] = row
        missing = [d for d in PARSER_DAY_ALIASES.values() if d not in rows]
        if missing:
            raise ValueError(f"Day rows not found: {', '.join(missing)}")
        return rows

    def _find_group_columns(self, header_row: int) -> dict[int, list[str]]:
        """Повертає словник {колонка: [назви груп]} із рядка заголовків груп."""
        columns = {
            col: groups
            for col in range(self.view.sheet.ncols)
            if (raw := self.view.text(header_row, col).strip()) and (groups := normalize_group_names(raw))
        }
        if not columns:
            raise ValueError("No group columns found in header row")
        return columns

    def _find_course_labels(self) -> dict[int, str | None]:
        """Повертає словник {колонка: курс}, поширюючи мітку зліва направо."""
        header_row = self._find_course_header_row()
        labels: dict[int, str | None] = {}
        current: str | None = None
        for col in range(self.view.sheet.ncols):
            current = course_from_header(self.view.text(header_row, col).strip()) or current
            labels[col] = current
        return labels

    def _find_course_header_row(self, max_rows: int = 20) -> int:
        """Знаходить рядок із заголовками курсів (наприклад, 'ПЕРШИЙ КУРС')."""
        for row in range(min(max_rows, self.view.sheet.nrows)):
            row_text = " ".join(self.view.text(row, c).strip().upper() for c in range(self.view.sheet.ncols))
            if "КУРС" in row_text:
                return row
        raise ValueError("Course header row not found")
