from django.db import models

from ArcheryApp.membership.models import MemberProfile
from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator


# Create your models here.

class ClubEvents(models.Model):
    MAX_TITLE_LENGTH = 100
    MAX_PICTURE_SIZE = 5 * 1024 * 1024
    PICTURE_ALLOWED_FORMATS = ['jpeg', 'png', 'gif', 'webp']
    MAX_HOSTED_BY_LEN = 255

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    image = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=MAX_PICTURE_SIZE),
            PhotoTypeValidator(allowed_formats=PICTURE_ALLOWED_FORMATS),
        ]
    )

    hosted_by = models.CharField(
        max_length=MAX_HOSTED_BY_LEN,
        blank=True,
        null=True,
    )

    event_description = models.TextField(
        blank=True,
        null=True,
    )

    author = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
    )

    participants = models.ManyToManyField(
        MemberProfile,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.event_description
