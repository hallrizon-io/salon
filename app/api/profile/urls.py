from django.urls import path
from .views import ProfileAPIView


urlpatterns = [
    path('profiles/', ProfileAPIView.as_view()),
]
