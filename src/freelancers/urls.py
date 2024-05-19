from django.urls import path

from freelancers.views import CreateFreelancerProfileView

app_name = "freelancers"

urlpatterns = [
    path("create/", CreateFreelancerProfileView.as_view(), name="create_freelancer"),
]
