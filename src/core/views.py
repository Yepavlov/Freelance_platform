from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from clients.models import ClientProfile
from core.forms import CityForm, CountryForm, SkillForm, StateForm
from core.models import BankingInformation, City, Country, Skill, State
from core.tasks import (generate_cities_task, generate_client_profile_task,
                        generate_countries_task,
                        generate_freelancer_profile_task, generate_skills_task,
                        generate_states_task, generate_users_task)
from freelancers.forms import BankingInformationForm
from freelancers.models import FreelancerProfile


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


class CreateBankingInformationView(LoginRequiredMixin, CreateView):
    model = BankingInformation
    form_class = BankingInformationForm
    template_name = "core/create_banking_info.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        if self.request.user.user_type == 0:
            freelancer_profile = FreelancerProfile.objects.get(user=self.request.user)
            form.instance.freelancer_profile = freelancer_profile
        elif self.request.user.user_type == 1:
            client_profile = ClientProfile.objects.get(user=self.request.user)
            form.instance.client_profile = client_profile
        form.instance.user = self.request.user
        return super().form_valid(form)


class BankingInformationListView(LoginRequiredMixin, ListView):
    model = BankingInformation
    template_name = "core/list_banking_info.html"
    context_object_name = "banking_info"

    def get_queryset(self):
        if self.request.user.user_type == 0:
            queryset = BankingInformation.objects.filter(freelancer_profile__user=self.request.user).select_related(
                "country"
            )
        elif self.request.user.user_type == 1:
            queryset = BankingInformation.objects.filter(client_profile__user=self.request.user).select_related(
                "country"
            )
        return queryset


class UpdateBankingInformationView(LoginRequiredMixin, UpdateView):
    model = BankingInformation
    form_class = BankingInformationForm
    template_name = "core/update_banking_info.html"
    queryset = BankingInformation.objects.all()
    success_url = reverse_lazy("core:list_banking_info")


class DeleteBankingInformation(LoginRequiredMixin, DeleteView):
    model = BankingInformation
    template_name = "core/delete_banking_info.html"
    queryset = BankingInformation.objects.all()
    success_url = reverse_lazy("core:list_banking_info")
    context_object_name = "banking_info"


def create_users_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_users_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_users_task.html")


def create_freelancer_profile_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_freelancer_profile_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_freelancer_profile_task.html")


def create_countries_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_countries_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_countries_task.html")


def create_states_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_states_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_states_task.html")


def create_cities_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_cities_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_cities_task.html")


def create_client_profile_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_client_profile_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_client_profile_task.html")


def create_skills_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        count = request.POST.get("count")
        generate_skills_task.delay(int(count))
        return redirect("core:index")
    return render(request, "core/create_skill_task.html")
