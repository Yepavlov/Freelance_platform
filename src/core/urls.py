from django.urls import path

from core.views import (CreateCityView, CreateCountryView, CreateSkillView,
                        CreateStateView, IndexView, create_cities_task_view,
                        create_client_profile_task_view,
                        create_countries_task_view,
                        create_freelancer_profile_task_view,
                        create_skills_task_view, create_states_task_view,
                        create_users_task_view)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create_city/", CreateCityView.as_view(), name="create_city"),
    path("create_state/", CreateStateView.as_view(), name="create_state"),
    path("create_country/", CreateCountryView.as_view(), name="create_country"),
    path("create_skill/", CreateSkillView.as_view(), name="create_skill"),
    path("create_users_task/", create_users_task_view, name="create_users_task"),
    path(
        "create_freelancer_profile_task/",
        create_freelancer_profile_task_view,
        name="create_freelancer_profile_task",
    ),
    path(
        "create_countries_task/",
        create_countries_task_view,
        name="create_countries_task",
    ),
    path(
        "create_states_task/",
        create_states_task_view,
        name="create_states_task",
    ),
    path(
        "create_cities_task/",
        create_cities_task_view,
        name="create_cities_task",
    ),
    path(
        "create_client_profile_task/",
        create_client_profile_task_view,
        name="create_client_profile_task",
    ),
    path(
        "create_skills_task/",
        create_skills_task_view,
        name="create_skills_task",
    ),
]
