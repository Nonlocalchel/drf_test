import io
import os
import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile, SimpleUploadedFile


def get_temp_file():
    return tempfile.mkdtemp(suffix=None, prefix=None, dir=None)


def open_photo_file(path):
    photo_file = open(path, 'rb') #<_io.BytesIO object at 0x000002416840FC40>
    mem_file = InMemoryUploadedFile(photo_file, field_name='photo', name='img_2.jpg',
                                    content_type='image/jpeg',
                                    charset=None, size=os.path.getsize(path))
    return mem_file


def close_photo_file(file):
    if file.closed:
        return

    file.close()
