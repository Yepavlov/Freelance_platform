from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from clients.models import Job
from freelancers.forms import (FreelancerForm, ProposalForm,
                               UpdateFreelancerForm)
from freelancers.models import FreelancerProfile, Proposal


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


class FreelancerJobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "freelancers/list_job.html"
    context_object_name = "jobs"

    def get_queryset(self):
        freelancer_profile = FreelancerProfile.objects.prefetch_related("skill").get(user=self.request.user)
        skill_ids = [skill.id for skill in freelancer_profile.skill.all()]

        queryset = (
            Job.objects.select_related("client_profile_id")
            .prefetch_related("skill")
            .filter(skill__id__in=skill_ids)
            .distinct()
        )
        search_value = self.request.GET.get("search")
        if search_value:
            queryset = queryset.filter(skill__title__icontains=search_value).distinct()
        return queryset


class CreateProposalView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "freelancers/create_proposal.html"
    success_url = reverse_lazy("core:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs["job_id"]
        job = get_object_or_404(Job, pk=job_id)
        context["job"] = job
        return context

    def form_valid(self, form):
        job_id = self.kwargs["job_id"]
        job = get_object_or_404(Job, pk=job_id)
        form.instance.job_id = job
        form.instance.freelancer_profile_id = self.request.user.freelancer_profiles
        return super().form_valid(form)


class ListProposalView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = "freelancers/list_proposals.html"
    context_object_name = "proposals"

    def get_queryset(self):
        queryset = Proposal.objects.filter(freelancer_profile_id__user=self.request.user)
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class UpdateProposalView(LoginRequiredMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "freelancers/update_proposal.html"
    queryset = Proposal.objects.all()
    success_url = reverse_lazy("freelancers:list_proposals")


class DeleteProposalView(LoginRequiredMixin, DeleteView):
    model = Proposal
    template_name = "freelancers/delete_proposal.html"
    queryset = Proposal.objects.all()
    success_url = reverse_lazy("freelancers:list_proposals")
