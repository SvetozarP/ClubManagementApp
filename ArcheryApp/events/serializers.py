from rest_framework import serializers

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.fieldbookings.models import FieldBookings


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvents
        fields = ['start_date', 'end_date', 'event_description']


class FieldBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldBookings
        fields = ['date', 'time_from', 'time_to']

class CombinedBookingSerializer(serializers.Serializer):
    bookings = serializers.SerializerMethodField()
    field_bookings = serializers.SerializerMethodField()

    @staticmethod
    def get_bookings(self, obj):
        bookings = ClubEvents.objects.all()
        return BookingSerializer(bookings, many=True).data

    @staticmethod
    def get_field_bookings(self, obj):
        field_bookings = FieldBookings.objects.all()
        return FieldBookingSerializer(field_bookings, many=True).data