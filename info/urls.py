from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "info"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("organisations/", views.organisations, name="organisations"),
    path("organisations/<str:org>/", views.organisation, name="organisation"),
    path(
        "organisations/<str:org>/resources/",
        views.organisation_resources,
        name="organisation_resources",
    ),
    path(
        "organisations/<str:org>/events/",
        views.organisation_events,
        name="organisation_events",
    ),
    path("resources/", views.resources, name="resources"),
    path("resources/<int:pk>/", views.ResourceDetailView.as_view(), name="resource"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event"),
    path(
        "dashboard/organisations/",
        login_required(views.DashboardView.as_view()),
        name="dashboard",
    ),
    path(
        "dashboard/organisations/<str:org>/",
        login_required(views.dashboard_org),
        name="dashboard_org",
    ),
    path(
        "dashboard/events/",
        login_required(views.DashboardEventListView.as_view()),
        name="dashboard_events",
    ),
    path(
        "dashboard/events/new/",
        login_required(views.DashboardEventCreateView.as_view()),
        name="new_dashboard_event",
    ),
    path(
        "dashboard/events/<int:pk>/",
        login_required(views.DashboardEventUpdateView.as_view()),
        name="dashboard_event",
    ),
    path(
        "dashboard/events/<int:pk>/delete/",
        login_required(views.DashboardEventDeleteView.as_view()),
        name="delete_dashboard_event",
    ),
    path(
        "dashboard/resources/",
        login_required(views.ResourceListview.as_view()),
        name="dashboard_resources",
    ),
    path(
        "dashboard/resources/new/",
        login_required(views.ResourceCreateView.as_view()),
        name="new_dashboard_resource",
    ),
    path(
        "dashboard/resources/<int:pk>/",
        login_required(views.ResourceUpdateView.as_view()),
        name="dashboard_resource",
    ),
    path(
        "dashboard/resources/<int:pk>/delete/",
        login_required(views.ResourceDeleteView.as_view()),
        name="delete_dashboard_resource",
    ),
    path(
        "dashboard/contacts/",
        login_required(views.ContactListView.as_view()),
        name="dashboard_contacts",
    ),
    path(
        "dashboard/contacts/new/",
        login_required(views.ContactCreateView.as_view()),
        name="new_dashboard_contact",
    ),
    path(
        "dashboard/contacts/<int:pk>/",
        login_required(views.ContactUpdateView.as_view()),
        name="dashboard_contact",
    ),
    path(
        "dashboard/contacts/<int:pk>/delete/",
        login_required(views.ContactDeleteView.as_view()),
        name="delete_dashboard_contact",
    ),
    path(
        "dashboard/locations/",
        login_required(views.LocationListView.as_view()),
        name="dashboard_locations",
    ),
    path(
        "dashboard/locations/new/",
        login_required(views.LocationCreateView.as_view()),
        name="new_dashboard_location",
    ),
    path(
        "dashboard/locations/<int:pk>/",
        login_required(views.LocationUpdateView.as_view()),
        name="dashboard_location",
    ),
    path(
        "dashboard/locations/<int:pk>/delete/",
        login_required(views.LocationDeleteView.as_view()),
        name="delete_dashboard_location",
    ),
]
