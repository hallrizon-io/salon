from django.db import models
from api.company.models import Company
from api.master.models import Master
from api.profile.models import Profile

# Create your models here.


class Reception(models.Model):
    description = models.CharField(max_length=255)
    time = models.DateTimeField()
    status = models.CharField(max_length=20)
    client = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Order %d' % self.id