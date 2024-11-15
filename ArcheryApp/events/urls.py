from django.urls import path

from ArcheryApp.events.views import CombinedBookingView, calendar_view

urlpatterns = [
    path('api/combined-bookings/', CombinedBookingView.as_view(), name='combined-bookings'),
    path('calendar/', calendar_view, name='calendar-view'),
]