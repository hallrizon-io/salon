from datetime import timedelta, datetime

from django.shortcuts import get_object_or_404
from django.utils.formats import date_format
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reception
from api.master.serializers import MasterDetailSerializer
from api.profile.serializers import ProfileDetailSerializer
from ..company.models import Company
from ..master.models import Master, WorkTypes
from ..profile.models import Profile


class ReceptionListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    master = MasterDetailSerializer()
    client = ProfileDetailSerializer()

    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()
    end_datetime = serializers.SerializerMethodField()

    class Meta():
        model = Reception
        exclude = ('start_timestamp', 'end_timestamp')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_start_datetime(self, obj):
        return obj.start_datetime

    def get_end_datetime(self, obj):
        return obj.end_datetime


class CreateReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = ('company_id', 'master_id', 'client_id')

    def validate(self, attrs):
        request = self.initial_data

        company = get_object_or_404(Company, pk=request.get('company_id'))
        service = get_object_or_404(WorkTypes, pk=request.get('service_id'))
        client = get_object_or_404(Profile, pk=request.get('client_id'))
        master = get_object_or_404(Master, pk=request.get('master_id'))

        start_timestamp = int(datetime.fromisoformat(request.get('datetime')).timestamp())
        salt = timedelta(minutes=14, seconds=59)
        end_timestamp = start_timestamp + service.duration.seconds + salt.seconds

        if not company.is_working_hours(start_timestamp, end_timestamp):
            raise ValidationError('Sorry, come to us when we are opening again')

        if not company.is_employee(master.id):
            raise ValidationError('The current master doesn\'t work for this company')

        if not master.is_available_work_type(service.id):
            raise ValidationError('The current work type doesn\'t support by this master')

        if not Reception.objects.is_available_booking(start_timestamp, end_timestamp, master.id):
            raise ValidationError('Sorry, your hours are already taken')

        validated_data = {
            'description': request.get('description', ''),
            'company': company,
            'service': service,
            'client': client,
            'master': master,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'status': Reception.Status.BOOKED
        }

        return validated_data

    def create(self, validated_data):
        return Reception.objects.create_reception(validated_data)


class BookedHoursSerializer(serializers.ModelSerializer):
    time_from = serializers.SerializerMethodField()
    time_to = serializers.SerializerMethodField()

    class Meta:
        model = Reception
        fields = ('time_from', 'time_to')

    def get_time_from(self, obj):
        return date_format(obj.time, 'DATETIME_FORMAT')

    def get_time_to(self, obj):
        return date_format(obj.time + timedelta(hours=1), 'DATETIME_FORMAT')
