from django.db import models

from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.membership.models import MemberProfile


# Create your models here.

class ShootSessionDetails(models.Model):

    class Meta:
        verbose_name = 'Shoot Session Details'

    archer = models.ForeignKey(
        to=MemberProfile,
        on_delete=models.CASCADE,
        related_name='shoot_session_details',
        blank=False,
        null=False,
    )

    shoot_session = models.OneToOneField(
        to=FieldBookings,
        on_delete=models.CASCADE,
        related_name='shoot_session_details',
        blank=False,
        null=False,
    )

    details = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )