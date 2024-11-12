from django.core.exceptions import ValidationError
from PIL import Image

class PhotoSizeValidator:
    def __init__(self, max_size=5 * 1024 * 1024):  # Default is 5 MB
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(f"File size should not exceed {self.max_size / (1024 * 1024)} MB.")


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