from django.urls import path

from ArcheryApp.fieldbookings.views import CreateFieldBookingsView, ListBookingsView, create_event

urlpatterns = [
    path('', CreateFieldBookingsView.as_view(), name='create-booking'),
    path('list/', ListBookingsView.as_view(), name='list-bookings'),
    path('create/<str:date>', create_event, name='create_date_booking')
]
