from django.db import models
from api.reception.models.reception import Reception
from main.validators import validate_feedback_mark


class Feedback(models.Model):
    reception = models.OneToOneField(Reception, unique=True, on_delete=models.CASCADE, related_name='feedback')
    mark = models.DecimalField(max_digits=2, decimal_places=1, validators=[validate_feedback_mark])

    def save(self, **kwargs):
        self.full_clean()
        super(Feedback, self).save(**kwargs)
