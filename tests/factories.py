from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import factory

from info import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))
    is_staff = True
    is_superuser = True

class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Region

    name = "North Yorkshire"

class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Location

    name = factory.Faker("name")
    address = factory.Faker("address")
    post_code = "YO12 7YU"

class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organisation

    name = factory.Faker("name")
    region = factory.SubFactory(RegionFactory)
    email = factory.Faker("email")
    website = factory.LazyAttribute(lambda o: f"{o.name}.something.com")
    description = factory.LazyAttribute(lambda o: o.name)
    admin = factory.SubFactory(UserFactory)

class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Contact

    organisation = factory.SubFactory(OrganisationFactory)
    name = factory.Faker("name")
    email = factory.Faker("email")

class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Resource

    organisation = factory.SubFactory(OrganisationFactory)
    name = factory.Faker("name")
    description = factory.LazyAttribute(lambda o: o.name)

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    organisation = factory.SubFactory(OrganisationFactory)
    contact = factory.SubFactory(ContactFactory)
    location = factory.SubFactory(LocationFactory)
    name = factory.Faker("name")
    description = factory.LazyAttribute(lambda o: o.name)
    price = factory.Sequence(lambda n: n)
    start_date_time = timezone.now()
    end_date_time = timezone.now() + timedelta(hours=2)

class SchedulerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Scheduler

    event = factory.SubFactory(EventFactory)
    cron = "* * * * *"
