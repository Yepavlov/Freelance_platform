from django.contrib import admin

from clients.models import ClientProfile

admin.site.register(
    [
        ClientProfile,
    ]
)
