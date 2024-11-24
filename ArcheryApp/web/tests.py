from decouple import config
from django.test import TestCase

# Create your tests here.


import cloudinary.uploader

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

response = cloudinary.uploader.upload("../../mediafiles/mediafiles/croesoswalltintro.webp")
print(response['url'])  # This should print the uploaded image URL