from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramStrictWordSimilarity
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import models
from . import forms

class IndexView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/index.html"

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        query = request.POST["search"]

        events = models.Event.objects.annotate(
            similarity=TrigramStrictWordSimilarity(query, "name") + TrigramStrictWordSimilarity(query, "description"),
        ).filter(
            similarity__gte=0.2
        ).order_by(
            '-similarity'
        )

        resources = models.Resource.objects.annotate(
            similarity=TrigramStrictWordSimilarity(query, "name") + TrigramStrictWordSimilarity(query, "description"),
        ).filter(
            similarity__gte=0.2
        ).order_by(
            "-similarity"
        )

        return self.render_to_response({"results": [*events, *resources]})

def organisations(request):
    return render(request, "info/organisations.html", {"orgs": models.Organisation.objects.all().order_by("name")})

def organisation(request, org):
    return render(request, "info/organisation.html", {"org": get_object_or_404(models.Organisation, slug=org)})

def organisation_resources(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    resources = models.Resource.objects.filter(organisation=org)
    return render(request, "info/organisation_resources.html", {"org": org, "resources": resources})

def organisation_resource(request, org, resource_id):
    org = get_object_or_404(models.Organisation, slug=org)
    resource = models.Resource.objects.get(pk=resource_id, organisation=org)
    return render(request, "info/organisation_resource.html", {"org": org, "resource": resource})

def organisation_events(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    events = models.Event.objects.filter(organisation=org, start_date_time__gte=timezone.now())
    return render(request, "info/organisation_events.html", {"org": org, "events": events})

def organisation_event(request, org, event_id):
    org = get_object_or_404(models.Organisation, slug=org)
    event = models.Event.objects.get(pk=event_id, organisation=org)
    return render(request, "info/organisation_event.html", {"org": org, "event": event})

def resources(request):
    resources = models.Resource.objects.all()
    return render(request, "info/resources.html", {"resources": resources})

def resource(request, resource_id):
    resource = get_object_or_404(models.Resource, pk=resource_id)
    return render(request, "info/resource.html", {"resource": resource})

def events(request):
    events = models.Event.objects.filter(start_date_time__gte=timezone.now()).order_by("start_date_time")
    return render(request, "info/events.html", {"events": events})

def event(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    return render(request, "info/event.html", {"event": event})

def locations(request):
    locations = models.Location.objects.all()
    return render(request, "info/locations.html", {"locations": locations})

def location(request, location_id):
    location = models.Location.objects.get(pk=location_id)
    return render(request, "info/location.html", {"location": location})

class OrganisationListView(ListView):
    template_name = "info/dashboard.html"
    model = models.Organisation
    context_object_name = "organisations"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisations"] = get_list_or_404(models.Organisation, admin=self.request.user)
        return context

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


class DashboardEventsView(ListView):
    model = models.Event
    context_object_name = "events"
    form_class = forms.Event
    template_name = "info/dashboard_events.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["events"] = models.Event.objects.filter(organisation=context["org"], start_date_time__gte=timezone.now())

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))


class DashboardEventView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/dashboard_event.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["event"] = get_object_or_404(models.Event, id=kwargs["event_id"])
        context["form"] = self.form_class(instance=context["event"])

        return context

    def get(self, request, org, event_id):
        return self.render_to_response(self.get_context_data(org=org, event_id=event_id))

    def delete(self, request, org, event_id):
        event = get_object_or_404(models.Event, id=event_id)
        event.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "event": event.name,
        })

    def post(self, request, org, event_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, event_id=event_id)
            context["event"].name = form.cleaned_data["name"]
            context["event"].description = form.cleaned_data["description"]
            context["event"].location = form.cleaned_data["location"]
            context["event"].start_date_time = form.cleaned_data["start_date_time"]
            context["event"].end_date_time = form.cleaned_data["end_date_time"]
            context["event"].price = form.cleaned_data["price"]
            context["event"].save()

        return self.render_to_response(self.get_context_data(org=org, event_id=event_id))


class DashboardResourcesView(ListView):
    model = models.Resource
    form_class = forms.Resource
    template_name = "info/dashboard_resources.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["resources"] = models.Resource.objects.filter(organisation=context["org"])

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))


