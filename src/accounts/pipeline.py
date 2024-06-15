from django.shortcuts import redirect
from django.urls import reverse


def redirect_to_complete_user_registration(backend, user=None, *args, **kwargs):
    if user and backend.name == "google-oauth2":
        if user.last_login is None:
            return redirect(reverse("accounts:complete_user_registration", kwargs={"uuid": user.uuid}))
        else:
            return {}
    return None
