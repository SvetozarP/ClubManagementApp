from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.deconstruct import deconstructible
import re
from django.utils.translation import gettext as _



@deconstructible
class PhotoSizeValidator:
    def __init__(self, max_size=5 * 1024 * 1024):  # Default is 5 MB
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(f"File size should not exceed {self.max_size / (1024 * 1024)} MB.")

@deconstructible
class PhotoTypeValidator:
    def __init__(self, allowed_formats=None):
        if allowed_formats is None:
            allowed_formats = ['jpeg', 'png', 'gif', 'webp']  # Default formats
        self.allowed_formats = allowed_formats

    def __call__(self, value):
        try:
            # Open the image to check its format
            img = Image.open(value)
            img_format = img.format.lower()

            if img_format not in self.allowed_formats:
                raise ValidationError(f"Unsupported image format. Allowed formats are: {', '.join(self.allowed_formats)}.")
        except Exception:
            raise ValidationError("Invalid image file.")


class ArcheryAppPasswordValidator:

    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                _("The password must be at least 10 characters long."),
                code='password_too_short',
            )

        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit',
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _("The password must contain at least one special character."),
                code='password_no_special',
            )

        if user:
            if user.username.lower() in password.lower():
                raise ValidationError(
                    _("The password must not be similar to your username."),
                    code='password_like_username',
                )

        common_words = ['password', '123456', 'qwerty', 'letmein', 'admin']
        if any(word in password.lower() for word in common_words):
            raise ValidationError(
                _("The password is too similar to a common dictionary word."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 10 characters long, contain one uppercase letter, "
            "one digit, one special character, and must not be similar to your username or a "
            "common dictionary word."
        )