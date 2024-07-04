from django.contrib import admin

from freelancers.models import FreelancerProfile

admin.site.register(
    [
        FreelancerProfile,
    ]
)
