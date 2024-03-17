from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .. import models


class ResourceListView(ListView):
    model = models.Resource
    paginate_by = 100
    template_name = "info/resources.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resources"] = models.Resource.objects.all()

        return context


class OrganisationResourceListView(ListView):
    model = models.Resource
    paginate_by = 100
    template_name = "info/resources.html"

    def get_queryset(self, **kwargs):
        return models.Resource.objects.filter(
            organisation=get_object_or_404(models.Organisation, slug=self.kwargs["org"])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=self.kwargs["org"])

        return context


class DashboardResourceListview(ListView):
    model = models.Resource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resources"] = models.Resource.objects.filter(
            organisation__admin=self.request.user
        )

        return context


class DashboardResourceCreateView(CreateView):
    model = models.Resource
    fields = ["organisation", "resource_name", "description", "tags"]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_resources")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user
        )
        return form


class DashboardResourceUpdateView(UpdateView):
    model = models.Resource
    fields = ["organisation", "resource_name", "description", "tags"]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_resources")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(
            admin=self.request.user
        )
        return form


class ResourceDetailView(DetailView):
    model = models.Resource


class DashboardResourceDeleteView(DeleteView):
    model = models.Resource
    success_url = reverse_lazy("info:dashboard_resources")
