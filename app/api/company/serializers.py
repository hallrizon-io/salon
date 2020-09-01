from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Company
from api.master.serializers import MasterDetailSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('id', 'image')


class CompanyDetailSerializer(serializers.ModelSerializer):
    masters = MasterDetailSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'address', 'opening_hours', 'closing_hours')

    def create(self, validated_data):
        enter_code = get_random_string(length=5).lower()
        return Company.objects.create(**validated_data, enter_code=enter_code)
