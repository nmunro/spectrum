from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import forms
from .. import models


class LocationListView(ListView):
    model = models.Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locations"] = models.Location.objects.filter(organisation__admin=self.request.user)

        return context

class LocationCreateView(CreateView):
    model = models.Location
    fields = [
        "organisation",
        "venue_name",
        "address",
        "post_code",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_locations")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class LocationUpdateView(UpdateView):
    model = models.Location
    fields = [
        "organisation",
        "venue_name",
        "address",
        "post_code",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_locations")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class LocationDetailView(DetailView):
    model = models.Location


class LocationDeleteView(DeleteView):
    model = models.Location
    success_url = reverse_lazy("info:dashboard_locations")
