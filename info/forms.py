from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Organisation


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = [
            "description",
            "region",
            "email",
            "website",
            "phone_number",
            "enable_scheduler",
            "accepting_volunteers",
        ]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class VolunteerForm(forms.Form):
    organisation = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(label="Your Name", max_length=255)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())
