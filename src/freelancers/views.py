from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from freelancers.forms import FreelancerForm, UpdateFreelancerForm
from freelancers.models import FreelancerProfile


class CreateFreelancerProfileView(LoginRequiredMixin, CreateView):
    model = FreelancerProfile
    form_class = FreelancerForm
    template_name = "freelancers/create.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FreelancerProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = FreelancerProfile
    template_name = "freelancers/freelancer_profile_details.html"
    context_object_name = "freelancer_profile"

    def get_queryset(self):
        return super().get_queryset().select_related("user", "country", "state", "city").prefetch_related("skill")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class FreelancerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FreelancerProfile
    form_class = UpdateFreelancerForm
    template_name = "freelancers/update.html"

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_success_url(self):
        return reverse_lazy("freelancers:freelancer_profile_details", kwargs={"pk": self.object.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
