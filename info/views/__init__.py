from .contacts import ContactCreateView, ContactDeleteView, ContactDetailView, ContactListView, ContactUpdateView
from .dashboard import DashboardView, dashboard_org
from .events import (
    DashboardEventCreateView,
    DashboardEventDeleteView,
    DashboardEventListView,
    DashboardEventUpdateView,
    EventDetailView,
    EventListView,
)
from .index import IndexView, favicon
from .locations import LocationCreateView, LocationDeleteView, LocationDetailView, LocationListView, LocationUpdateView
from .organisations import organisation, organisation_events, organisation_resources, organisations
from .resources import (
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListview,
    ResourceUpdateView,
    resources
)
