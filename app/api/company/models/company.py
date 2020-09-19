from datetime import datetime, date, time
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Window, Avg, F
from django.utils.crypto import get_random_string
from faker import Faker
from rest_framework.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField(max_length=50)
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
        is_exist = Company.objects.filter(pk=company_id, is_active=True).exists()
        if raise_exception and not is_exist:
            raise ValidationError({'company_id': "The current company doesn't exist"})
        return is_exist

    @staticmethod
    def all_with_calculated_rating(order=None):
        companies = Company.objects.annotate(
            rating=Window(
                expression=Avg('feedbacks__mark'),
                partition_by=[F('id')]
            )
        ).distinct()

        if order:
            sort_by_rating = lambda x: F('rating').asc(nulls_last=True) if x == 'asc' else F('rating').desc(
                nulls_last=True)
            companies = companies.order_by(sort_by_rating(order))

        return companies

    @classmethod
    def create_random_company(cls):
        faker = Faker()
        return cls.objects.create(
            name=faker.company(),
            address=faker.street_address(),
            opening_hours=time(10, 0),
            closing_hours=time(18, 0),
            enter_code=get_random_string(length=5).lower()
        )

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
