from django.contrib.auth import get_user_model

from clients.models import Job
from clients.utils.samples import sample_client_profile, sample_job
from core.models import Skill
from core.utils.samples_for_location import (sample_city, sample_country,
                                             sample_state)
from freelancers.models import (FreelancerProfile, Proposal,
                                ReviewAboutFreelancer)


def sample_freelancer_profile(user_email: str, position: str, hourly_rate: float, sex: int, **params):
    test_user = get_user_model()(email=user_email)
    test_user.set_password("123456789")
    test_user.save()
    my_skill = Skill.objects.create(
        title="SQL",
    )
    country_instance = sample_country("USA")
    state_instance = sample_state("USA", "CA")
    city_instance = sample_city("USA", "CA", "San Jose")

    default = {
        "user": test_user,
        "description": "Python developer in test description",
        "birth_date": "1965-03-07",
        "photo": None,
        "country": country_instance,
        "state": state_instance,
        "city": city_instance,
        "resume": None,
    }
    default.update(params)
    freelancer_profile = FreelancerProfile.objects.create(
        position=position,
        hourly_rate=hourly_rate,
        sex=sex,
        **default,
    )
    freelancer_profile.skill.add(my_skill)
    return freelancer_profile


def sample_proposal(freelancer_email: str, client_email: str, hourly_rate: float, estimated_end_date: str, **params):
    freelancer_profile = sample_freelancer_profile(
        user_email=freelancer_email,
        position="Python developer",
        hourly_rate=42.00,
        sex=0,
    )
    job = sample_job(
        user_email=client_email,
        title="Python developer",
        description="Creating web application",
        hourly_rate=35.00,
        estimated_end_date="2024-09-18",
    )
    default = {
        "freelancer_profile_id": freelancer_profile,
        "job_id": job,
        "title": "Python developer in test description",
        "documentation": None,
    }
    default.update(params)
    return Proposal.objects.create(
        hourly_rate=hourly_rate,
        estimated_end_date=estimated_end_date,
        **default,
    )


def sample_review_about_freelancer(freelancer_email: str, client_email: str, rating: float, **params):
    freelancer_profile = sample_freelancer_profile(
        user_email=freelancer_email,
        position="Python developer",
        hourly_rate=42.00,
        sex=0,
    )
    my_skill = Skill.objects.create(
        title="SQL",
    )
    client_profile = sample_client_profile(
        user_email=client_email,
    )
    job = Job.objects.create(
        title="Python developer",
        description="Creating web application",
        hourly_rate=35.00,
        estimated_end_date="2024-09-18",
        client_profile_id=client_profile,
    )
    job.skill.add(my_skill)
    default = {
        "review": "some review",
        "from_client": client_profile,
        "to_freelancer": freelancer_profile,
        "job": job,
    }
    default.update(params)
    return ReviewAboutFreelancer(
        rating=rating,
        **default,
    )
