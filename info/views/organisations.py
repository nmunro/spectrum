from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .. import models


def organisations(request):
    return render(request, "info/organisations.html", {"orgs": models.Organisation.objects.all().order_by("name")})

def organisation(request, org: str):
    return render(request, "info/organisation.html", {"org": get_object_or_404(models.Organisation, slug=org)})

def organisation_resources(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    resources = models.Resource.objects.filter(organisation=org)
    return render(request, "info/organisation_resources.html", {"org": org, "resources": resources})

def organisation_resource(request, org, pk: int):
    org = get_object_or_404(models.Organisation, slug=org)
    resource = models.Resource.objects.get(pk=pk, organisation=org)
    return render(request, "info/organisation_resource.html", {"org": org, "resource": resource})

def organisation_events(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    events = models.Event.objects.filter(organisation=org, start_date_time__gte=timezone.now())
    return render(request, "info/organisation_events.html", {"org": org, "events": events})

def organisation_event(request, org, pk: int):
    org = get_object_or_404(models.Organisation, slug=org)
    event = models.Event.objects.get(pk=pk, organisation=org)
    return render(request, "info/organisation_event.html", {"org": org, "event": event})
