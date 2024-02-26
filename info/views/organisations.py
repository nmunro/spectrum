from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .. import models


def organisations(request):
    return render(request, "info/organisations.html", {"orgs": models.Organisation.objects.all().order_by("name")})

def organisation(request, org: str):
    return render(request, "info/organisation.html", {"org": get_object_or_404(models.Organisation, slug=org)})

def organisation_resources(request, org: str):
    org = get_object_or_404(models.Organisation, slug=org)
    resources = models.Resource.objects.filter(organisation=org)

    return render(request, "info/resources.html", {"org": org, "resources": resources})

def organisation_events(request, org: str):
    org = get_object_or_404(models.Organisation, slug=org)
    events = models.Event.objects.filter(organisation=org, start_date_time__gte=timezone.now())

    return render(request, "info/events.html", {"org": org, "events": events})
