from rest_framework import serializers
from .models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'email',
                 'last_login', 'is_active', 'date_joined')


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name')