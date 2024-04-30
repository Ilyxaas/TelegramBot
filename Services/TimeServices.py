import calendar
import datetime
from datetime import date
from datetime import timedelta


class TimeServices:

    @staticmethod
    def CurrentDay():
        return date.today()

    @staticmethod
    def NextDay():
        return date.today() + timedelta(days=1)

    @staticmethod
    def EndDayInWeek():
        today = date.today()
        return today + timedelta(days=6 - today.weekday())

    @staticmethod
    def EndDayInMonth():
        today = date.today()
        LastDayIndex = calendar.monthrange(today.year, today.month)[1]
        print(LastDayIndex)
        EndDay = date(today.year, today.month, LastDayIndex)
        return EndDay

    @staticmethod
    def StringToDateTime(Str: str) -> (date, bool):
        try:
            splits = Str.split('-')
            if len(splits) == 3:
                Year = int(splits[0])
                Month = int(splits[1])
                Day = int(splits[2])
        except:
            return None, False

        if 0 < Month < 13:
            LastDayIndex = calendar.monthrange(Year, Month)[1]
            if Day < LastDayIndex:
                return date(Year, Month, Day), True
            else:
                return None, False
        else:
            return None, False

    @staticmethod
    def CompareDate(Date1 : date, Date2: date) -> (date, bool):
        if Date1.year >= Date2.year and Date1.month >= Date2.month and Date1.day > Date2.day:
            return True
        return False

    @staticmethod
    def GetCurrentDayTime():
        result = str(datetime.datetime.now()).split('.')[0]
        return result



