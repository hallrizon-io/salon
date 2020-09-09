from abc import abstractmethod, ABC
from datetime import date, timedelta, datetime
from objects.calendar import Calendar


class DatePeriodState:
    def __init__(self):
        self.today = date.today()

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @abstractmethod
    def get_dates(self):
        pass

    @staticmethod
    def get_object(period):
        if period is None:
            period = 'default'

        periods = {
            'yesterday': YesterdayState(),
            'today': TodayState(),
            'tomorrow': TomorrowState(),
            'prev_week': PreviousWeek(),
            'this_week': ThisWeek(),
            'next_week': NextWeek(),
            'prev_month': PreviousMonth(),
            'this_month': ThisMonth(),
            'next_month': NextMonth(),
            'default': DefaultPeriod()
        }

        return periods[period]


class TodayState(DatePeriodState, ABC):
    def get_dates(self):
        return [self.today, self.today + timedelta(days=1)]


class YesterdayState(DatePeriodState, ABC):
    def get_dates(self):
        return [self.today, self.today - timedelta(days=1)]


class TomorrowState(DatePeriodState, ABC):
    def get_dates(self):
        return [self.today + timedelta(days=1), self.today + timedelta(days=2)]


class PreviousWeek(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1] - 1)


class ThisWeek(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1])


class NextWeek(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1] + 1)


class PreviousMonth(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month - 1)


class ThisMonth(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month)


class NextMonth(DatePeriodState, ABC):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month + 1)


class DefaultPeriod(DatePeriodState, ABC):
    def get_dates(self):
        return [datetime(1970, 1, 1), datetime(2038, 1, 19)]
