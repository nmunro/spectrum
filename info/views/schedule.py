from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .. import models


class DashboardScheduleListView(ListView):
    model = models.Schedule
    paginate_by = 100
    context_object_name = "schedules"

    def get_queryset(self, **kwargs):
        return models.Schedule.objects.all()


class DashboardScheduleCreateView(CreateView):
    model = models.Schedule
    fields = [
        "label",
        "rrule",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedules")


class DashboardScheduleUpdateView(UpdateView):
    model = models.Schedule
    fields = [
        "label",
        "rrule",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedules")


class ScheduleDetailView(DetailView):
    model = models.Schedule

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_schedule")


class DashboardScheduleDeleteView(DeleteView):
    model = models.Schedule
    success_url = reverse_lazy("info:dashboard_schedules")
