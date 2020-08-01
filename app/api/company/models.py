from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to="companies/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

