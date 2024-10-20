from .contacts import ContactCreateView, ContactDeleteView, ContactDetailView, ContactListView, ContactUpdateView
from .events import (
    DashboardEventCreateView,
    DashboardEventDeleteView,
    DashboardEventListView,
    DashboardEventUpdateView,
    EventDetailView,
    EventListView,
    OrganisationEventListView
)
from .index import IndexView, favicon
from .locations import LocationCreateView, LocationDeleteView, LocationDetailView, LocationListView, LocationUpdateView
from .organisations import (
    DashboardOrganisationCreateView,
    DashboardOrganisationView,
    DashboardOrganisationUpdateView,
    OrganisationDetailView,
    OrganisationListView
)
from .profile import DashboardUserView, UserCreateView
from .reminder import ReminderCreateView
from .schedule import (
    DashboardiCalScheduleCreateView,
    DashboardiCalScheduleDeleteView,
    DashboardiCalScheduleListView,
    DashboardiCalScheduleUpdateView,
)
from .volunteer import volunteer
