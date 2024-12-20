from django.urls import path

from ArcheryApp.events.views import calendar_view, CalendarAPIView, EventsListView, PastEventsView, EventDetailsView, \
    CreateNewEventView, UpdateEventView, participation_functionality

urlpatterns = [
    path('api/combined-bookings/', CalendarAPIView.as_view(), name='combined-bookings'),
    path('calendar/', calendar_view, name='calendar-view'),
    path('', EventsListView.as_view(), name='club-events'),
    path('past-events/', PastEventsView.as_view(), name='club-past-events'),
    path('create/', CreateNewEventView.as_view(), name='club-create-event'),
    path('<int:pk>/detail/', EventDetailsView.as_view(), name='club-event-detail'),
    path('<int:pk>/edit/', UpdateEventView.as_view(), name='club-event-update'),
    path('<int:pk>/participate/', participation_functionality, name='club-event-participate'),
]