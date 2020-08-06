from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    class UserType(models.IntegerChoices):
        CLIENT = 1
        MASTER = 2

    user_type = models.IntegerField(choices=UserType.choices, default=UserType.CLIENT)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else ' '

    class Meta:
        verbose_name = 'Profile'
