# Create your models here.
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='active')

    def __str__(self):
        return self.name