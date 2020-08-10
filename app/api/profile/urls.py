from django.urls import path
from .views import ProfileAPIView
from ..master.views import MasterAPIView

urlpatterns = [
    path('profiles/', ProfileAPIView.as_view()),
    path('profiles/master', MasterAPIView.as_view()),
]
