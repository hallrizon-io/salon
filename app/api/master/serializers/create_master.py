from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.company.models import Company
from api.company.serializers import CreateCompanySerializer
from api.master.models import Master
from api.master.serializers.create_work_type import CreateWorkTypesSerializer
from api.profile.models import Profile
from api.profile.serializers import CreateProfileSerializer
from api.service.models import Service


class CreateMasterSerializer(serializers.ModelSerializer):
    profile = CreateProfileSerializer(user_type=Profile.UserType.MASTER)
    company = CreateCompanySerializer()
    work_types = CreateWorkTypesSerializer(many=True)
    new_company = serializers.BooleanField()

    class Meta:
        model = Master
        fields = ('profile', 'company', 'work_types', 'new_company')

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=False)
        if 'work_types' in self._errors:
            self._errors['work_types'] = [*filter(None, self._errors['work_types'])]

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return is_valid

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        company_data = validated_data.pop('company')
        is_new_company = company_data.pop('new_company')
        work_types_data = []

        profile = Profile.objects.create_user(
            **profile_data, username=profile_data['email'], user_type=Profile.UserType.MASTER
        )

        if is_new_company:
            company = Company.objects.create(**company_data, enter_code=get_random_string(length=5).lower())
        else:
            company = Company.objects.get(enter_code=self.context.get('enter_code'))

        for ordered_dict in validated_data.get('work_types'):
            work_type, duration, *other = ordered_dict.values()
            work_types_data.append({'service': Service.objects.get(name=work_type), 'duration': duration})

        return Master.objects.create_master(profile, company, work_types_data)
