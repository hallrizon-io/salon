from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Company
from api.master.serializers import MasterDetailSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'rating', 'opening_hours',
                  'closing_hours', 'image', 'enter_code', 'is_active')


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
