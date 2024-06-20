from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  RedirectView, UpdateView)

from clients.forms import ClientForm, JobForm, UpdateClientForm
from clients.models import ClientProfile, Job
from freelancers.models import Proposal


class CreateClientProfileView(LoginRequiredMixin, CreateView):
    model = ClientProfile
    form_class = ClientForm
    template_name = "clients/create.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateJobView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "clients/create_job.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        client_profile = get_object_or_404(ClientProfile, user=self.request.user)
        form.instance.client_profile_id = client_profile
        return super().form_valid(form)


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "clients/list_job.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = (
            Job.objects.select_related(
                "client_profile_id",
            )
            .prefetch_related(
                "skill",
                "proposals",
            )
            .filter(client_profile_id__user=self.request.user)
        )
        search_value = self.request.GET.get("search")
        if search_value:
            queryset = queryset.filter(title__icontains=search_value)
        return queryset


class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "clients/update_job.html"
    queryset = Job.objects.all()
    success_url = reverse_lazy("clients:list_jobs")


class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = "clients/delete_job.html"
    queryset = Job.objects.all()
    success_url = reverse_lazy("clients:list_jobs")


class ClientProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClientProfile
    template_name = "clients/client_profile_details.html"
    context_object_name = "client_profile"

    def get_queryset(self):
        return super().get_queryset().select_related("user", "city", "state", "country")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ClientProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClientProfile
    form_class = UpdateClientForm
    template_name = "clients/update.html"

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_success_url(self):
        return reverse_lazy("clients:client_profile_details", kwargs={"pk": self.object.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ClientProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = "clients/proposal_detail.html"
    context_object_name = "proposal"

    def get_queryset(self):
        return super().get_queryset().select_related("job_id")


class IsConcludedProposalView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("clients:list_jobs")

    def get_redirect_url(self, *args, **kwargs):
        proposal = get_object_or_404(Proposal, pk=kwargs["pk"])
        job = proposal.job_id

        proposal.selected = True
        proposal.save()
        job.is_concluded = True
        job.save()

        return super().get_redirect_url(*args, **kwargs)
