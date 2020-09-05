# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from api.feedback.managers import FeedbackViewManager


class FeedbackAPIView(APIView):
    def post(self, request):
        feedback_view_manager = FeedbackViewManager(request)
        return Response(*feedback_view_manager.processing())
