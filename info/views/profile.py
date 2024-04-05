from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


class DashboardProfileView(UpdateView):
    model = User
    fields = [
        "first_name",
        "last_name",
        "email",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_profile", kwargs={"pk": self.request.user.pk})
