from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Contact


class ContactList(ListView):
    model = Contact
    ordering = ["-id"]


class ContactCreate(CreateView):
    model = Contact
    fields = ["name", "email", "phone"]
    success_url = reverse_lazy("contact_list")


class ContactUpdate(UpdateView):
    model = Contact
    fields = ["name", "email", "phone"]
    success_url = reverse_lazy("contact_list")


class ContactDelete(DeleteView):
    model = Contact
    success_url = reverse_lazy("contact_list")

    # Create your views here.
