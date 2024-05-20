from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from freelancers.utils.utils import documentation_upload
from freelancers.utils.validators import (birth_date_validator,
                                          extension_validator,
                                          rating_validator, validate_file_size)


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
    country = models.ForeignKey("core.Country", on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey("core.State", on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey("core.City", on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(
        _("photo"),
        upload_to="images/freelancer_profile_photo/",
        blank=True,
        null=True,
        validators=[validate_file_size],
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
        default="images/default.jpg",
    )

    class Meta:
        verbose_name = "Freelancer Profile"
        verbose_name_plural = "Freelancer Profiles"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.position} ({self.id})"

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
