from django.urls import path

from ArcheryApp.events.views import calendar_view, CalendarAPIView

urlpatterns = [
    path('api/combined-bookings/', CalendarAPIView.as_view(), name='combined-bookings'),
    path('calendar/', calendar_view, name='calendar-view'),
]