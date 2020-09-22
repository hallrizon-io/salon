from django.db import models
from api.company.models.company import Company
from api.profile.models import Profile
from main.validators import validate_feedback_mark


class Feedback(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True, related_name='feedbacks')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='companies_assessment')
    mark = models.DecimalField(max_digits=2, decimal_places=1, validators=[validate_feedback_mark])

    class Meta:
        unique_together = ['company', 'client']

    def save(self, **kwargs):
        self.full_clean()
        super(Feedback, self).save(**kwargs)
