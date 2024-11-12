from django.db import models

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator


# Create your models here.

class ClubMission(models.Model):

    image_url = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
        ]
    )

    mission_text = models.TextField()


class ClubHistory(models.Model):

    history_title = models.CharField(
        max_length=100
    )

    history_text = models.TextField()
