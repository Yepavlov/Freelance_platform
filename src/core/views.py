from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.forms import CityForm, CountryForm, SkillForm, StateForm
from core.models import City, Country, Skill, State
from core.tasks import generate_users_task


class IndexView(TemplateView):
    template_name = "index.html"


class CreateCityView(CreateView):
    model = City
    form_class = CityForm
    template_name = "core/create_city.html"
    success_url = reverse_lazy("core:index")


class CreateStateView(CreateView):
    model = State
    form_class = StateForm
    template_name = "core/create_state.html"
    success_url = reverse_lazy("core:index")


class CreateCountryView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = "core/create_country.html"
    success_url = reverse_lazy("core:index")


class CreateSkillView(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "core/create_skill.html"
    success_url = reverse_lazy("core:index")


def create_users_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_users_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_users_task.html")
