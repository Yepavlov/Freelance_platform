from django.urls import path

from freelancers.views import (CreateFreelancerProfileView,
                               FreelancerProfileDetailView)

app_name = "freelancers"

urlpatterns = [
    path("create/", CreateFreelancerProfileView.as_view(), name="create_freelancer"),
    path(
        "freelancer_profile_delails/<int:pk>",
        FreelancerProfileDetailView.as_view(),
        name="freelancer_profile_details",
    ),
]
