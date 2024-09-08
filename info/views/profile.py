from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from ..forms import RegisterForm


class UserCreateView(CreateView):
    model = User
    template_name = "info/register.html"
    fields = [
        "username",
        "email",
        "password1",
        "password2",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("login")

    def post(self, request):
        if (form := RegisterForm(request.POST)).is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)

            return redirect("info:dashboard_organisations")

        return render(request, "info/register.html", {"form": RegisterForm()})

    def get(self, request):
        return render(request, 'info/register.html', {"form": RegisterForm()})


class DashboardUserView(UpdateView):
    model = User
    fields = [
        "first_name",
        "last_name",
        "email",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_user", kwargs={"pk": self.request.user.pk})
