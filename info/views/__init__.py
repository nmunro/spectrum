from .contacts import ContactCreateView, ContactDeleteView, ContactDetailView, ContactListView, ContactUpdateView
from .dashboard import DashboardView, dashboard_org
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
from .organisations import OrganisationDetailView, OrganisationListView
from .resources import (
    DashboardResourceCreateView,
    DashboardResourceDeleteView,
    DashboardResourceListview,
    DashboardResourceUpdateView,
    OrganisationResourceListView,
    ResourceDetailView,
    ResourceListView
)
