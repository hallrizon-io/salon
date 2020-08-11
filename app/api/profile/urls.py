from django.urls import path
from .views import ProfileAPIView
from api.master.views import CreateMasterView

urlpatterns = [
    path('profiles/', ProfileAPIView.as_view()),
    path('profiles/master', CreateMasterView.as_view()),
]
