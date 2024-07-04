from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  RedirectView, UpdateView)

from clients.forms import (ClientForm, ClientReviewForm, JobForm,
                           UpdateClientForm)
from clients.models import ClientProfile, Job, ReviewAboutClient
from freelancers.models import FreelancerProfile, Proposal


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
        filter_status = self.request.GET.get("filter_status")
        search_value = self.request.GET.get("search")
        if search_value:
            queryset = queryset.filter(title__icontains=search_value)
        if filter_status == "is_concluded":
            queryset = queryset.filter(is_concluded=True)
        elif filter_status == "not_concluded":
            queryset = queryset.filter(is_concluded=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_status"] = self.request.GET.get("filter_status", "")
        context["search_value"] = self.request.GET.get("search", "")
        return context


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


class FreelancerProfileDetailView(LoginRequiredMixin, DetailView):
    model = FreelancerProfile
    template_name = "clients/freelancer_profile_info.html"
    context_object_name = "freelancer_profile"

    def get_object(self, queryset=None):
        uuid = self.kwargs.get("uuid")
        return get_object_or_404(FreelancerProfile, user__uuid=uuid)

    def get_queryset(self):
        return super().get_queryset().select_related("user", "city", "state", "country").prefetch_related("skills")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer_profile = self.get_object()
        average_rating = freelancer_profile.received_reviews.aggregate(Avg("rating"))["rating__avg"] or 0.0
        reviews = freelancer_profile.get_all_reviews()
        context["received_reviews"] = reviews
        context["average_rating"] = average_rating
        return context


class CreateClientReviewView(LoginRequiredMixin, CreateView):
    model = ReviewAboutClient
    form_class = ClientReviewForm
    template_name = "clients/create_client_review.html"
    success_url = reverse_lazy("freelancers:list_proposals")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal_id = self.kwargs.get("proposal_id")
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        context["job"] = proposal.job_id
        return context

    def form_valid(self, form):
        proposal_id = self.kwargs.get("proposal_id")
        proposal = get_object_or_404(Proposal, pk=proposal_id)

        form.instance.job = proposal.job_id
        form.instance.to_client = proposal.job_id.client_profile_id
        form.instance.from_freelancer = self.request.user.freelancer_profiles

        if proposal.selected:
            return super().form_valid(form)
        else:
            form.add_error(None, "You can only leave a review after the proposal will be selected.")
            return self.form_invalid(form)
