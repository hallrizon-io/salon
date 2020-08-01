from django.urls import path, include

urlpatterns = [
    path('', include('api.profile.urls')),
    path('', include('api.company.urls')),
    path('', include('api.master.urls')),
    path('', include('api.reception.urls'))
]
