from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .. import models


class EventListView(ListView):
    model = models.Event
    paginate_by = 100
    template_name = "info/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = models.Event.objects.filter(
            organisation__admin=self.request.user,
            start_date_time__gte=timezone.now(),
        ).order_by("start_date_time")

        return context


class DashboardEventListView(ListView):
    model = models.Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = models.Event.objects.filter(
            organisation__admin=self.request.user,
            start_date_time__gte=timezone.now(),
        )

        return context


class DashboardEventCreateView(CreateView):
    model = models.Event
    fields = [
        "organisation",
        "event_name",
        "description",
        "location",
        "contact",
        "ticketed",
        "start_date_time",
        "end_date_time",
        "price",
        "tags",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user
        )
        return form


class DashboardEventUpdateView(UpdateView):
    model = models.Event
    fields = [
        "organisation",
        "event_name",
        "description",
        "location",
        "contact",
        "ticketed",
        "start_date_time",
        "end_date_time",
        "price",
        "tags",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user
        )
        return form


class EventDetailView(DetailView):
    model = models.Event

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")


class DashboardEventDeleteView(DeleteView):
    model = models.Event
    success_url = reverse_lazy("info:dashboard_events")
