from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import MyUserManager


class UserType(models.IntegerChoices):
    Freelancer = 0, "Freelancer"
    Client = 1, "Client"


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        unique=True,
        editable=False,
        db_index=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    phone_number = PhoneNumberField(
        _("phone number"),
        null=True,
        blank=True,
        region="US",
    )
    user_type = models.PositiveSmallIntegerField(
        _("user type"),
        choices=UserType.choices,
        default=UserType.Freelancer,
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "password",
        "is_staff",
        "phone_number",
        "user_type",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_registration_age(self):
        return f"Time on site: {timezone.now() - self.date_joined}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
