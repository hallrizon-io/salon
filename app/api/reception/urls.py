from django.urls import path
from .views import ReceptionListView


urlpatterns = [
    path('orders/', ReceptionListView.as_view()),
]
