from .contacts import ContactCreateView, ContactDeleteView, ContactDetailView, ContactListView, ContactUpdateView
from .dashboard import dashboard_organisation
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
    OrganisationDetailView,
    OrganisationListView
)
from .profile import DashboardUserView, UserCreateView
from .resources import (
    DashboardResourceCreateView,
    DashboardResourceDeleteView,
    DashboardResourceListView,
    DashboardResourceUpdateView,
    OrganisationResourceListView,
    ResourceDetailView,
    ResourceListView
)
