from django.db import models
from api.company.models import Company
from django.contrib import admin


# Create your models here.
from api.profile.models import Profile


class WorkTypes(models.Model):
    name = models.CharField(max_length=30, unique=True)
    duration = models.DurationField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"


class WorkTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration')
    list_display_links = ('name',)


class MasterManager(models.Manager):
    def create_master(self, profile, company, work_types):
        master = self.create(profile=profile)
        master.company.add(company)
        master.work_types.add(*work_types)
        return master


class Master(models.Model):
    company = models.ManyToManyField(to=Company, related_name='masters')
    work_types = models.ManyToManyField(to=WorkTypes)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = MasterManager()

    def __str__(self):
        return self.profile.first_name + ' ' + self.profile.last_name

    def is_available_work_type(self, work_type_id):
        return self.work_types.filter(pk=work_type_id).exists()
