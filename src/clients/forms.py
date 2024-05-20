from django.forms import ModelForm

from clients.models import ClientProfile


class ClientForm(ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            "company",
            "company_description",
            "city",
            "state",
            "country",
            "image",
        ]
