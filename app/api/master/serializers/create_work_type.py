from datetime import timedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.service.models import Service
from main.validators import validate_contains_numbers


class CreateWorkTypesSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, validators=[validate_contains_numbers])
    duration = serializers.DurationField(required=True, min_value=timedelta(minutes=15))

    def validate_name(self, value):
        if not Service.objects.filter(name=value).exists():
            raise ValidationError("The system doesn't support current service")
        return value
