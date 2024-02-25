from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.views.generic.base import TemplateView

from .. import forms
from .. import models


class DashboardView(TemplateView):
    template_name = "info/dashboard.html"
    model = models.Organisation
    context_object_name = "organisations"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orgs"] = get_list_or_404(models.Organisation, admin=self.user)
        context["user"] = self.request.user
        return context

    def get(self, request):
        return self.render_to_response(self.get_context_data())

@login_required
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
            "form": forms.OrgForm(instance=org),
            "resources": models.Resource.objects.filter(organisation=org),
            "events": models.Event.objects.filter(organisation=org),
            "contacts": models.Contact.objects.filter(organisation=org),
            "locations": models.Location.objects.filter(organisation=org),
        },
    )
