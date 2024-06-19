from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def generate_users_task(count: int):
    get_user_model().generate_users(count)
