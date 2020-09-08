from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils.formats import date_format
from rest_framework.exceptions import ValidationError
from api.company.models import Company
from api.master.models import Master
from api.profile.models import Profile
from api.service.models import Service


class ReceptionManager(models.Manager):
    def create_reception(self, data):
        return self.create(**data)

    def is_available_booking(self, start_timestamp, end_timestamp, master_id):
        return not self.filter(
            Q(master_id=master_id),
            Q(status__in=(Reception.Status.ACCEPTED, Reception.Status.BOOKED)),
            Q(start_timestamp__gte=start_timestamp) & Q(start_timestamp__lt=end_timestamp) |
            Q(end_timestamp__gte=start_timestamp) & Q(end_timestamp__lt=end_timestamp)
        ).exists()

    @staticmethod
    def is_reception_exist(reception_id, raise_exception=True):
        is_exist = False
        try:
            is_exist = Reception.objects.filter(pk=reception_id, status=Reception.Status.ACCEPTED).exists()
        except ObjectDoesNotExist:
            if raise_exception:
                raise ValidationError({'reception_id': "The current reception doesn't exist"})
        return is_exist


class Reception(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'Accepted'
        CANCELED = 'Canceled'
        BOOKED = 'Booked'

    description = models.CharField(max_length=255, blank=True)
    start_timestamp = models.PositiveBigIntegerField(db_index=True, null=True)
    end_timestamp = models.PositiveBigIntegerField(null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name='receptions')
    client = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='receptions')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='receptions')
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING, related_name='receptions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReceptionManager()

    def __str__(self):
        return f'Reception {self.id}'

    def start_datetime(self):
        return date_format(datetime.fromtimestamp(self.start_timestamp), 'DATETIME_FORMAT')

    start_datetime.admin_order_field = '-start_timestamp'
    start_datetime = property(start_datetime)

    @property
    def end_datetime(self):
        return date_format(datetime.fromtimestamp(self.end_timestamp), 'DATETIME_FORMAT')