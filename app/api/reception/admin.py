# Register your models here.
from django.contrib import admin
from .filters import DatePeriodListFilter
from .models.feedback import Feedback
from .models.reception import Reception


@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'service', 'client', 'master',
                    'company', 'start_datetime', 'end_datetime')
    list_display_links = ('id',)
    list_filter = (DatePeriodListFilter, 'status', 'company', 'service')


admin.site.register(Feedback)
