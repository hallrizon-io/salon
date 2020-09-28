from celery import shared_task
from api.profile.models import Profile


@shared_task
def create_random_profile():
    Profile.create_random_profile()
