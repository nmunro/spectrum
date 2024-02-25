from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("organisations/", views.organisations, name="organisations"),
    path("organisations/<str:org>/", views.organisation, name="organisation"),
    path("organisations/<str:org>/resources/", views.organisation_resources, name="organisation_resources"),
    path("organisations/<str:org>/resources/<int:resource_id>/", views.organisation_resource, name="organisation_resource"),
    path("organisations/<str:org>/events/", views.organisation_events, name="organisation_events"),
    path("organisations/<str:org>/events/<int:event_id>/", views.organisation_event, name="organisation_event"),

    path("resources/", views.resources, name="resources"),
    path("resources/<int:resource_id>/", views.resource, name="resource"),

    path("events/", views.events, name="events"),
    path("events/<int:event_id>/", views.event, name="event"),

    path("locations/", views.locations, name="locations"),
    path("location/<int:location_id>/", views.location, name="location"),

    path("dashboard/", login_required(views.DashboardView.as_view()), name="dashboard"),

    path("dashboard/organisations/", views.dashboard_org, name="dashboard_org"),
    path("dashboard/organisations/<str:org>/", views.dashboard_org, name="dashboard_org"),

    path("dashboard/events/", login_required(views.DashboardEventsView.as_view()), name="dashboard_events"),
    path("dashboard/events/new/", login_required(views.DashboardNewEventView.as_view()), name="new_dashboard_event"),
    path("dashboard/events/<int:event_id>/", login_required(views.DashboardEventView.as_view()), name="dashboard_event"),

    path("dashboard/resources/", login_required(views.DashboardResourcesView.as_view()), name="dashboard_resources"),
    path("dashboard/resources/new/", login_required(views.DashboardNewResourceView.as_view()), name="new_dashboard_resource"),
    path("dashboard/resources/<int:resource_id>/", login_required(views.DashboardResourceView.as_view()), name="dashboard_resource"),

    path("dashboard/contacts/", login_required(views.DashboardContactsView.as_view()), name="dashboard_contacts"),
    path("dashboard/contacts/new/", login_required(views.DashboardNewContactView.as_view()), name="new_dashboard_contact"),
    path("dashboard/contacts/<int:contact_id>/", login_required(views.DashboardContactView.as_view()), name="dashboard_contact"),

    path("dashboard/locations/", login_required(views.DashboardLocationsView.as_view()), name="dashboard_locations"),
    path("dashboard/locations/new/", login_required(views.DashboardNewLocationView.as_view()), name="new_dashboard_location"),
    path("dashboard/locations/<int:location_id>/", login_required(views.DashboardLocationView.as_view()), name="dashboard_location"),
]
