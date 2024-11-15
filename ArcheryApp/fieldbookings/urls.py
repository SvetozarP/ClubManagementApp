from django.urls import path

from ArcheryApp.fieldbookings.views import bookings

urlpatterns = [
    path('', bookings, name='bookings'),
]
