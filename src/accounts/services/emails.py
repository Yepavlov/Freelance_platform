from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.utils.token_generator import TokenGenerator


def send_registration_email(user_instance: get_user_model(), request: HttpRequest) -> None:
    message = render_to_string(
        template_name="email/registration_email.html",
        context={
            "user": user_instance,
            "domain": get_current_site(request),
            "token": TokenGenerator().make_token(user_instance),
            "uid": urlsafe_base64_encode(force_bytes(user_instance.uuid)),
        },
    )
    email = EmailMessage(
        subject=settings.REGISTRATION_EMAIL_SUBJECT,
        body=message,
        to=[user_instance.email],
        cc=[settings.EMAIL_HOST_USER],
    )
    email.content_subtype = "html"
    email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
