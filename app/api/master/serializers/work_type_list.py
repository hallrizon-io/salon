from rest_framework import serializers
from api.master.models import WorkType


class WorkTypesListSerializer(serializers.ModelSerializer):
    work_type_name = serializers.CharField(source='service.name')
    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = WorkType
        exclude = ('master',)
