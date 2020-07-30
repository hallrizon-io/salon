from rest_framework import serializers
from .models import Company


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('id', 'image')