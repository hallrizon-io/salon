from django.urls import path
from .views import FeedbackAPIView

urlpatterns = [
    path('feedbacks/', FeedbackAPIView.as_view())
]
