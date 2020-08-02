from django.db import models
from api.company.models import Company
from api.master.models import Master
from api.profile.models import Profile

# Create your models here.


class Reception(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'Accepted'
        CANCELED = 'Canceled'

    description = models.CharField(max_length=255)
    time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACCEPTED)
    client = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='client')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='company')
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING, related_name='master')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Reception %d' % self.id

