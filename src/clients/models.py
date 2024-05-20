from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from clients.utils.utils import documentation_upload
from clients.utils.validators import rating_validator, validate_file_size
from core.models import BaseModel


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
