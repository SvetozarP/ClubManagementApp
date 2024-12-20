import uuid
from datetime import timedelta
from cloudinary.models import CloudinaryField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator
from ArcheryApp.membership.managers import MemberProfileManager

# We need to ensure that email cannot be repeated. This cannot happen through unique in the model due to the logic of
# creating user and resetting password. Ambiguous error message returned for security reasons.
def validate_unique_email(value):
    if MemberProfile.objects.filter(email=value,profile_completed=True).exists():
        raise ValidationError(
            'Please enter valid email.',
            params={'value': value},
        )

# Custom user model, inherits and extends AbstractBaseUser.
class MemberProfile(AbstractBaseUser, PermissionsMixin):
    MAX_PHONE_NO_LEN = 11
    USERNAME_MAX_LEN = 150
    USERNAME_MIN_LEN = 5
    CSRF_MAX_LEN = 64
    NAME_MAX_LEN = 50

    email = models.EmailField(
        validators=[validate_unique_email],
        #unique=True
    )

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        validators=[
            MinLengthValidator(USERNAME_MIN_LEN),
        ],
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

    # image = models.ImageField(
    #     upload_to = 'mediafiles/',
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

    profile_completed = models.BooleanField(
        default=False,
    )

    reset_token = models.UUIDField(
        null=True,
        blank=True,
    )

    reset_token_expiry = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_reset_request = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = MemberProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Methods for generating CSRF and reset tokens
    def generate_csrf_token(self):
        self.csrf_token = get_random_string(64)
        self.save()

    def clear_csrf_token(self):
        self.csrf_token = None
        self.save()

    def generate_reset_token(self):
        # Prevent multiple requests within an hour
        if self.last_reset_request and self.last_reset_request > now() - timedelta(hours=1):
            raise Exception("You can only request a reset token once per hour.")

        self.reset_token = uuid.uuid4()
        self.reset_token_expiry = now() + timedelta(days=1)
        self.last_reset_request = now()
        self.save()

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expiry = None
        self.save()