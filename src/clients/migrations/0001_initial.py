# Generated by Django 4.2.11 on 2024-05-16 01:49

from django.db import migrations, models

import clients.utils.utils
import clients.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ClientProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="company name",
                    ),
                ),
                (
                    "company_description",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="company description",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="images/client_profile_images/",
                        validators=[clients.utils.validators.validate_file_size],
                        verbose_name="photo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Client Profile",
                "verbose_name_plural": "Client Profiles",
            },
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("title", models.CharField(max_length=255, verbose_name="job title")),
                (
                    "description",
                    models.TextField(max_length=1000, verbose_name="job description"),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2, max_digits=5, verbose_name="hourly rate"
                    ),
                ),
                (
                    "estimated_end_date",
                    models.DateField(verbose_name="estimated end date"),
                ),
                (
                    "documentation",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=clients.utils.utils.documentation_upload,
                        verbose_name="documentation",
                    ),
                ),
                (
                    "is_concluded",
                    models.BooleanField(default=False, verbose_name="is concluded"),
                ),
            ],
            options={
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
            },
        ),
        migrations.CreateModel(
            name="ReviewAboutClient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "review",
                    models.TextField(
                        blank=True, max_length=1000, null=True, verbose_name="review"
                    ),
                ),
                (
                    "rating",
                    models.DecimalField(
                        decimal_places=1,
                        default=0.0,
                        max_digits=3,
                        validators=[clients.utils.validators.rating_validator],
                    ),
                ),
            ],
            options={
                "verbose_name": "Review About Client",
                "verbose_name_plural": "Reviews About Clients",
            },
        ),
    ]
