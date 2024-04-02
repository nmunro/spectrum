from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import models


class ContactListView(ListView):
    model = models.Contact
    paginate_by = 100
    context_object_name = "contacts"

    def get_queryset(self, **kwargs):
        return models.Contact.objects.filter(organisation__admin=self.request.user).order_by("contact_name")

class ContactCreateView(CreateView):
    model = models.Contact
    fields = [
        "organisation",
        "contact_name",
        "email",
        "phone_number",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_contacts")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class ContactUpdateView(UpdateView):
    model = models.Contact
    fields = [
        "organisation",
        "contact_name",
        "email",
        "phone_number",
    ]

    def get_success_url(self) -> str:
        return reverse_lazy("info:dashboard_contacts")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["organisation"].queryset = models.Organisation.objects.filter(admin=self.request.user)
        return form


class ContactDetailView(DetailView):
    model = models.Contact


class ContactDeleteView(DeleteView):
    model = models.Contact
    success_url = reverse_lazy("info:dashboard_contacts")
