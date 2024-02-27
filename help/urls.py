from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.help, name="help"),
    path("overview/", views.help, name="overview"),
    path("organisations/", views.help, name="oragnisations"),
    path("organisations/edit/", views.help, name="organisations_edit"),

    path("events/", views.help, name="events"),
    path("events/add/", views.help, name="events_add"),
    path("events/edit/", views.help, name="events_edit"),
    path("events/delete/", views.help, name="events_delete"),

    path("resources/", views.help, name="resources"),
    path("resources/add/", views.help, name="resources_add"),
    path("resources/edit/", views.help, name="resources_edit"),
    path("resources/delete/", views.help, name="resources_delete"),

    path("locations/", views.help, name="locations"),
    path("locations/add/", views.help, name="locations_add"),
    path("locations/edit/", views.help, name="locations_edit"),
    path("locations/delete/", views.help, name="locations_delete"),

    path("contacts/", views.help, name="contacts"),
    path("contacts/add/", views.help, name="contacts_add"),
    path("contacts/edit/", views.help, name="contacts_edit"),
    path("contacts/delete/", views.help, name="contacts_delete"),
]
