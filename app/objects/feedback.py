from abc import abstractmethod, ABC
from rest_framework import status
from rest_framework.exceptions import ValidationError
from api.reception.models import Reception
from api.reception.models import Feedback
from api.company.models import Company
from api.profile.models import Profile


class FeedbackManager:
    def __init__(self, request):
        self.strategy = ReceptionStrategy() if 'reception_id' in request else CompanyStrategy()
        self.check_required_params(request)
        self.strategy.set_request(request)

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def check_required_params(self, request):
        missing_params = set(self.strategy.required) - set(request.keys())
        if missing_params:
            raise ValidationError({param: f'Missing required parameter "{param}"' for param in missing_params})

    def execute(self):
        self.strategy.give_feedback()
        return self.strategy.get_response()


class Strategy:
    required = ()

    @abstractmethod
    def give_feedback(self):
        pass

    def set_request(self, request):
        for key, value in request.items():
            setattr(self, key, value)

    def get_response(self):
        message = 'Feedback was successful created' if self.is_created else 'Your feedback was changed'
        status_code = status.HTTP_201_CREATED if self.is_created else status.HTTP_200_OK
        return {
            'message': message,
            'status_code': status_code
        }


class ReceptionStrategy(Strategy, ABC):
    required = ('reception_id', 'mark')

    def give_feedback(self):
        reception = Reception.objects.get(pk=self.reception_id)
        feedback, is_created = Feedback.objects.update_or_create(
            reception=reception, defaults={'mark': self.mark}
        )
        self.is_created = is_created


class CompanyStrategy(Strategy, ABC):
    required = ('client_id', 'company_id', 'mark')

    def give_feedback(self):
        company = Company.objects.get(pk=self.company_id)
        profile = Profile.objects.get(pk=self.client_id)
        feedback, is_created = company.feedbacks.update_or_create(
            client=profile, company=company, defaults={'mark': self.mark}
        )
        self.is_created = is_created
