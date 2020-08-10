from django.db import models
from api.company.models import Company

# Create your models here.
from api.profile.models import Profile


class WorkTypes(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"


class MasterManager(models.Manager):
    def create_master(self, profile, company, work_types):
        master = self.create(profile=profile)
        master.company.add(company)
        master.work_types.add(*work_types)
        return master


class Master(models.Model):
    def __str__(self):
        return self.profile.first_name + ' ' + self.profile.last_name

    company = models.ManyToManyField(to=Company, related_name='masters')
    work_types = models.ManyToManyField(to=WorkTypes)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = MasterManager()
