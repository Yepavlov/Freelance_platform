from decimal import ROUND_DOWN, Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from clients.utils.utils import documentation_upload
from clients.utils.validators import rating_validator, validate_file_size
from core.models import BaseModel, City, Country, Skill, State


class ClientProfile(models.Model):
    company = models.CharField(
        _("company name"),
        blank=True,
        null=True,
        max_length=255,
    )
    country = models.ForeignKey("core.Country", on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey("core.State", on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey("core.City", on_delete=models.SET_NULL, null=True, blank=True)
    company_description = models.CharField(
        _("company description"),
        blank=True,
        null=True,
        max_length=255,
    )
    user = models.OneToOneField(
        to=get_user_model(),
        related_name="client_profiles",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        _("image"),
        upload_to="images/client_profile_images/",
        blank=True,
        null=True,
        validators=[validate_file_size],
        default="images/default.jpg",
    )

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"

    def __str__(self):
        return f"{self.company} {self.user.first_name} {self.user.last_name} {self.id}"

    @classmethod
    def generate_clients_profile(cls, count: int) -> None:
        faker = Faker()
        users = list(
            get_user_model()
            .objects.filter(user_type=1)
            .exclude(client_profiles__isnull=False)
            .values_list("uuid", flat=True)
        )
        if len(users) < count:
            raise ValueError("Not enough users available to create the requested number of Client Profiles")
        cities = list(City.objects.all())
        client_profile_list = []
        for i in range(count):
            user_uuid = faker.random.choice(users)
            users.remove(user_uuid)
            city = faker.random.choice(cities)
            state = city.state
            country = state.country
            client_profile = ClientProfile(
                company=faker.company(),
                city=city,
                state=state,
                country=country,
                company_description=faker.text(max_nb_chars=200),
                user_id=user_uuid,
            )

            client_profile_list.append(client_profile)

        ClientProfile.objects.bulk_create(client_profile_list)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Job(BaseModel):
    title = models.CharField(
        _("job title"),
        max_length=255,
    )
    description = models.TextField(
        _("job description"),
        max_length=1000,
    )
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
    is_concluded = models.BooleanField(
        _("is concluded"),
        default=False,
    )
    skill = models.ManyToManyField(
        "core.Skill",
        "jobs",
    )
    client_profile_id = models.ForeignKey(
        "clients.ClientProfile",
        related_name="jobs",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.title}, {self.client_profile_id}"

    @classmethod
    def generate_jobs(cls, count: int) -> None:
        faker = Faker()
        client_profiles = list(ClientProfile.objects.all())
        skills = list(Skill.objects.all())
        for i in range(count):
            client_profile = faker.random.choice(client_profiles)
            skill_subset = faker.random.sample(skills, faker.random.randint(1, len(skills)))
            hourly_rate = faker.pyfloat(left_digits=3, right_digits=2, positive=True)
            hourly_rate = Decimal(hourly_rate).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            job = Job(
                title=faker.word(),
                description=faker.text(max_nb_chars=200),
                hourly_rate=hourly_rate,
                estimated_end_date=faker.date_this_year(after_today=True),
                client_profile_id=client_profile,
            )
            job.save()
            job.skill.add(*skill_subset)


class ReviewAboutClient(BaseModel):
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
    from_freelancer = models.ForeignKey(
        "freelancers.FreelancerProfile",
        on_delete=models.CASCADE,
        related_name="sent_reviews",
    )
    to_client = models.ForeignKey(
        "clients.ClientProfile",
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )
    job = models.ForeignKey(
        "clients.Job",
        related_name="client_reviews",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Review About Client"
        verbose_name_plural = "Reviews About Clients"

    def __str__(self):
        return f"{self.rating} {self.from_freelancer} -> {self.to_client} ({self.job.title})"
