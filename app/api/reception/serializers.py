from datetime import timedelta, datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import Reception
from api.master.serializers import MasterDetailSerializer
from api.profile.serializers import ProfileDetailSerializer
from api.company.models import Company
from api.master.models.master import Master
from api.profile.models import Profile


class ReceptionListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    master = MasterDetailSerializer()
    client = ProfileDetailSerializer()
    service = serializers.SlugRelatedField(slug_field='name', read_only=True)

    updated = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d %H:%M:%S')
    created = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S')
    time_from = serializers.CharField(source='start_datetime')
    time_to = serializers.CharField(source='end_datetime')

    class Meta():
        model = Reception
        exclude = ('start_timestamp', 'end_timestamp', 'created_at', 'updated_at')


class CreateReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = ('company_id', 'master_id', 'client_id', 'service_id')

    def validate(self, attrs):
        request = self.initial_data

        try:
            client = Profile.objects.get(pk=request.get('client_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'client_id': "The current client doesn't exist"})

        try:
            company = Company.objects.get(pk=request.get('company_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'company_id': "The current company doesn't exist"})

        try:
            master = Master.objects.get(pk=request.get('master_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'master_id': "The current master doesn't exist"})

        try:
            service = master.work_types.get(company=company.id, work_type=request.get('service_id'))
        except ObjectDoesNotExist:
            raise ValidationError({'service_id': "The current service doesn't support by this master"})

        start_timestamp = int(datetime.fromisoformat(request.get('datetime')).timestamp())
        salt = timedelta(minutes=14, seconds=59)
        end_timestamp = start_timestamp + service.duration.seconds + salt.seconds

        if not company.is_working_hours(start_timestamp, end_timestamp):
            raise ValidationError({'other_reason': 'Sorry, come to us when we are opening again'})

        if not company.is_employee(master.id):
            raise ValidationError({'other_reason': "The current master doesn't work for this company"})

        if not Reception.objects.is_available_booking(start_timestamp, end_timestamp, master.id):
            raise ValidationError({'other_reason': 'Sorry, your hours are already taken'})

        validated_data = {
            'description': request.get('description', ''),
            'company': company,
            'service': service.work_type,
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
    time_from = serializers.CharField(source='start_datetime')
    time_to = serializers.CharField(source='end_datetime')
    work_type = serializers.CharField(source='service.name')

    class Meta:
        model = Reception
        fields = ('time_from', 'time_to', 'work_type', 'status')
