import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageCreator:
    """Create fake images for create data on django orm"""

    @staticmethod
    def get_fake_image_miniature():
        """Create fake miniature img"""
        image = io.BytesIO()
        Image.new('RGB', (150, 150)).save(image, 'JPEG')
        image.seek(0)
        min_file = SimpleUploadedFile('image.jpg', image.getvalue())
        return min_file

    @staticmethod
    def get_fake_image():
        """Create fake image"""
        image = io.BytesIO()
        Image.new('RGB', (1152, 2048)).save(image, 'JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('image2.jpg', image.getvalue())
        return image_file
