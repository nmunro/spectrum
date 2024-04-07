from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import models


class OrganisationListView(ListView):
    model = models.Organisation
    paginate_by = 100

    def get_queryset(self, **kwargs):
        return models.Organisation.objects.filter(active=True).order_by(
            "organisation_name"
        )


class OrganisationDetailView(DetailView):
    model = models.Organisation
    slug_field = "slug"
    slug_url_kwarg = "org"
