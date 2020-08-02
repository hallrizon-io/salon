from django.urls import path
from .views import ReceptionListView


urlpatterns = [
    path('receptions/', ReceptionListView.as_view()),
]
