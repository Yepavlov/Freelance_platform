from django.urls import path

from clients.views import (ClientProfileDetailView, ClientProfileUpdateView,
                           ClientProposalDetailView, CreateClientProfileView,
                           CreateJobView, IsConcludedProposalView, JobDelete,
                           JobListView, JobUpdate)

app_name = "clients"

urlpatterns = [
    path("create/", CreateClientProfileView.as_view(), name="create_client"),
    path(
        "client_profile_details/<int:pk>",
        ClientProfileDetailView.as_view(),
        name="client_profile_details",
    ),
    path(
        "update/<int:pk>",
        ClientProfileUpdateView.as_view(),
        name="client_profile_update",
    ),
    path(
        "create_job/",
        CreateJobView.as_view(),
        name="create_job",
    ),
    path(
        "list_jobs/",
        JobListView.as_view(),
        name="list_jobs",
    ),
    path(
        "job_update/<int:pk>",
        JobUpdate.as_view(),
        name="job_update",
    ),
    path(
        "job_delete/<int:pk>",
        JobDelete.as_view(),
        name="job_delete",
    ),
    path(
        "job_proposal_detail/<int:pk>",
        ClientProposalDetailView.as_view(),
        name="job_proposal_detail",
    ),
    path(
        "choose_proposal/<int:pk>/",
        IsConcludedProposalView.as_view(),
        name="choose_proposal",
    ),
]
