import io
import json
import tempfile

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.conf import settings


class ManipulateExpectedDataMixin:
    expected_data_path = ''

    def get_expected_data(self) -> list:
        path = self.expected_data_path
        with open(path) as expected_data_file:
            expected_data = json.loads(expected_data_file.read())
            return expected_data

    def write_data_to_json_file(self, new_data) -> None:
        path = self.expected_data_path
        with open(path, 'w') as expected_data_file:
            expected_data_file.write(json.dumps(new_data))


class CreateImageMixin:
    def set_media_root(self):
        settings.MEDIA_ROOT = self.temp_file

    @property
    def temp_file(self):
        return tempfile.mkdtemp(suffix=None, prefix=None, dir=None)

    @property
    def fake_image_miniature(self):
        image = io.BytesIO()
        Image.new('RGB', (150, 150)).save(image, 'JPEG')
        image.seek(0)
        min_file = SimpleUploadedFile('image.jpg', image.getvalue())
        return min_file

    @property
    def fake_image(self):
        image = io.BytesIO()
        Image.new('RGB', (1152, 2048)).save(image, 'JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('image2.jpg', image.getvalue())
        return image_file
