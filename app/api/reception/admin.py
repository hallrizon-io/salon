from django.contrib import admin
from .models import Reception, ReceptionAdmin

# Register your models here.

admin.site.register(Reception, ReceptionAdmin)
