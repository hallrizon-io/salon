from django.urls import path
from .views import MasterListView, MasterBookedHoursView


urlpatterns = [
    path('masters/', MasterListView.as_view()),
    path('masters/<int:pk>/', MasterBookedHoursView.as_view()),
]
