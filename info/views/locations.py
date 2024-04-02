from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import models


class LocationListView(ListView):
    model = models.Location
    paginate_by = 100
    context_object_name = "locations"

    def get_queryset(self, **kwargs):
        return models.Location.objects.filter(organisation__admin=self.request.user).order_by("venue_name")

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
