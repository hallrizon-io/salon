# Create your models here.
from django.db import models
from api.company.models import Company
from api.profile.models import Profile
from api.service.models import Service


class MasterManager(models.Manager):
    def create_master(self, profile, company, work_types_data):
        master = self.create(profile=profile)
        master.company.add(company)
        for work_type_data in work_types_data:
            work_type = WorkTypes(**work_type_data, master=master, company=company)
            work_type.save()
            master.work_types.add(work_type)
        return master


class Master(models.Model):
    company = models.ManyToManyField(to=Company, related_name='masters')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = MasterManager()

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    def is_available_work_type(self, company_id, work_type_id):
        return self.work_types.get(company=company_id, work_type=work_type_id).exists()


class WorkTypes(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='work_types', db_index=True, null=True)
    work_type = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    duration = models.DurationField()
    price_from = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_to = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"
        unique_together = ('company', 'master', 'work_type')
