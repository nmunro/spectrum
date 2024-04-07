from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from .. import forms
from .. import models


class DashboardView(ListView):
    template_name = "info/dashboard.html"
    model = models.Organisation
    paginate_by = 100
    context_object_name = "orgs"

    def get_queryset(self, **kwargs):
        return models.Organisation.objects.filter(admin=self.request.user).order_by("organisation_name")

def dashboard_org(request, org):
    org = get_object_or_404(models.Organisation, slug=org)

    if request.method == "POST":
        org.description = request.POST["description"]
        org.region = models.Region.objects.get(pk=int(request.POST["region"]))
        org.email = request.POST["email"]
        org.website = request.POST["website"]
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
