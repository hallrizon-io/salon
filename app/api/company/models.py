from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


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

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