class DashboardResourceView(TemplateView):
    form_class = forms.ResourceForm
    template_name = "info/dashboard_resource.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["resource"] = get_object_or_404(models.Resource, id=kwargs["resource_id"])
        context["form"] = self.form_class(instance=context["resource"])

        return context

    def get(self, request, org, resource_id):
        return self.render_to_response(self.get_context_data(org=org, resource_id=resource_id))

    def delete(self, request, org, resource_id):
        resource = get_object_or_404(models.Resource, id=resource_id)
        resource.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "resource": resource.name,
        })

    def post(self, request, org, resource_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, resource_id=resource_id)
            context["resource"].name = form.cleaned_data["name"]
            context["resource"].description = form.cleaned_data["description"]
            context["resource"].save()

        return self.render_to_response(self.get_context_data(org=org, resource_id=resource_id))

class DashboardNewResourceView(TemplateView):
    form_class = forms.ResourceForm
    template_name = "info/new_resource.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))

    def post(self, request, org):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = models.Resource.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                organisation=get_object_or_404(models.Organisation, slug=org),
            )

        return redirect(obj)

class DashboardNewEventView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/new_event.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))

    def post(self, request, org):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = models.Event.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                location=form.cleaned_data["location"],
                start_date_time=form.cleaned_data["start_date_time"],
                end_date_time=form.cleaned_data["end_date_time"],
                price=form.cleaned_data["price"],
                organisation=get_object_or_404(models.Organisation, slug=org),
            )

        return redirect(obj)

class DashboardContactsView(ListView):
    model = models.Contact
    form_class = forms.ContactForm
    template_name = "info/dashboard_contacts.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["contacts"] = models.Contact.objects.filter(organisation=context["org"])

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))

class DashboardNewContactView(TemplateView):
    form_class = forms.ContactForm
    template_name = "info/new_contact.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["organisation"] = get_object_or_404(models.Organisation, slug=kwargs["organisation"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(organisation=org))

    def post(self, request, org):
        form = self.form_class(request.POST)

        if form.is_valid():
            obj = models.Contact.objects.create(
                organisation=models.Organisation.objects.get(slug=org),
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
            )

        return redirect("dashboard_contacts", org=org)

class DashboardContactView(TemplateView):
    form_class = forms.ContactForm
    template_name = "info/dashboard_contact.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["contact"] = get_object_or_404(models.Contact, id=kwargs["contact_id"])
        context["form"] = self.form_class(instance=context["contact"])

        return context

    def get(self, request, org, contact_id):
        return self.render_to_response(self.get_context_data(org=org, contact_id=contact_id))

    def delete(self, request, org, contact_id):
        contact = get_object_or_404(models.Contact, id=contact_id)
        contact.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "contact": contact.name,
        })

    def post(self, request, org, contact_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, contact_id=contact_id)
            context["contact"].name = form.cleaned_data["name"]
            context["contact"].email = form.cleaned_data["email"]
            context["contact"].phone_number = form.cleaned_data["phone_number"]
            context["contact"].save()

        return self.render_to_response(self.get_context_data(org=org, contact_id=contact_id))

class DashboardLocationsView(ListView):
    model = models.Location
    form_class = forms.LocationForm
    template_name = "info/dashboard_locations.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["locations"] = models.Location.objects.filter(organisation=context["org"])

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))


class DashboardNewLocationView(TemplateView):
    form_class = forms.LocationForm
    template_name = "info/new_location.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["organisation"] = get_object_or_404(models.Organisation, slug=kwargs["organisation"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(organisation=org))

    def post(self, request, org):
        form = self.form_class(request.POST)

        if form.is_valid():
            obj = models.Location.objects.create(
                organisation=models.Organisation.objects.get(slug=org),
                name=form.cleaned_data["name"],
                address=form.cleaned_data["address"],
                post_code=form.cleaned_data["post_code"],
            )

        return redirect("dashboard_locations", org=org)

class DashboardLocationView(TemplateView):
    form_class = forms.LocationForm
    template_name = "info/dashboard_location.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["location"] = get_object_or_404(models.Location, id=kwargs["location_id"])
        context["form"] = self.form_class(instance=context["location"])

        return context

    def get(self, request, org, location_id):
        return self.render_to_response(self.get_context_data(org=org, location_id=location_id))

    def delete(self, request, org, location_id):
        location = get_object_or_404(models.Location, id=location_id)
        location.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "location": location.name,
        })

    def post(self, request, org, location_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, location_id=location_id)
            context["location"].organisation = get_object_or_404(models.Organisation, slug=org)
            context["location"].name = form.cleaned_data["name"]
            context["location"].address = form.cleaned_data["address"]
            context["location"].post_code = form.cleaned_data["post_code"]
            context["location"].save()

        return self.render_to_response(self.get_context_data(org=org, location_id=location_id))
