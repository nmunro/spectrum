from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .. import forms, models


class DashboardOrganisationView(ListView):
    template_name = "info/dashboard.html"
    model = models.Organisation
    paginate_by = 100
    context_object_name = "orgs"

    def get_queryset(self, **kwargs):
        return models.Organisation.objects.filter(
            admin=self.request.user, active=True
        ).order_by("organisation_name")


class DashboardOrganisationCreateView(CreateView):
    model = models.Organisation
    fields = [
        "organisation_name",
        "region",
        "email",
        "website",
        "phone_number",
        "description",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_organisations")

    def form_valid(self, form):
        form.instance.admin = self.request.user
        form.instance.active = False
        form.instance.slug = slugify(form.instance.organisation_name)
        return super().form_valid(form)


def dashboard_organisation(request, org):
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
