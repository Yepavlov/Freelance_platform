from django.urls import path

from clients.views import (ClientProfileDetailView, ClientProfileUpdateView,
                           CreateClientProfileView, CreateJobView, JobListView)

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
]
