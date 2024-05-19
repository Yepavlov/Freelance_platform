# Generated by Django 4.2.11 on 2024-05-19 19:16

from django.db import migrations, models

import clients.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientprofile",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images/client_profile_images/",
                validators=[clients.utils.validators.validate_file_size],
                verbose_name="image",
            ),
        ),
    ]
