# Register your models here.
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'user_type', 'is_active')
    list_display_links = ('full_name',)

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.resolver_match.func.__name__ == 'change_view':
            return qs
        else:
            return qs.filter(user_type=Profile.UserType.CLIENT)
