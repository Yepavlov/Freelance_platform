from datetime import date
from decimal import Decimal, ROUND_DOWN

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from clients.models import Job
from core.models import BaseModel, Country, State, City, Skill
from freelancers.utils.utils import documentation_upload
from freelancers.utils.validators import (
    birth_date_validator,
    extension_validator,
    rating_validator,
    validate_file_size,
)


class SexChoices(models.IntegerChoices):
    MALE = 0, "Male"
    FEMALE = 1, "Female"
    NO_ANSWER = 2, "I don't want to answer "


class FreelancerProfile(models.Model):
    position = models.CharField(
        _("position"),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        _("date of birth"),
        blank=True,
        null=True,
        validators=[birth_date_validator],
    )
    hourly_rate = models.DecimalField(
        _("hourly rate"),
        max_digits=5,
        decimal_places=2,
    )
    country = models.ForeignKey(
        "core.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    state = models.ForeignKey(
        "core.State", on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.ForeignKey(
        "core.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    photo = models.ImageField(
        _("photo"),
        upload_to="images/freelancer_profile_photo/",
        blank=True,
        null=True,
        validators=[validate_file_size],
        default="images/default.jpg",
    )
    sex = models.PositiveSmallIntegerField(
        _("gender"),
        choices=SexChoices.choices,
        default=SexChoices.NO_ANSWER,
    )
    resume = models.FileField(
        _("resume"),
        upload_to="freelancers_resume/",
        blank=True,
        null=True,
        validators=[extension_validator, validate_file_size],
    )
    skill = models.ManyToManyField(
        "core.Skill",
        related_name="freelancer_profiles",
    )
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="freelancer_profiles",
    )

    class Meta:
        verbose_name = "Freelancer Profile"
        verbose_name_plural = "Freelancer Profiles"

    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} {self.position} ({self.id})"
        )

    @classmethod
    def generate_freelancers_profile(cls, count: int) -> None:
        faker = Faker()
        users = list(
            get_user_model()
            .objects.filter(user_type=0)
            .exclude(freelancer_profiles__isnull=False)
            .values_list("uuid", flat=True)
        )
        if len(users) < count:
            raise ValueError(
                "Not enough users available to create the requested number of Freelancer Profiles"
            )
        cities = list(City.objects.all())
        skills = list(Skill.objects.all())

        for i in range(count):
            user_uuid = faker.random.choice(users)
            users.remove(user_uuid)
            city = faker.random.choice(cities)
            state = city.state
            country = state.country
            skill_subset = faker.random.sample(
                skills, faker.random.randint(1, len(skills))
            )
            hourly_rate = faker.pyfloat(left_digits=3, right_digits=2, positive=True)
            hourly_rate = Decimal(hourly_rate).quantize(
                Decimal("0.01"), rounding=ROUND_DOWN
            )
            freelancer_profile = FreelancerProfile(
                position=" ".join(faker.words(nb=2)),
                description=faker.text(max_nb_chars=200),
                birth_date=faker.date_of_birth(minimum_age=14),
                hourly_rate=hourly_rate,
                country=country,
                state=state,
                city=city,
                user_id=user_uuid,
            )

            freelancer_profile.save()

            freelancer_profile.skill.add(*skill_subset)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Proposal(BaseModel):
    title = models.CharField(_("title"), max_length=255, null=True, blank=True)
    hourly_rate = models.DecimalField(
        _("hourly rate"),
        max_digits=5,
        decimal_places=2,
    )
    estimated_end_date = models.DateField(_("estimated end date"))
    documentation = models.FileField(
        _("documentation"),
        upload_to=documentation_upload,
        blank=True,
        null=True,
    )
    selected = models.BooleanField(_("selected"), default=False)
    freelancer_profile_id = models.ForeignKey(
        "freelancers.FreelancerProfile",
        on_delete=models.CASCADE,
        related_name="proposals",
    )
    job_id = models.ForeignKey(
        "clients.Job",
        on_delete=models.CASCADE,
        related_name="proposals",
    )

    def __str__(self):
        return f"{self.title}, {self.freelancer_profile_id} {self.job_id}"

    @classmethod
    def generate_proposals(cls, count: int) -> None:
        faker = Faker()
        freelancers_profile = list(FreelancerProfile.objects.all())
        jobs = list(Job.objects.all())
        proposal_list = []
        for i in range(count):
            job = faker.random.choice(jobs)
            freelancer_profile = faker.random.choice(freelancers_profile)
            hourly_rate = faker.pyfloat(left_digits=3, right_digits=2, positive=True)
            hourly_rate = Decimal(hourly_rate).quantize(
                Decimal("0.01"), rounding=ROUND_DOWN
            )
            proposal = Proposal(
                title=faker.word(),
                hourly_rate=hourly_rate,
                estimated_end_date=faker.date_this_year(after_today=True),
                freelancer_profile_id=freelancer_profile,
                job_id=job,
            )
            proposal_list.append(proposal)
        Proposal.objects.bulk_create(proposal_list)


class ReviewAboutFreelancer(BaseModel):
    review = models.TextField(
        _("review"),
        max_length=1000,
        blank=True,
        null=True,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[rating_validator],
    )
    from_client = models.ForeignKey(
        "clients.ClientProfile",
        on_delete=models.CASCADE,
        related_name="sent_reviews",
    )
    to_freelancer = models.ForeignKey(
        "freelancers.FreelancerProfile",
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )
    job = models.ForeignKey(
        "clients.Job",
        related_name="freelancer_reviews",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Review About Freelancer"
        verbose_name_plural = "Reviews About Freelancers"

    def __str__(self):
        return f"{self.rating} {self.from_client} -> {self.to_freelancer} ({self.job.title})"
