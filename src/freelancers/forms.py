from django import forms
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from core.models import BankingInformation
from freelancers.models import FreelancerProfile, Proposal


class FreelancerForm(ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            "position",
            "description",
            "birth_date",
            "hourly_rate",
            "city",
            "state",
            "country",
            "photo",
            "sex",
            "resume",
            "skill",
        ]


class UpdateFreelancerForm(FreelancerForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_number = PhoneNumberField(
        label="Phone Number",
        widget=PhoneNumberPrefixWidget(
            country_choices=[
                ("US", "+1"),
            ],
            attrs={"placeholder": "Format: (XXX)-XXX-XXXX"},
        ),
        help_text="Format: (XXX)-XXX-XXXX",
        required=False,
    )

    class Meta(FreelancerForm.Meta):
        fields = FreelancerForm.Meta.fields + [
            "first_name",
            "last_name",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, "user", None)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["phone_number"].initial = user.phone_number

    @staticmethod
    def normalize_text(text: str) -> str:
        return text.strip().capitalize()

    def save(self, commit=True):
        freelancer_profile = super().save(commit=False)
        user = freelancer_profile.user
        if user:
            user.first_name = self.normalize_text(self.cleaned_data.get("first_name", ""))
            user.last_name = self.normalize_text(self.cleaned_data.get("last_name", ""))
            user.phone_number = self.cleaned_data.get("phone_number")
            if commit:
                user.save()
                freelancer_profile.save()
                self.save_m2m()
        return freelancer_profile


class ProposalForm(ModelForm):
    class Meta:
        model = Proposal
        fields = (
            "title",
            "hourly_rate",
            "estimated_end_date",
            "documentation",
        )


class BankingInformationForm(ModelForm):
    class Meta:
        model = BankingInformation
        fields = (
            "account_holder_name",
            "account_number",
            "bank_name",
            "country",
            "currency",
        )
