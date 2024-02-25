from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .. import forms
from .. import models


class ContactListView(ListView):
    model = models.Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = models.Contact.objects.filter(organisation__admin=self.request.user)

        return context

class ContactCreateView(CreateView):
    model = models.Contact
    fields = [
        'organisation',
        'name',
        'email',
        'phone_number',
    ]

    def get_success_url(self):
        return reverse_lazy('dashboard_contacts')


class ContactUpdateView(UpdateView):
    model = models.Contact
    fields = [
        'organisation',
        'name',
        'email',
        'phone_number',
    ]

    def get_success_url(self):
        return reverse_lazy('dashboard_contacts')


class ContactDetailView(DetailView):
    model = models.Contact


class ContactDeleteView(DeleteView):
    model = models.Contact
    success_url = reverse_lazy("dashboard_contacts")
