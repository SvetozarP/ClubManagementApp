from django.db import models
from simple_history.models import HistoricalRecords
from cloudinary.models import CloudinaryField

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator
from ArcheryApp.membership.models import MemberProfile


# Create your models here.
# ClubMission holds information about the Club mission part of the landing page. This can be modified by the SuperUser
class ClubMission(models.Model):

    class Meta:
        verbose_name_plural = "Club Mission"

    # Had to convert to Cloudinary as Superhosting does not support mediafiles over HTTPS
    # image_url = models.ImageField(
    #     upload_to = 'mediafiles/',
    #     validators=[
    #         PhotoSizeValidator(max_size=5 * 1024 * 1024),
    #         PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
    #     ]
    # )

    image_url = CloudinaryField(
        'image_url',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp']),
        ],
        blank=True,
        null=True
    )

    mission_text = models.TextField()

    history = HistoricalRecords()

    def __str__(self):
        return f"Mission: {self.mission_text}"

# Information about club history. All separate entries create their own section in club history, which then gets
# different style for odd and even.
class ClubHistory(models.Model):
    HISTORY_MAX_TITLE_LEN = 100

    class Meta:
        verbose_name_plural = "Club History"

    # Convert to Cloudinary field.
    # image = models.ImageField(
    #     upload_to = 'history/',
    #     validators=[
    #         PhotoSizeValidator(max_size=5 * 1024 * 1024),
    #         PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
    #     ],
    #     blank=True,
    #     null=True,
    # )

    image = CloudinaryField(
        'image',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp']),
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

# Membership info - show people how to become members and give option to contact the club. If user has token, option to
# Register account.
class MembershipInfo(models.Model):

    class Meta:
        verbose_name_plural = "Membership Information"

    description = models.TextField()
    # Convert to Cloudinary field
    # image = models.ImageField(
    #     upload_to = 'membershipinfo/',
    #     validators=[
    #         PhotoSizeValidator(max_size=MAX_PICTURE_SIZE),
    #         PhotoTypeValidator(allowed_formats=PICTURE_ALLOWED_FORMATS),
    #     ],
    #     blank=True,
    #     null=True,
    # )

    image = CloudinaryField(
        'image',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp']),
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

# Hold info for any testimonials collected from participants in events / beginners courses / sessions and display in the
# main landing page. This can be modified by SuperUser.
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


# Hold information about any contact requests. One-to-One with HandleContactRequests and mark answered ones
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


# One-to-One with Contact requests - record who answered the request, when and what was done over the request
class HandleContactRequest(models.Model):

    class Meta:
        verbose_name_plural = "Request answers"

    action_by = models.ForeignKey(
        to=MemberProfile,
        on_delete=models.CASCADE,
        related_name='handled_contact_requests',
    )

    contact_request = models.ForeignKey(
        to=ContactRequest,
        on_delete=models.CASCADE,
        related_name='handled_contact_requests',
    )

    action_taken = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )