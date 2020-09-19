# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils.formats import date_format
from rest_framework.exceptions import ValidationError
from faker import Faker


class Profile(AbstractUser):
    def __str__(self):
        return f'{self.full_name}'

    class UserType(models.IntegerChoices):
        CLIENT = 1
        MASTER = 2

    user_type = models.IntegerField(choices=UserType.choices, default=UserType.CLIENT)
    birth_date = models.DateField(null=True)
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

    @staticmethod
    def is_profile_exist(client_id, raise_exception=False):
        is_exist = Profile.objects.filter(pk=client_id, is_active=True).exists()
        if raise_exception and not is_exist:
            raise ValidationError({'client_id': "The current client doesn't exist"})
        return is_exist

    @classmethod
    def create_random_profile(cls):
        faker = Faker()
        profile = faker.profile(fields=('name', 'birthdate', ''))
        first_name, last_name, *other = profile['name'].split(' ', 2)
        email = faker.ascii_safe_email()
        return cls.objects.create_user(
            username=email,
            password=get_random_string(length=12).lower(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            birth_date=date_format(profile['birthdate'], 'DATE_FORMAT')
        )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Profile'
