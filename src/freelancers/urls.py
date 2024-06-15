from django.urls import path

from freelancers.views import (CreateFreelancerProfileView, CreateProposalView,
                               DeleteProposalView, FreelancerJobListView,
                               FreelancerProfileDetailView,
                               FreelancerProfileUpdateView, ListProposalView,
                               UpdateProposalView)

app_name = "freelancers"

urlpatterns = [
    path("create/", CreateFreelancerProfileView.as_view(), name="create_freelancer"),
    path(
        "freelancer_profile_delails/<int:pk>",
        FreelancerProfileDetailView.as_view(),
        name="freelancer_profile_details",
    ),
    path(
        "update/<int:pk>",
        FreelancerProfileUpdateView.as_view(),
        name="freelancer_profile_update",
    ),
    path("list_job/", FreelancerJobListView.as_view(), name="freelancer_list_job"),
    path(
        "create_proposal/<int:job_id>/",
        CreateProposalView.as_view(),
        name="create_proposal",
    ),
    path(
        "list_proposal/",
        ListProposalView.as_view(),
        name="list_proposals",
    ),
    path(
        "update_proposal/<int:pk>",
        UpdateProposalView.as_view(),
        name="update_proposal",
    ),
    path(
        "delete_proposal/<int:pk>",
        DeleteProposalView.as_view(),
        name="delete_proposal",
    ),
]
