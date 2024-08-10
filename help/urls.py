from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "help"

urlpatterns = [
    path("overview/", views.overview, name="overview"),
    path("organisations/", views.organisations, name="organisations"),
    path("organisations/edit/", views.organisations_edit, name="organisations_edit"),

    path("events/", views.events, name="events"),
    path("events/add/", views.events_add, name="events_add"),
    path("events/edit/", views.events_edit, name="events_edit"),
    path("events/delete/", views.events_delete, name="events_delete"),

    path("resources/", views.resources, name="resources"),
    path("resources/add/", views.resources_add, name="resources_add"),
    path("resources/edit/", views.resources_edit, name="resources_edit"),
    path("resources/delete/", views.resources_delete, name="resources_delete"),

    path("locations/", views.locations, name="locations"),
    path("locations/add/", views.locations_add, name="locations_add"),
    path("locations/edit/", views.locations_edit, name="locations_edit"),
    path("locations/delete/", views.locations_delete, name="locations_delete"),

    path("contacts/", views.contacts, name="contacts"),
    path("contacts/add/", views.contacts_add, name="contacts_add"),
    path("contacts/edit/", views.contacts_edit, name="contacts_edit"),
    path("contacts/delete/", views.contacts_delete, name="contacts_delete"),

    path("schedules/", views.schedules, name="schedules"),
    path("schedules/add/", views.schedules_add, name="schedules_add"),
    path("schedules/delete/", views.schedules_delete, name="schedules_delete"),
]
