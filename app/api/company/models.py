from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string


class Company(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to="image/companies/", blank=True)
    enter_code = models.CharField(max_length=5, unique=True, null=True, validators=[
        RegexValidator(
            regex='^[a-z0-9]{5}$',
            message='Incorrect enter_code, available symbols (a-z, 0-9)'
        ),
    ])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.enter_code = get_random_string(length=5).lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

