from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (CityViewSet, ClientProfileRetrieveAPIView,
                       CountryViewSet, CreateClientProfileAPIView,
                       CreateFreelancerProfileAPIView,
                       FreelancerProfileRetrieveAPIView, StateCreateAPIView,
                       StateDestroyAPIView, StateRetrieveAPIView,
                       StateUpdateAPIView)

app_name = "api"
router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version="v1.0",
        description="API for passing questions",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger_docs"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls")),
    path("create_state/", StateCreateAPIView.as_view(), name="create_state"),
    path(
        "create_freelancer_profile/",
        CreateFreelancerProfileAPIView.as_view(),
        name="create_freelancer_profile",
    ),
    path(
        "retrieve_freelancer_profile/",
        FreelancerProfileRetrieveAPIView.as_view(),
        name="retrieve_freelancer_profile",
    ),
    path(
        "create_client_profile/",
        CreateClientProfileAPIView.as_view(),
        name="create_client_profile",
    ),
    path(
        "retrieve_client_profile/",
        ClientProfileRetrieveAPIView.as_view(),
        name="retrieve_client_profile",
    ),
    path("update_state/<int:pk>/", StateUpdateAPIView.as_view(), name="update_state"),
    path(
        "retrieve_state/<int:pk>/",
        StateRetrieveAPIView.as_view(),
        name="retrieve_state",
    ),
    path("delete_state/<int:pk>/", StateDestroyAPIView.as_view(), name="delete_state"),
]
