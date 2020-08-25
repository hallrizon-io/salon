from django.contrib import admin
from .models import Master, WorkTypes, WorkTypesAdmin

# Register your models here.
admin.site.register(Master)
admin.site.register(WorkTypes, WorkTypesAdmin)
