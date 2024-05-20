from django.contrib.auth import get_user_model

from clients.models import ClientProfile, Job
from core.models import Skill
from core.utils.samples_for_location import (sample_city, sample_country,
                                             sample_state)


def sample_client_profile(user_email: str, **params):
    test_user = get_user_model()(email=user_email)
    test_user.set_password("123456789")
    test_user.save()
    country_instance = sample_country("USA")
    state_instance = sample_state("USA", "CA")
    city_instance = sample_city("USA", "CA", "San Francisco")
    default = {
        "user": test_user,
        "company": "Google Inc.",
        "country": country_instance,
        "state": state_instance,
        "city": city_instance,
        "image": None,
    }
    default.update(params)
    return ClientProfile.objects.create(
        **default,
    )


def sample_job(user_email: str, title: str, description: str, hourly_rate: float, estimated_end_date: str, **params):
    client_profile = sample_client_profile(
        user_email=user_email,
    )
    my_skill, created = Skill.objects.get_or_create(
        title="Python",
    )
    default = {
        "documentation": None,
        "client_profile_id": client_profile,
    }
    default.update(params)
    job = Job.objects.create(
        title=title,
        description=description,
        hourly_rate=hourly_rate,
        estimated_end_date=estimated_end_date,
        **default,
    )
    job.skill.add(my_skill)
    return job
