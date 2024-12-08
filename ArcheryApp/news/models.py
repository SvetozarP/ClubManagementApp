from django.db import models
from cloudinary.models import CloudinaryField

from ArcheryApp.membership.models import MemberProfile
from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator


# Create your models here.
# Club news model
class ClubNews(models.Model):

    class Meta:
        verbose_name_plural = "Club News"

    title = models.CharField(
        max_length=100
    )

    # Converted to Cloudinary
    # image = models.ImageField(
    #     upload_to = 'clubnews/',
    #     validators=[
    #         PhotoSizeValidator(max_size=5 * 1024 * 1024),
    #         PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp']),
    #     ]
    # )

    image = CloudinaryField(
        'image',
        validators=[
            PhotoSizeValidator(max_size=5 * 1024 * 1024),
            PhotoTypeValidator(allowed_formats=['jpeg', 'png', 'gif', 'webp'])
        ],
        null=True,
        blank=True,
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

    def __str__(self):
        return f'{self.title} - {self.created_at}'

# Announcements model
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

    def __str__(self):
        return f'{self.title}'