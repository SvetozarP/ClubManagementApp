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
    HISTORY_MAX_TITLE_LEN = 100

    history_title = models.CharField(
        max_length=HISTORY_MAX_TITLE_LEN
    )

    history_text = models.TextField()


class MembershipInfo(models.Model):
    MAX_PICTURE_SIZE = 5 * 1024 * 1024
    PICTURE_ALLOWED_FORMATS = ['jpeg', 'png', 'gif', 'webp']

    description = models.TextField()
    image_url = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=MAX_PICTURE_SIZE),
            PhotoTypeValidator(allowed_formats=PICTURE_ALLOWED_FORMATS),
        ]
    )


class Testimonials(models.Model):
    CUSTOMER_MAX_LEN = 100

    text = models.TextField()
    customer = models.CharField(
        max_length=CUSTOMER_MAX_LEN
    )

    date_given = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )