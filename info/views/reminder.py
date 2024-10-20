from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .. import models


class ReminderCreateView(CreateView):
    model = models.Reminder
    fields = [
        "name",
        "email",
        "duration",
    ]

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse_lazy("info:event", kwargs={'pk': self.kwargs.get("pk")})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.initial["event"] = models.Event.objects.get(pk=self.kwargs.get("pk"))

        return form

    def form_valid(self, form):
        form.instance.event = models.Event.objects.get(pk=self.kwargs.get("pk"))

        return super().form_valid(form)
