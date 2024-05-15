from django.contrib.auth import get_user_model

from clients.models import ClientProfile, Job
from core.models import Skill


def sample_client_profile(user_email: str, location: str, **params):
    test_user = get_user_model()(email=user_email)
    test_user.set_password("123456789")
    test_user.save()
    default = {
        "user": test_user,
        "company": "Google Inc.",
        "image": None,
    }
    default.update(params)
    return ClientProfile.objects.create(
        location=location,
        **default,
    )


def sample_job(user_email: str, title: str, description: str, hourly_rate: float, estimated_end_date: str, **params):
    client_profile = sample_client_profile(
        user_email=user_email,
        location="San Francisco, CA, USA",
    )
    my_skill = Skill.objects.create(
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
