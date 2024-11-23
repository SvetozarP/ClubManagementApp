from django.db import models
from simple_history.models import HistoricalRecords

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator


# Create your models here.

class ClubMission(models.Model):

    class Meta:
        verbose_name_plural = "Club Mission"

    image_url = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
        ]
    )

    mission_text = models.TextField()

    history = HistoricalRecords()

    def __str__(self):
        return f"Mission: {self.mission_text}"


class ClubHistory(models.Model):
    HISTORY_MAX_TITLE_LEN = 100

    class Meta:
        verbose_name_plural = "Club History"

    image = models.ImageField(
        upload_to = 'history/',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
        ],
        blank=True,
        null=True,
    )

    history_title = models.CharField(
        max_length=HISTORY_MAX_TITLE_LEN
    )

    history_text = models.TextField()

    history = HistoricalRecords()

    def __str__(self):
        return f"History: {self.history_title}"


class MembershipInfo(models.Model):
    MAX_PICTURE_SIZE = 5 * 1024 * 1024
    PICTURE_ALLOWED_FORMATS = ['jpeg', 'png', 'gif', 'webp']

    class Meta:
        verbose_name_plural = "Membership Information"

    description = models.TextField()
    image = models.ImageField(
        upload_to = 'membershipinfo/',
        validators=[
            PhotoSizeValidator(max_size=MAX_PICTURE_SIZE),
            PhotoTypeValidator(allowed_formats=PICTURE_ALLOWED_FORMATS),
        ],
        blank=True,
        null=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'Last updated: {self.updated_on}'

class Testimonials(models.Model):
    CUSTOMER_MAX_LEN = 100

    class Meta:
        verbose_name_plural = "Testimonials"

    text = models.TextField()
    customer = models.CharField(
        max_length=CUSTOMER_MAX_LEN
    )

    date_given = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.customer} - {self.date_given}'


class ContactRequest(models.Model):
    NAME_MAX_LEN = 100

    class Meta:
        verbose_name_plural = "Contact Requests"

    name = models.CharField(
        max_length=NAME_MAX_LEN,
    )
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_answered = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Message from {self.name} ({self.email})"