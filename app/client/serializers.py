from rest_framework import serializers
from .models import Client


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'email',
                 'last_login', 'is_active', 'date_joined')
