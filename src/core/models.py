from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class BankingInformation(BaseModel):
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    currency = models.CharField(max_length=50)
    freelancer_profile = models.ForeignKey(
        "freelancers.FreelancerProfile",
        on_delete=models.CASCADE,
        related_name="freelancer_banking_information",
        blank=True,
        null=True,
    )
    client_profile = models.ForeignKey(
        "clients.ClientProfile",
        on_delete=models.CASCADE,
        related_name="client_banking_information",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Banking Information"
        verbose_name_plural = "Freelancer Banking Information"

    def __str__(self):
        profile_id = self.freelancer_profile_id or self.client_profile_id
        return f"{self.bank_name} {self.account_holder_name} {self.account_number} {profile_id}"


class Skill(models.Model):
    title = models.CharField(
        _("title"),
        max_length=150,
    )

    def __str__(self):
        return f"{self.title} ({self.id})"

    @classmethod
    def generate_skills(cls, count: int) -> None:
        faker = Faker()
        list_skills = []
        for i in range(count):
            skill = Skill(
                title=faker.word(),
            )
            list_skills.append(skill)
        Skill.objects.bulk_create(list_skills)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Payment(models.Model):
    amount = models.DecimalField(
        _("amount"),
        max_digits=10,
        decimal_places=2,
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        max_length=1000,
    )
    payment_date = models.DateField(
        _("payment date"),
        auto_now_add=True,
    )
    payment_method = models.CharField(
        _("payment method"),
        max_length=100,
    )
    job = models.ForeignKey(
        "clients.Job",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"${self.amount} - {self.payment_date} {self.job}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
