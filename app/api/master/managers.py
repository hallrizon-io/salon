from django.db import transaction
from rest_framework.generics import get_object_or_404
from api.company.models import Company
from api.company.serializers import CreateCompanySerializer
from api.master.models import Master
from api.master.serializers import CreateWorkTypesSerializer
from api.profile.models import Profile
from api.profile.serializers import CreateProfileSerializer


class MasterViewManager:
    def __init__(self, request):
        self.data = request.data

    def processing(self):
        profile_serializer = CreateProfileSerializer(
            user_type=Profile.UserType.MASTER, data=self.data.get('profile')
        )
        work_types_serializer = CreateWorkTypesSerializer(data={'work_types': self.data.get('work_types')})
        company_serializer = CreateCompanySerializer(data=self.data.get('company'))

        profile_serializer.is_valid(raise_exception=True)
        work_types_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            if self.data.get('new_company', False):
                company_serializer.is_valid(raise_exception=True)
                company = company_serializer.save()
            else:
                company = get_object_or_404(
                    Company, enter_code=self.data.get('company').get('enter_code')
                )

            master = Master.objects.create_master(
                profile=profile_serializer.save(),
                company=company,
                work_types_data=work_types_serializer.save()
            )
        return master
