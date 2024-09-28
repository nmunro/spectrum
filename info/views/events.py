from django.shortcuts import get_object_or_404, render
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

    def get_queryset(self):
        return models.Event.objects.filter(
            start_date_time__gte=timezone.now(),
            hide=False,
        ).order_by("start_date_time")


class OrganisationEventListView(ListView):
    model = models.Event
    paginate_by = 100
    template_name = "info/events.html"

    def get_queryset(self, **kwargs):
        return models.Event.objects.filter(
            organisation=get_object_or_404(
                models.Organisation,
                slug=self.kwargs["org"],
                active=True,
            ),
            hide=False,
            start_date_time__gte=timezone.now(),
        ).order_by("start_date_time")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=self.kwargs["org"])

        return context


class DashboardEventListView(ListView):
    model = models.Event
    paginate_by = 100
    context_object_name = "events"

    def get_queryset(self, **kwargs):
        return models.Event.objects.filter(
            organisation__admin=self.request.user,
            organisation__active=True,
            start_date_time__gte=timezone.now(),
        ).order_by("start_date_time")


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
        "ical_rrules",
        "price",
        "tags",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["ical_rrules"].queryset = models.iCalSchedule.objects.filter(organisation__admin=self.request.user)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user,
            active=True,
        ).order_by("organisation_name")

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
        "hide",
        "start_date_time",
        "end_date_time",
        "ical_rrules",
        "price",
        "tags",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["ical_rrules"].queryset = models.iCalSchedule.objects.filter(organisation__admin=self.request.user)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user,
            active=True,
        ).order_by("organisation_name")

        return form


class EventDetailView(DetailView):
    model = models.Event

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_events")


class DashboardEventDeleteView(DeleteView):
    model = models.Event
    success_url = reverse_lazy("info:dashboard_events")
