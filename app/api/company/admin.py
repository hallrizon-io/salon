# Register your models here.
from .models import Company
from django.contrib import admin


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'opening_hours', 'closing_hours', 'rating', 'is_active')
    list_display_links = ('name',)

    def get_queryset(self, request):
        if request.resolver_match.func.__name__ == 'changelist_view':
            return Company.all_with_calculated_rating()
        else:
            return super(CompanyAdmin, self).get_queryset(request)

    def rating(self, obj):
        return 'No feedbacks yet' if obj.rating is None else round(obj.rating, 1)
