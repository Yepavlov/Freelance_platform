from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserRegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        label="Phone Number",
        widget=PhoneNumberPrefixWidget(
            country_choices=[
                ("US", "+1"),
            ],
            attrs={"placeholder": "Format: (XXX)-XXX-XXXX"},
        ),
        help_text="Format: (XXX)-XXX-XXXX",
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "phone_number",
            "user_type",
            "password1",
            "password2",
        ]
