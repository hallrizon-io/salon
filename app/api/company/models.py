from datetime import datetime, date, timedelta

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


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
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

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
