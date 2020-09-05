from django.db import models
from rest_framework.exceptions import ValidationError

from api.company.models.company import Company
from api.profile.models import Profile
from objects.feedback import validate_feedback_mark
from api.reception.models import Reception


class Feedback(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True, related_name='feedbacks')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='companies_assessment')
    mark = models.DecimalField(max_digits=2, decimal_places=1, validators=[validate_feedback_mark])

    class Meta:
        unique_together = ['company', 'client']

    def save(self, **kwargs):
        Company.is_company_exist(self.company_id, raise_exception=True)
        Profile.is_profile_exist(self.client_id, raise_exception=True)
        if not Reception.objects.filter(company=self.company_id, client=self.client_id).exists():
            raise ValidationError({'client_id': 'Ops, you cannot leave feedback because you never used our services'})
        self.full_clean()
        super(Feedback, self).save(**kwargs)
