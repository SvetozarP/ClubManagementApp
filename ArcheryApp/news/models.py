from django.db import models

from ArcheryApp.membership.models import MemberProfile
from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator


# Create your models here.

class ClubNews(models.Model):

    title = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp']),
        ]
    )

    news_text = models.TextField()

    author = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True,
    )


class ClubAnnouncements(models.Model):
    MAX_TITLE_LENGTH = 100

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to=MemberProfile,
        related_name='announcements',
        on_delete=models.CASCADE,
    )

    read_by = models.ManyToManyField(
        to=MemberProfile,
        related_name='read_announcements',
        blank=True,
    )