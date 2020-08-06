from rest_framework import serializers
from .models import Company
from ..master.serializers import MasterDetailSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('id', 'image')


class CompanyDetailSerializer(serializers.ModelSerializer):
    masters = MasterDetailSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'