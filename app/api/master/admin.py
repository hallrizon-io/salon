# Register your models here.
from django.contrib import admin
from .models.master import Master
from .models.worktypes import WorkTypes


class WorkTypesInline(admin.TabularInline):
    model = WorkTypes
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company' and request._object is not None:
            kwargs["queryset"] = request._object.company.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = (WorkTypesInline,)

    def get_form(self, request, obj=None, **kwargs):
        request._object = obj
        return super(MasterAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(WorkTypes)
