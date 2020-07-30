from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Client(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Client'