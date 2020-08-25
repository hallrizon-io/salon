from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    def __str__(self):
        return f'{self.full_name} ({self.client_type})'

    class UserType(models.IntegerChoices):
        CLIENT = 1
        MASTER = 2

    user_type = models.IntegerField(choices=UserType.choices, default=UserType.CLIENT)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        from datetime import date
        born = self.birth_date
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def client_type(self):
        return {1: "Client", 2: "Master"}[self.user_type]

    class Meta:
        verbose_name = 'Profile'
