from django.contrib import admin
from .models import Master, WorkTypes

# Register your models here.
admin.site.register([Master, WorkTypes])