from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string


class MemberProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class MemberProfile(AbstractBaseUser, PermissionsMixin):
    MAX_PHONE_NO_LEN = 11
    USERNAME_MAX_LEN = 150
    CSRF_MAX_LEN = 64
    NAME_MAX_LEN = 50

    email = models.EmailField(
        unique=True
    )

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True
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

    objects = MemberProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_csrf_token(self):
        self.csrf_token = get_random_string(64)
        self.save()

    def clear_csrf_token(self):
        self.csrf_token = None
        self.save()