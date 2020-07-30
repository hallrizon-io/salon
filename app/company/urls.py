from django.urls import path
from .views import CompanyListView


urlpatterns = [
    path('api/v1/companies/', CompanyListView.as_view()),
]
