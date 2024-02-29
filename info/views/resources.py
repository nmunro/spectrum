from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import models


def resources(request):
    return render(
        request,
        "info/resources.html",
        {"resources": models.Resource.objects.all()}
    )


class ResourceListview(ListView):
    model = models.Resource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resources"] = models.Resource.objects.filter(organisation__admin=self.request.user)

        return context


class ResourceCreateView(CreateView):
    model = models.Resource
    fields = ["organisation", "name", "description", "tags"]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_resources")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class ResourceUpdateView(UpdateView):
    model = models.Resource
    fields = ["organisation", "name", "description", "tags"]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_resources")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class ResourceDetailView(DetailView):
    model = models.Resource


class ResourceDeleteView(DeleteView):
    model = models.Resource
    success_url = reverse_lazy("info:dashboard_resources")
