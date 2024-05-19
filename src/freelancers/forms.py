from django.forms import ModelForm

from freelancers.models import FreelancerProfile


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
