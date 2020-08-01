from django.db import models
from api.company.models import Company

# Create your models here.


class Master(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    age = models.DateField()
    company = models.ManyToManyField(to=Company, related_name="master_company")

    def __str__(self):
        return self.name + ' ' + self.surname