from datetime import date, timedelta
from enum import IntEnum, StrEnum

from calandarExceptions import (
    TodaySundayException,
)


class DayOfTheWeekNumber(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class DayOfTheWeek(StrEnum):
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота"
    SUNDAY = "Воскресенье"


class CustomCalendar:
    @staticmethod
    def getDateToday():
        return date.today()

    @staticmethod
    def getTomorrowsDate():
        dateToday = date.today()
        return dateToday + timedelta(days=1)

    @staticmethod
    def getDayNumber(date):
        return date.day

    @staticmethod
    def getDayOfTheWeek(date):
        dayOfTheWeekNumber = DayOfTheWeekNumber(date.weekday())
        if dayOfTheWeekNumber == 6:
            raise TodaySundayException(date)
        dayOfTheWeek = DayOfTheWeek[dayOfTheWeekNumber.name]
        return dayOfTheWeek
