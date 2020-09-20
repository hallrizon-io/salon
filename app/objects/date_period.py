from abc import abstractmethod, ABC
from datetime import date, timedelta, datetime

from django.contrib import admin

from objects.calendar import Calendar
from typing import List, final


class DatePeriodState(ABC):
    today = datetime.today()

    @property
    def context(self):
        """Pointer on context"""
        return self._context

    @context.setter
    def context(self, value: admin.SimpleListFilter):
        """Set pointer on context"""
        self._context = value

    @abstractmethod
    def get_dates(self) -> List[datetime]:
        """Return list of two date instances that based on state"""
        pass

    @staticmethod
    @final
    def get_object(period: str) -> 'DatePeriodState':
        """Return child instance of DatePeriodState"""

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

        if period not in periods:
            period = 'default'

        return periods[period]


class TodayState(DatePeriodState):
    def get_dates(self):
        return [self.today, self.today + timedelta(days=1)]


class YesterdayState(DatePeriodState):
    def get_dates(self):
        return [self.today, self.today - timedelta(days=1)]


class TomorrowState(DatePeriodState):
    def get_dates(self):
        return [self.today + timedelta(days=1), self.today + timedelta(days=2)]


class PreviousWeek(DatePeriodState):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1] - 1)


class ThisWeek(DatePeriodState):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1])


class NextWeek(DatePeriodState):
    def get_dates(self):
        return Calendar.get_week_dates(self.today.year, self.today.isocalendar()[1] + 1)


class PreviousMonth(DatePeriodState):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month - 1)


class ThisMonth(DatePeriodState):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month)


class NextMonth(DatePeriodState):
    def get_dates(self):
        return Calendar.get_month_dates(self.today.year, self.today.month + 1)


class DefaultPeriod(DatePeriodState):
    def get_dates(self):
        return [datetime(1970, 1, 1), datetime(2038, 1, 19)]
