from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Master, WorkTypes
from api.profile.serializers import ProfileDetailSerializer
from api.service.models import Service


class WorkTypesListSerializer(serializers.ModelSerializer):
    work_type_name = serializers.CharField(source='work_type.name')
    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = WorkTypes
        exclude = ('master',)


class WorkTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    duration = serializers.DurationField()

    class Meta:
        model = WorkTypes
        fields = ['name', 'duration']

    def validate_name(self, value):
        active_work_types = Service.objects.filter(is_active=True).values_list('name', flat=True)
        if value not in active_work_types:
            raise ValidationError({'name': f'Invalid work type: {value}'})
        return value


class CreateWorkTypesSerializer(serializers.Serializer):
    work_types = WorkTypeSerializer(many=True)

    def create(self, validated_data):
        work_types = []

        for ordered_dict in validated_data.get('work_types'):
            work_type, duration, *other = ordered_dict.values()
            work_types.append({'work_type': Service.objects.get(name=work_type), 'duration': duration})

        return work_types


class MasterListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    work_types = WorkTypesListSerializer(many=True)
    profile = ProfileDetailSerializer()

    class Meta:
        model = Master
        fields = '__all__'


class MasterDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()
    work_types = WorkTypesListSerializer(many=True)

    class Meta:
        model = Master
        fields = ('id', 'profile', 'work_types')
