from django.db import models
from api.company.models import Company
from api.service.models import Service
from .master import Master


class WorkType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='work_types', db_index=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    duration = models.DurationField()
    price_from = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_to = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"
        unique_together = ('company', 'master', 'service')
