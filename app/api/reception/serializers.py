from datetime import timedelta, datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import Reception
from api.profile.serializers import ProfileDetailSerializer
from api.company.models import Company
from api.master.models.master import Master
from api.profile.models import Profile
from api.service.models import Service


class MasterField(serializers.DictField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'first_name': value.profile.first_name,
            'last_name': value.profile.last_name,
            'age': value.profile.age,
        }


class CompanyField(serializers.DictField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'address': value.address,
            'opening_hours': value.opening_hours,
            'closing_hours': value.closing_hours
        }


class ReceptionListSerializer(serializers.ModelSerializer):
    company = CompanyField()
    master = MasterField()
    client = ProfileDetailSerializer()
    service = serializers.SlugRelatedField(slug_field='name', read_only=True)

    updated = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d %H:%M:%S')
    created = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S')
    time_from = serializers.CharField(source='start_datetime')
    time_to = serializers.CharField(source='end_datetime')

    class Meta:
        model = Reception
        exclude = ('start_timestamp', 'end_timestamp', 'created_at', 'updated_at')


class CreateReceptionSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Reception
        fields = ('company_id', 'master_id', 'client_id', 'service_id', 'datetime')

    def validate(self, attrs):
        request = self.initial_data
        expected_int_value = "Expected a positive integer value"

        for field in self.fields.keys():
            if field not in request.keys():
                raise ValidationError({field: 'This field is required.'})
            elif not request[field]:
                raise ValidationError({field: 'This field may not be blank.'})

        try:
            client = Profile.objects.get(pk=request.get('client_id'))
        except (ValueError, ObjectDoesNotExist) as exception:
            message = "The current client doesn't exist"
            if isinstance(exception, ValueError):
                message = expected_int_value
            raise ValidationError({'client_id': message})

        try:
            company = Company.objects.get(pk=request.get('company_id'))
        except (ValueError, ObjectDoesNotExist) as exception:
            message = "The current company doesn't exist"
            if isinstance(exception, ValueError):
                message = expected_int_value
            raise ValidationError({'company_id': message})

        try:
            master = Master.objects.get(pk=request.get('master_id'))
        except (ValueError, ObjectDoesNotExist) as exception:
            message = "The current master doesn't exist"
            if isinstance(exception, ValueError):
                message = expected_int_value
            raise ValidationError({'master_id': message})

        if not company.is_employee(master.id):
            raise ValidationError({'other_reason': "The current master doesn't work for this company"})

        try:
            service = Service.objects.get(pk=request.get('service_id'))
        except (ValueError, ObjectDoesNotExist) as exception:
            message = "The system doesn't support current service"
            if isinstance(exception, ValueError):
                message = expected_int_value
            raise ValidationError({'service_id': message})

        try:
            work_type = master.work_types.get(company=company.id, service=service.id)
        except ObjectDoesNotExist:
            raise ValidationError({'service_id': "The current service doesn't support by this master"})

        try:
            start_timestamp = int(datetime.fromisoformat(request.get('datetime')).timestamp())
        except (ValueError, TypeError):
            raise ValidationError({'datetime': "Date has wrong format. Use one of these formats instead: YYYY-MM-DD HH:MM."})

        salt = timedelta(minutes=14, seconds=59)
        end_timestamp = start_timestamp + work_type.duration.seconds + salt.seconds

        if not company.is_working_hours(start_timestamp, end_timestamp):
            raise ValidationError({'other_reason': 'Sorry, come to us when we are opening again'})

        if not Reception.objects.is_available_booking(start_timestamp, end_timestamp, master.id):
            raise ValidationError({'other_reason': 'Sorry, your hours are already booked'})

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
    time_from = serializers.CharField(source='start_datetime')
    time_to = serializers.CharField(source='end_datetime')
    work_type = serializers.CharField(source='service.name')

    class Meta:
        model = Reception
        fields = ('time_from', 'time_to', 'work_type', 'status')
