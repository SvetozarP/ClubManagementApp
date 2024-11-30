from django.core.exceptions import ValidationError
from django.test import TestCase
from io import BytesIO
from PIL import Image

import sys
import tempfile

from ArcheryApp.common.validators import PhotoSizeValidator, PhotoTypeValidator, ArcheryAppPasswordValidator


class TestPhotoSizeValidator(TestCase):
    #Arrange, Act and assert in one - Init the validator, simulate file, pass through validation
    def test_valid_size(self):
        validator = PhotoSizeValidator(max_size=2 * 1024 * 1024)  # 2 MB
        file = tempfile.NamedTemporaryFile()
        file.write(b"x" * (1 * 1024 * 1024))  # 1 MB file
        file.seek(0)
        file.size = len(file.read())
        validator(file)  # Should pass without exception

    def test_invalid_size(self):
        validator = PhotoSizeValidator(max_size=2 * 1024 * 1024)  # 2 MB
        file = tempfile.NamedTemporaryFile()
        file.write(b"x" * (3 * 1024 * 1024))  # 3 MB file
        file.seek(0)
        file.size = len(file.read())
        with self.assertRaises(ValidationError):
            validator(file) #We should see validation error

class TestPhotoTypeValidator(TestCase):
    #Arrange
    def create_image_file(self, format='JPEG'):
        img = Image.new('RGB', (100, 100), color='red') #Create the image
        temp_file = BytesIO() # Create file in the memory
        img.save(temp_file, format=format) #Save the image
        temp_file.seek(0) #retutn pointer to 0
        temp_file.size = len(temp_file.getvalue()) #Retrieve the size of the file
        temp_file.file = temp_file  # Mimic Django file structure
        return temp_file #Return the created file (image)
    #Act and assert
    def test_valid_image_format(self):
        validator = PhotoTypeValidator(allowed_formats=['jpeg', 'png'])
        image_file = self.create_image_file('JPEG')
        validator(image_file)  # Pass

    def test_invalid_image_format(self):
        validator = PhotoTypeValidator(allowed_formats=['jpeg', 'png'])
        image_file = self.create_image_file('BMP')
        with self.assertRaises(ValidationError):
            validator(image_file) # validation error expected

    def test_invalid_image_content(self):
        validator = PhotoTypeValidator()
        invalid_file = BytesIO(b"Not an image")
        invalid_file.file = invalid_file
        with self.assertRaises(ValidationError):
            validator(invalid_file) #Invalid file exception

class TestArcheryAppPasswordValidator(TestCase):
    #Arrange
    def setUp(self):
        self.validator = ArcheryAppPasswordValidator()
    #Act and Assert
    def test_valid_password(self):
        valid_password = "Valid1Lkdjfldkjflkj!"
        self.validator.validate(valid_password)

    def test_short_password(self):
        short_password = "Short1!"
        with self.assertRaises(ValidationError):
            self.validator.validate(short_password)

    def test_no_uppercase(self):
        no_upper = "password123!"
        with self.assertRaises(ValidationError):
            self.validator.validate(no_upper)

    def test_no_digit(self):
        no_digit = "Password!"
        with self.assertRaises(ValidationError):
            self.validator.validate(no_digit)

    def test_no_special_character(self):
        no_special = "Password123"
        with self.assertRaises(ValidationError):
            self.validator.validate(no_special)

    def test_password_like_username(self):
        class MockUser:
            username = "archer"

        user = MockUser()
        similar_password = "archer123!"
        with self.assertRaises(ValidationError):
            self.validator.validate(similar_password, user)

    def test_common_password(self):
        common_password = "password123!"
        with self.assertRaises(ValidationError):
            self.validator.validate(common_password)
