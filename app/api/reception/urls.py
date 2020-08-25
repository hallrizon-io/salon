from django.urls import path
from .views import ReceptionAPIView


urlpatterns = [
    path('receptions/', ReceptionAPIView.as_view()),
]
