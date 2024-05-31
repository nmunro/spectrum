from django.shortcuts import get_object_or_404, render

from .. import forms, models


def dashboard_organisation(request, org):
    org = get_object_or_404(models.Organisation, slug=org)

    if request.method == "POST":
        org.description = request.POST["description"]
        org.region = models.Region.objects.get(pk=int(request.POST["region"]))
        org.email = request.POST["email"]
        org.website = request.POST["website"]
        org.accepting_volunteers = request.POST.get("accepting_volunteers", "off") == "on"
        org.save()

    return render(
        request,
        "info/dashboard_org.html",
        {
            "org": org,
            "form": forms.OrganisationForm(instance=org),
            "resources": models.Resource.objects.filter(organisation=org),
            "events": models.Event.objects.filter(organisation=org),
            "contacts": models.Contact.objects.filter(organisation=org),
            "locations": models.Location.objects.filter(organisation=org),
        },
    )
