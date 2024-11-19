from rest_framework import serializers

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.fieldbookings.models import FieldBookings


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvents
        fields = ['start_date', 'end_date', 'event_description', 'id']


class FieldBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldBookings
        fields = ['date', 'time_from', 'time_to']
