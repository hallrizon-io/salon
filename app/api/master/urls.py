from django.urls import path
from .views import MasterAPIView, MasterBookedHoursView


urlpatterns = [
    path('masters/', MasterAPIView.as_view()),
    path('masters/<int:pk>/', MasterBookedHoursView.as_view()),
]
