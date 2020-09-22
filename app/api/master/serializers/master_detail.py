from rest_framework import serializers
from api.master.models import Master
from api.master.serializers.work_type_list import WorkTypesListSerializer
from api.profile.serializers import ProfileDetailSerializer


class MasterDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()
    work_types = WorkTypesListSerializer(many=True)

    class Meta:
        model = Master
        fields = ('id', 'profile', 'work_types')
