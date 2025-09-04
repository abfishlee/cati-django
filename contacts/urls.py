from django.urls import path

from .views import ContactCreate, ContactDelete, ContactList, ContactUpdate

urlpatterns = [
    path("", ContactList.as_view(), name="contact_list"),
    path("new/", ContactCreate.as_view(), name="contact_create"),
    path("<int:pk>/edit/", ContactUpdate.as_view(), name="contact_update"),
    path("<int:pk>/delete/", ContactDelete.as_view(), name="contact_delete"),
]
