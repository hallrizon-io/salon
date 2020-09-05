from datetime import datetime, date

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    image = models.ImageField(upload_to="image/companies/", blank=True)
    enter_code = models.CharField(max_length=5, unique=True, null=True, validators=[
        RegexValidator(
            regex='^[a-z0-9]{5}$',
            message='Incorrect enter_code, available symbols (a-z, 0-9)'
        ),
    ])
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    @staticmethod
    def is_company_exist(company_id, raise_exception=False):
        is_exist = False
        try:
            is_exist = Company.objects.filter(pk=company_id, is_active=True).exists()
        except ObjectDoesNotExist:
            if raise_exception:
                raise ValidationError({'company_id': "The current company doesn't exist"})
        return is_exist

    def is_working_hours(self, start_timestamp, end_timestamp):
        reception_day = date.fromtimestamp(start_timestamp)
        opening_timestamp = datetime.combine(reception_day, self.opening_hours).timestamp()
        closing_timestamp = datetime.combine(reception_day, self.closing_hours).timestamp()
        if opening_timestamp > start_timestamp or closing_timestamp < end_timestamp:
            return False
        else:
            return True

    def is_employee(self, master_id):
        return self.masters.filter(pk=master_id).exists()
