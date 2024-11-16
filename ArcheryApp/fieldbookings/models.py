from datetime import datetime

from django.db import models

from ArcheryApp.common.choices import FieldDistanceChoices
from ArcheryApp.membership.models import MemberProfile


# Create your models here.
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


class FieldBookings(models.Model):

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