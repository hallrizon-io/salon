from django.db import models
from api.company.models import Company
from api.profile.models import Profile


class MasterManager(models.Manager):
    def create_master(self, profile, company, work_types_data):
        master = self.create(profile=profile)
        master.company.add(company)
        for work_type_data in work_types_data:
            master.work_types.create(**work_type_data, company=company)
        return master


class Master(models.Model):
    company = models.ManyToManyField(to=Company, related_name='masters')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = MasterManager()

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    def is_available_work_type(self, company_id, work_type_id):
        return self.work_types.get(company=company_id, work_type=work_type_id).exists()
