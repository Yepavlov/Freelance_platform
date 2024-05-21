from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (CityViewSet, CountryViewSet, StateCreateAPIView,
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
    path("create_state/", StateCreateAPIView.as_view(), name="create_state"),
    path("update_state/<int:pk>/", StateUpdateAPIView.as_view(), name="update_state"),
    path(
        "retrieve_state/<int:pk>/",
        StateRetrieveAPIView.as_view(),
        name="retrieve_state",
    ),
    path("delete_state/<int:pk>/", StateDestroyAPIView.as_view(), name="delete_state"),
]
