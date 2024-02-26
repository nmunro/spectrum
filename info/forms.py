from django.forms import ModelForm, DateTimeInput
from .models import Contact, Event, Organisation, Resource, Location


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
            'organisation',
            'name',
            'email',
            'phone_number',
        ]

class OrgForm(ModelForm):
    class Meta:
        model = Organisation
        fields = ['description', 'region', 'email', 'website']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'organisation',
            'name',
            'description',
            'location',
            'contact',
            'ticketed',
            'start_date_time',
            'end_date_time',
            'price',
            'tags',
        ]


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = [
            'organisation',
            'name',
            'description',
            'tags',
        ]


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = [
            'organisation',
            'name',
            'address',
            'post_code',
        ]
