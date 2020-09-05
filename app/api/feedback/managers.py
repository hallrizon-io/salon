from rest_framework import status
from rest_framework.exceptions import ValidationError
from objects.feedback import FeedbackManager


class FeedbackViewManager:
    def __init__(self, request):
        self.data = request.data

    def processing(self):
        feedback = FeedbackManager(self.data)

        try:
            response = feedback.execute()
            status_code = response.pop('status_code')
        except ValidationError as error:
            response = error.detail
            status_code = status.HTTP_400_BAD_REQUEST

        return response, status_code
