from datetime import timedelta
from django.utils.formats import date_format
from rest_framework import serializers
from .models import Reception
from ..master.serializers import MasterDetailSerializer
from ..profile.serializers import ProfileDetailSerializer


class ReceptionListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    master = MasterDetailSerializer()
    client = ProfileDetailSerializer()

    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta():
        model = Reception
        fields = '__all__'

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_time(self, obj):
        return date_format(obj.time, 'DATETIME_FORMAT')


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
