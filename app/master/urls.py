from django.urls import path
from .views import MasterListView


urlpatterns = [
    path('api/v1/masters/', MasterListView.as_view()),
]
