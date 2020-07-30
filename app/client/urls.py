from django.urls import path
from .views import ClientListView


urlpatterns = [
    path('api/v1/clients/', ClientListView.as_view()),
]
