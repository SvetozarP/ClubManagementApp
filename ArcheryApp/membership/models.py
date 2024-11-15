from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator
from ArcheryApp.membership.managers import MemberProfileManager


class MemberProfile(AbstractBaseUser, PermissionsMixin):
    MAX_PHONE_NO_LEN = 11
    USERNAME_MAX_LEN = 150
    CSRF_MAX_LEN = 64
    NAME_MAX_LEN = 50
    MAX_PICTURE_SIZE = 5 * 1024 * 1024
    PICTURE_ALLOWED_FORMATS = ['jpeg', 'png', 'gif', 'webp']

    email = models.EmailField(
        unique=True
    )

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True,
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=NAME_MAX_LEN,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=NAME_MAX_LEN,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    csrf_token = models.CharField(
        max_length=CSRF_MAX_LEN,
        blank=True,
        null=True
    )

    is_registered = models.BooleanField(
        default=False
    )

    phone_number = models.CharField(
        max_length=MAX_PHONE_NO_LEN,
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    image = models.ImageField(
        upload_to = 'mediafiles/',
        validators=[
            PhotoSizeValidator(max_size=MAX_PICTURE_SIZE),
            PhotoTypeValidator(allowed_formats=PICTURE_ALLOWED_FORMATS),
        ]
    )

    profile_completed = models.BooleanField(
        default=False,
    )

    objects = MemberProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def generate_csrf_token(self):
        self.csrf_token = get_random_string(64)
        self.save()

    def clear_csrf_token(self):
        self.csrf_token = None
        self.save()