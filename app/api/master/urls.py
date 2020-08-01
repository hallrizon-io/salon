from django.urls import path
from .views import MasterListView


urlpatterns = [
    path('masters/', MasterListView.as_view()),
]
