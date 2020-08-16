from datetime import date, timedelta, datetime, time

from objects.calendar import Calendar
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DatePeriodListFilter(admin.SimpleListFilter):
    title = _('Date Period')
    parameter_name = 'date_period'

    def lookups(self, request, model_admin):
        return (
            ('yesterday', _('Yesterday')), ('today', _('Today')), ('tomorrow', _('Tomorrow')),
            ('prev_week', _('Preview week')), ('this_week', _('This week')), ('next_week', _('Next week')),
            ('prev_month', _('Preview month')), ('this_month', _('This month')), ('next_month', _('Next month'))
        )

    def queryset(self, request, queryset):
        dates = []
        today = date.today()
        if self.value() == 'yesterday':
            dates.extend([today - timedelta(days=1), today])
        elif self.value() == 'today':
            dates.extend([today, today + timedelta(days=1)])
        elif self.value() == 'tomorrow':
            dates.extend([today + timedelta(days=1), today + timedelta(days=2)])
        elif self.value() == 'prev_week':
            dates.extend(Calendar.get_week_dates(today.year, today.isocalendar()[1] - 1))
        elif self.value() == 'this_week':
            dates.extend(Calendar.get_week_dates(today.year, today.isocalendar()[1]))
        elif self.value() == 'next_week':
            dates.extend(Calendar.get_week_dates(today.year, today.isocalendar()[1] + 1))
        elif self.value() == 'prev_month':
            dates.extend(Calendar.get_month_dates(today.year, today.month - 1))
        elif self.value() == 'this_month':
            dates.extend(Calendar.get_month_dates(today.year, today.month))
        elif self.value() == 'next_month':
            dates.extend(Calendar.get_month_dates(today.year, today.month + 1))
        else:
            #Unix Epoch
            dates.extend([datetime(1970, 1, 1), datetime(2038, 1, 19)])

        timestamp_range = [int(date.timestamp()) for date in map(datetime.combine, dates, [time()] * 2)]

        return queryset.filter(start_timestamp__range=timestamp_range)
