from datetime import datetime, time
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from objects.date_period import DatePeriodState


class DatePeriodListFilter(admin.SimpleListFilter):
    title = _('Date Period')
    parameter_name = 'date_period'

    def __init__(self,  request, params, model, model_admin):
        super(DatePeriodListFilter, self).__init__(request, params, model, model_admin)
        self.state = DatePeriodState.get_object(self.value())
        self.state.context = self

    def lookups(self, request, model_admin):
        return (
            ('yesterday', _('Yesterday')), ('today', _('Today')), ('tomorrow', _('Tomorrow')),
            ('prev_week', _('Preview week')), ('this_week', _('This week')), ('next_week', _('Next week')),
            ('prev_month', _('Preview month')), ('this_month', _('This month')), ('next_month', _('Next month'))
        )

    def queryset(self, request, queryset):
        dates = self.state.get_dates()
        timestamp_range = [int(date.timestamp()) for date in map(datetime.combine, dates, [time()] * 2)]
        return queryset.filter(start_timestamp__range=timestamp_range)
