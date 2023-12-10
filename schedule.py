from logger import logger


_log = logger.getLogger(__name__)

try:
    import urllib3
    import requests
    from bs4 import BeautifulSoup

    from customCalendar import CustomCalendar
    from calandarExceptions import (
        TodayIsDaOffException,
        TodaySundayException
    )

    urllib3.disable_warnings()
except Exception as e:
    _log.error(e)


class _ScheduleParser:
    def __init__(self, url):
        self.__url = url
        self.__group = None
        self.__response = None
        self.__soup = None
        self.__table = None
        self.__listOfGroups = self.__getGroups()

    def setGroup(self, group):
        self.__group = group

    def getLessons(self):
        self.__response = self.__getGroupPageResponse()
        self.__soup = self.__getGroupPageSoup()
        self.__table = self.__getGroupScheduleTable()
        try:
            currentDayIndex, currentDay = self.__findDay()
            lessonsWithUncleanText = self.__findAllLessonsOfTheCurrentDay(currentDayIndex)
            lessons = self.__getCleanText(lessonsWithUncleanText)
            return lessons
        except TodaySundayException as e:
            return None
        except TodayIsDaOffException as e:
            return "Выходной"
        finally:
            self.__clear()

    def getScheduleForAllGroups(self):
        lessons = []
        for group in self.__listOfGroups:
            self.setGroup(group)
            groupLessons = self.getLessons()
            lessons.append(
                {
                    "group": group,
                    "lessons": groupLessons
                }
            )
        return lessons

    def __getGroupPageResponse(self):
        groupUrl = f"{self.__url}{self.__group}.html"
        return requests.get(groupUrl, verify=False)

    def __getGroupPageSoup(self):
        return BeautifulSoup(self.__response.text.encode("latin-1", "ignore"), "lxml")

    def __getPageResponseWithAllGroups(self):
        return requests.get("https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai/%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D1%8B.html", verify=False)

    def __getSoupPageWithAllGroups(self, response):
        return BeautifulSoup(response.text.encode("latin-1", "ignore"), "lxml")

    def __getGroups(self):
        response = self.__getPageResponseWithAllGroups()
        soup = self.__getSoupPageWithAllGroups(response)
        groupContainer = soup.find("div", {"class": "колонки-группы"})
        groups = groupContainer.find_all("p")
        return [group.text for group in groups]

    def __getGroupScheduleTable(self):
        return self.__soup.find("table",  {"class": "расписание"})

    def __findDay(self):
        date = CustomCalendar.getDateToday()
        dayNumber = CustomCalendar.getDayNumber(date)
        dateString = f"{CustomCalendar.getDayOfTheWeek(date)}, {dayNumber}"
        for index, date in enumerate(self.__table.find_all("tr")):
            if dateString in date.text:
                return index, date.text
        else:
            raise TodayIsDaOffException(CustomCalendar.getDateToday())


    def __findAllLessonsOfTheCurrentDay(self, elementIndex):
        lessons = []
        allTableRows = self.__table.find_all("tr")[elementIndex + 1:]
        for lesson in allTableRows:
            if lesson.attrs.get("class") == ["дата"]:
                return lessons
            if lesson.attrs.get("class") == ["занятие"]:
                lessons.append(lesson.text)

    def __getCleanText(self, lessons):
        clearedText = []
        for lesson in lessons:
            lesson = lesson.replace("\n", " ")
            lesson = lesson.replace("\xa0", "_")
            lesson = lesson.replace("\xad", "")
            lesson = lesson.strip()
            splitText = lesson.split(" ")
            time = splitText[0]
            lessonNumber = time[0]
            if len(time) == 23:
                time = time[12:]
            else:
                time = time[11:]
            discipline = " ".join(splitText[1:-2]).split(",")
            numberOfPairs = len(discipline)
            if numberOfPairs >= 2:
                discipline = " ".join(discipline[0].split()[:-1])
                teacher = [teacher.replace("_", " ").replace(",", "") for teacher in
                           splitText[:-numberOfPairs:][-numberOfPairs:]]
                cabinet = [cabinet.replace(",", "") for cabinet in splitText[-numberOfPairs:]]
            else:
                discipline = " ".join(discipline)
                teacher = splitText[-2].replace("_", " ")
                cabinet = splitText[-1]
            clearedText.append(
                {
                    "lesson": lessonNumber,
                    "time": time,
                    "discipline": discipline,
                    "teacher": teacher,
                    "cabinet": cabinet
                }
            )
        return clearedText

    def __clear(self):
        self.__group = None
        self.__response = None
        self.__soup = None
        self.__table = None

    @property
    def groups(self):
        return self.__listOfGroups


g_scheduleParser = _ScheduleParser("https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai/")
"https://xn--80aapkb3algkc.xn--j1afpl.xn--p1ai/%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D1%8B.html"
