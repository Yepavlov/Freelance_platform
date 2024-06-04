from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from freelancers.forms import FreelancerForm
from freelancers.models import FreelancerProfile


class CreateFreelancerProfileView(LoginRequiredMixin, CreateView):
    model = FreelancerProfile
    form_class = FreelancerForm
    template_name = "freelancers/create.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FreelancerProfileDetailView(LoginRequiredMixin, DetailView):
    model = FreelancerProfile
    template_name = "freelancers/freelancer_profile_details.html"
    context_object_name = "freelancer_profile"
