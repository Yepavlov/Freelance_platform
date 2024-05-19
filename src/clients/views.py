from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from clients.forms import ClientForm
from clients.models import ClientProfile


class CreateClientProfileView(LoginRequiredMixin, CreateView):
    model = ClientProfile
    form_class = ClientForm
    template_name = "clients/create.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
