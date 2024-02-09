from django.forms import ModelForm, DateTimeInput
from .models import Contact, Event, Organisation, Resource, Location


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
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
            'name',
            'description',
            'location',
            'contact',
            'start_date_time',
            'end_date_time',
            'price',
        ]

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description']


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'post_code']
