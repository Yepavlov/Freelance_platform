from django.urls import path

from core.views import (CreateCityView, CreateCountryView, CreateSkillView,
                        CreateStateView, IndexView)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create_city/", CreateCityView.as_view(), name="create_city"),
    path("create_state/", CreateStateView.as_view(), name="create_state"),
    path("create_country/", CreateCountryView.as_view(), name="create_country"),
    path("create_skill/", CreateSkillView.as_view(), name="create_skill"),
]
