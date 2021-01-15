from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.master.models import WorkType
from api.service.models import Service


class WorkTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='service.name', required=True, allow_blank=False)
    duration = serializers.DurationField(required=True)

    class Meta:
        model = WorkType
        fields = ['name', 'duration']

    def validate_name(self, value):
        active_work_types = Service.objects.filter(is_active=True).values_list('name', flat=True)
        if value not in active_work_types:
            raise ValidationError({'work_types': {'name': f'Invalid work type: {value}'}})
        return value

    def validate_duration(self, value):
        try:
            datetime.strptime(value, "%H:%M:%S")
        except TypeError:
            raise ValidationError({'work_type': {
                'duration': 'Duration has wrong format. Use one of these formats instead: [DD] [HH:[MM:]]ss[.uuuuuu].'}})
