from django.urls import path

from clients.views import CreateClientProfileView

app_name = "clients"

urlpatterns = [
    path("create/", CreateClientProfileView.as_view(), name="create_client"),
]
