from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    def __str__(self):
        return self.full_name

    class UserType(models.IntegerChoices):
        CLIENT = 1
        MASTER = 2

    user_type = models.IntegerField(choices=UserType.choices, default=UserType.CLIENT)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Profile'
