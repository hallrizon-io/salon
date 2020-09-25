from celery import shared_task
from api.reception.models import Reception


@shared_task
def update_completed_receptions():
    Reception.objects.update_completed_receptions()
