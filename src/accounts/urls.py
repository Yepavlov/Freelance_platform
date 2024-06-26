from django.urls import path

from accounts.views import (ActivateUserView, CompleteUserRegistrationView,
                            UserLoginView, UserLogoutView,
                            UserRegistrationView)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path(
        "activate/<str:uuid64>/<str:token>",
        ActivateUserView.as_view(),
        name="activate_user",
    ),
    path(
        "complete-registration/<uuid:uuid>",
        CompleteUserRegistrationView.as_view(),
        name="complete_user_registration",
    ),
]
