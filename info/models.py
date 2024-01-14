import time

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from phone_field import PhoneField


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __repr__(self):
        return f"<Region: {str(self)}>"

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    post_code = models.CharField(max_length=10)

    def __repr__(self):
        return f"<Location: {str(self)}>"

    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse("organisation", kwargs={"org": self.slug})

    def __repr__(self):
        return f"<Organisation: {str(self)}>"

    def __str__(self):
        return self.name

class Contact(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = PhoneField(blank=True, help_text='Contact phone number')

    def __repr__(self):
        return f"<Contact: {str(self)}>"

    def __str__(self):
        if self.phone_number:
            return f"{self.name}: {self.email} - {self.phone_number}"

        return f"{self.name}: {self.email}"

class Resource(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    @property
    def type(self):
        return "Resource"

    def get_absolute_url(self):
        return reverse("resource", kwargs={"resource_id": self.id})

    def get_list_url(self):
        return reverse("resources")

    def __repr__(self):
        return f"<Resource: {str(self)}>"

    def __str__(self):
        return f"{self.organisation.name}: {self.name}"

class Event(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="GBP")
    ticketed = models.BooleanField(default=False)
    tickets = models.IntegerField(default=0)
    tickets_purchased = models.IntegerField(default=0)

    @property
    def type(self):
        return "Resource"

    def format_duration(self):
        total_seconds = int((self.end_date_time - self.start_date_time).total_seconds())
        hours, remainder = divmod(total_seconds, 60*60)
        minutes, _ = divmod(remainder, 60)

        return f"{hours} hrs, {minutes} mins"

    def get_absolute_url(self):
        return reverse("event", kwargs={"event_id": self.id})

    def get_list_url(self):
        return reverse("events")

    def __repr__(self):
        return f"<Event: {str(self)}>"

    def __str__(self):
        return f"{self.organisation.name}: {self.name}"
