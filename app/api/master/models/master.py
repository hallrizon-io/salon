from datetime import timedelta, datetime
from random import randrange
from django.db import models
from django.db.models import F, Avg, Count, Func
from api.company.models import Company
from api.profile.models import Profile
from api.service.models import Service


class MasterManager(models.Manager):
    def create_master(self, profile, company, work_types_data):
        master = self.create(profile=profile)
        master.company.add(company)
        for work_type_data in work_types_data:
            master.work_types.create(**work_type_data, company=company)
        return master

    def create_random_master(self):
        generate_duration = lambda: (timedelta(minutes=randrange(30, 120, 5)) + datetime.min).time()
        work_types_data = [{'service': service, 'duration': generate_duration()} for service in Service.objects.all()]

        return self.create_master(
            profile=Profile.create_random_profile(),
            company=Company.create_random_company(),
            work_types_data=work_types_data
        )


class Master(models.Model):
    company = models.ManyToManyField(to=Company, related_name='masters')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = MasterManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    @property
    def ratings(self):
        return self.receptions.values('master', 'company', 'service').annotate(
            company_name=F('company__name'),
            service_name=F('service__name'),
            rating=Func(Avg('feedback__mark'), function='ROUND', template='%(function)s(%(expressions)s, 1)'),
            receptions=Count('id')
        )

    def is_available_work_type(self, company_id, work_type_id):
        return self.work_types.get(company=company_id, work_type=work_type_id).exists()
