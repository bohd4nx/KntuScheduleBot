from enum import StrEnum


class MainMenuCallback(StrEnum):
    SCHEDULE_TODAY = "schedule_today"
    SCHEDULE_TOMORROW = "schedule_tomorrow"
    SCHEDULE_WEEK = "schedule_week"
    HOW_TO_USE = "how_to_use"
    BACK_TO_MENU = "back_to_menu"
