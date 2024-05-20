from django.core.exceptions import ValidationError
from django.forms import ModelForm

from core.models import City, Country, Skill, State


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name", "state"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if City.objects.filter(name=name).exists():
            raise ValidationError(f"The city {name} already exists.")
        return name


class StateForm(ModelForm):
    class Meta:
        model = State
        fields = ["name", "country"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if State.objects.filter(name=name).exists():
            raise ValidationError(f"The state {name} already exists.")


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Country.objects.filter(name=name).exists():
            raise ValidationError(f"The country {name} already exists.")


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if Skill.objects.filter(title=title).exists():
            raise ValidationError(f"The skill {title} already exists.")
        return title
