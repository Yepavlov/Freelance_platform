from celery import shared_task
from django.contrib.auth import get_user_model

from clients.models import ClientProfile
from core.models import City, Country, Skill, State
from freelancers.models import FreelancerProfile


@shared_task
def generate_users_task(count: int):
    get_user_model().generate_users(count)


@shared_task
def generate_freelancer_profile_task(count: int):
    FreelancerProfile.generate_freelancers_profile(count)


@shared_task
def generate_client_profile_task(count: int):
    ClientProfile.generate_clients_profile(count)


@shared_task
def generate_cities_task(count: int):
    City.generate_cities(count)


@shared_task
def generate_states_task(count: int):
    State.generate_states(count)


@shared_task
def generate_countries_task(count: int):
    Country.generate_countries(count)


@shared_task
def generate_skills_task(count: int):
    Skill.generate_skills(count)
