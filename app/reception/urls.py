from django.urls import path
from .views import ReceptionListView


urlpatterns = [
    path('api/v1/orders/', ReceptionListView.as_view()),
]
