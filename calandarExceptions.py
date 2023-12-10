class BaseCalendarException(Exception):
    def __init__(self, date):
        self.date = date


class TodayIsDaOffException(BaseCalendarException):
    def __str__(self):
        return f"Сегодня <{self.date}> выходной"


class TodaySundayException(TodayIsDaOffException):
    def __str__(self):
        return f"Сегодня <{self.date}> воскресенье"
