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


class CreateCompanySerializer(serializers.ModelSerializer):
    new_company = False

    class Meta:
        model = Company
        fields = ('name', 'address', 'enter_code')
        extra_kwargs = {
            'enter_code': {
                'allow_blank': False,
                'min_length': 5,
                'max_length': 5
            },
        }

    def create(self, validated_data):
        return Company.objects.create(**validated_data)