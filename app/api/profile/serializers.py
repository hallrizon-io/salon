import re
from datetime import datetime
from django.utils.formats import date_format
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from main.validators import validate_contains_numbers
from .models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'email',
                  'last_login', 'is_active', 'date_joined')

    def get_birth_date(self, obj):
        return date_format(obj.birth_date, 'DATE_FORMAT') if obj.birth_date else ''

    def get_last_login(self, obj):
        return date_format(obj.last_login, 'DATETIME_FORMAT') if isinstance(obj.last_login, datetime) else ''

    def get_date_joined(self, obj):
        return date_format(obj.date_joined, 'DATETIME_FORMAT')


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'age')


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth_date', 'email', 'phone', 'password')
        extra_kwargs = {
            'first_name': {'allow_blank': False, 'required': True, 'validators': [validate_contains_numbers]},
            'last_name': {'allow_blank': False, 'required': True, 'validators': [validate_contains_numbers]},
            'email': {
                'allow_blank': False,
                'required': True,
                'min_length': 8,
                'validators': [UniqueValidator(queryset=Profile.objects.all())]
            },
            'phone': {'allow_blank': False},
            'password': {'required': True}
        }
        validators = [UniqueTogetherValidator(
            queryset=Profile.objects.all(),
            fields=('first_name', 'last_name'),
        )]

    def __init__(self, user_type, **kwargs):
        self.user_type = user_type
        super(CreateProfileSerializer, self).__init__(**kwargs)

    def validate_birth_date(self, value):
        if value >= datetime.now().date():
            raise serializers.ValidationError('Sorry, we think you\'re too young for that sh**')
        return value

    def validate_phone(self, value):
        if re.match(r'^\+\d{12}$', value) is None:
            raise serializers.ValidationError('Incorrect phone number')
        return value

    def create(self, validated_data):
        return Profile.objects.create_user(
            **validated_data, username=validated_data['email'], user_type=self.user_type
        )
