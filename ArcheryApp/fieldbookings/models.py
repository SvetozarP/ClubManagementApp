from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from ArcheryApp.common.choices import FieldDistanceChoices
from ArcheryApp.membership.models import MemberProfile


# Create your models here.
# Adds functionality for future - field can be configured with lanes and distances
class FieldConfiguration(models.Model):
    MAX_DISTANCE_FIELD_LEN = 9

    lane_no = models.IntegerField(
        blank=False,
        null=False,
    )

    distance = models.CharField(
        max_length=MAX_DISTANCE_FIELD_LEN,
        choices=FieldDistanceChoices,
        blank=True,
        null=True,
    )

    max_archers = models.IntegerField(
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

# List of bookings for shooting
class FieldBookings(models.Model):

    class Meta:
        verbose_name_plural = "Field Bookings"

    archer = models.ForeignKey(
        to=MemberProfile,
        on_delete=models.CASCADE,
        related_name='field_bookings',
        blank=False,
        null=False,
    )

    lane = models.ForeignKey(
        to=FieldConfiguration,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    date = models.DateField(
        blank=False,
        null=False,
    )

    time_from = models.TimeField(
        blank=False,
        null=False,
    )

    time_to = models.TimeField(
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.date} {self.time_from} - {self.time_to}"


    @property
    def is_active(self):
        event_datetime = datetime.combine(self.date, self.time_to)
        return event_datetime >= datetime.now()

    def clean(self):
        """
        Validates that time_from is before time_to.
        """
        if self.time_from and self.time_to and self.time_from >= self.time_to:
            raise ValidationError({
                'time_from': 'Start time must be before the end time.',
                'time_to': 'End time must be after the start time.',
            })