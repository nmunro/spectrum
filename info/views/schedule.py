from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .. import models


class DashboardiCalScheduleListView(ListView):
    model = models.iCalSchedule
    paginate_by = 100
    context_object_name = "schedules"

    def get_queryset(self, **kwargs):
        return models.iCalSchedule.objects.all()


class DashboardiCalScheduleCreateView(CreateView):
    model = models.iCalSchedule
    fields = [
        "organisation",
        "label",
        "rrule",
    ]

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["orgs"] = models.Organisation.objects.filter(
            admin=self.request.user,
            active=True,
            enable_scheduler=True,
        ).order_by("organisation_name")
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedules")


class DashboardiCalScheduleUpdateView(UpdateView):
    model = models.iCalSchedule
    fields = [
        "organisation",
        "label",
        "rrule",
    ]

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["orgs"] = models.Organisation.objects.filter(
            admin=self.request.user,
            active=True,
            enable_scheduler=True,
        ).order_by("organisation_name")
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedules")


class iCalScheduleDetailView(DetailView):
    model = models.iCalSchedule

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedule")


class DashboardiCalScheduleDeleteView(DeleteView):
    model = models.iCalSchedule
    success_url = reverse_lazy("info:dashboard_schedules")
