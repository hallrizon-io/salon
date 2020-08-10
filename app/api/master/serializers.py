from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Master, WorkTypes
from ..profile.serializers import ProfileDetailSerializer


class MasterListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    work_types = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    profile = ProfileDetailSerializer()

    class Meta:
        model = Master
        fields = '__all__'


class MasterDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = Master
        fields = ('id', 'profile')


class WorkTypeListSerializer(serializers.ModelSerializer):
    work_types = serializers.ListField(child=serializers.CharField(max_length=20))

    class Meta:
        model = WorkTypes
        fields = ('work_types',)

    def validate_work_types(self, list):
        for work_type in list:
            if not WorkTypes.objects.filter(name=work_type).exists():
                raise ValidationError('Invalid work type: ' + work_type)
        return list

    def create(self, validated_data):
        return [WorkTypes.objects.get(name=work_type) for work_type in dict(validated_data).get('work_types')]
