import datetime

from cron_validator import CronValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from phone_field import PhoneField
from taggit.managers import TaggableManager


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __repr__(self) -> str:
        return f"<Region: {str(self)}>"

    def __str__(self) -> str:
        return str(self.name)


class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self) -> str:
        return reverse("info:organisation", kwargs={"org": self.slug})

    def __repr__(self) -> str:
        return f"<Organisation: {str(self)}>"

    def __str__(self) -> str:
        return str(self.name)


class Location(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name="locations")
    name = models.CharField(max_length=255)
    address = models.TextField()
    post_code = models.CharField(max_length=10)

    def __repr__(self) -> str:
        return f"<Location: {str(self)}>"

    def __str__(self) -> str:
        return str(self.name)


class Contact(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = PhoneField(blank=True, help_text="Contact phone number")

    def __repr__(self) -> str:
        return f"<Contact: {str(self)}>"

    def __str__(self) -> str:
        if self.phone_number:
            return f"{self.name}: {self.email} - {self.phone_number}"

        return f"{self.name}: {self.email}"


class Resource(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    tags = TaggableManager(blank=True)

    def get_absolute_url(self) -> str:
        return reverse("info:resource", kwargs={"pk": self.pk})

    def get_list_url(self) -> str:
        return reverse("info:resources")

    def __repr__(self) -> str:
        return f"<Resource: {str(self)}>"

    def __str__(self) -> str:
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
    schedules = models.ManyToManyField("Scheduler", related_name="events", blank=True)

    tags = TaggableManager(blank=True)

    class Meta:
        unique_together = ["start_date_time", "location"]

    @property
    def format_duration(self) -> str:
        total_seconds = int((self.end_date_time - self.start_date_time).total_seconds())
        hours, remainder = divmod(total_seconds, 60*60)
        minutes, _ = divmod(remainder, 60)

        return f"{hours} hrs, {minutes} mins"

    @property
    def ends_today(self) -> bool:
        now = timezone.now()

        return all([
            self.schedules,
            now.year == self.end_date_time.year,
            now.month == self.end_date_time.month,
            now.day == self.end_date_time.day,
        ])

    def get_absolute_url(self) -> str:
        return reverse("info:event", kwargs={"pk": self.pk})

    def get_list_url(self) -> str:
        return reverse("info:events")

    def __repr__(self) -> str:
        return f"<Event: {str(self)}>"

    def __str__(self) -> str:
        return f"{self.organisation.name}: {self.name} @ {self.start_date_time}"


class Scheduler(models.Model):
    label = models.CharField(max_length=255, default="")
    cron = models.CharField(max_length=64, default="* * * * *")

    def clean(self, *args, **kwargs) -> None:
        try:
            CronValidator.parse(self.cron)

        except ValueError:
            raise ValidationError({"cron": "Invalid cron expression"})

    def __repr__(self) -> str:
        return f"<Schedule: {str(self)}>"

    def __str__(self) -> str:
        return f"{self.label}: {self.cron}"
