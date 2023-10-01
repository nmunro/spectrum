import time

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from djmoney.models.fields import MoneyField


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    post_code = models.CharField(max_length=10)

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

    def __str__(self):
        return self.name

class Resource(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse("resource", kwargs={"resource_id": self.id})

    def __repr__(self):
        return f"<Resource: {str(self)}>"

    def __str__(self):
        return f"{self.organisation.name}: {self.name}"

class Event(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="GBP")
    ticketed = models.BooleanField(default=False)
    tickets = models.IntegerField(default=0)
    tickets_purchased = models.IntegerField(default=0)

    def format_duration(self):
        res = time.gmtime(self.duration.seconds)
        return time.strftime("%-H hours, %-M minutes", res)

    def get_absolute_url(self):
        return reverse("event", kwargs={"event_id": self.id})

    def __repr__(self):
        return f"<Event: {str(self)}>"

    def __str__(self):
        return f"{self.organisation.name}: {self.name}"
