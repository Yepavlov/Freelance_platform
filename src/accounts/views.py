from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView

from accounts.forms import UserRegistrationForm
from accounts.services.emails import send_registration_email
from accounts.utils.token_generator import TokenGenerator


class UserRegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        send_registration_email(user_instance=self.object, request=self.request)

        return super().form_valid(form)


class ActivateUserView(RedirectView):

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            uuid = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(uuid=uuid)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data!!!", status=410)

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(
                request,
                current_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            if current_user.user_type == 0:
                return HttpResponseRedirect(reverse("freelancers:create_freelancer"))
            elif current_user.user_type == 1:
                return HttpResponseRedirect(reverse("clients:create_client"))
        return HttpResponse("Wrong data!!!", status=410)


class UserLoginView(LoginView):
    pass


class UserLogoutView(LogoutView):
    pass
