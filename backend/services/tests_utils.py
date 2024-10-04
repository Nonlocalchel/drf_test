import tempfile


def get_temp_file():
    return tempfile.mkdtemp(suffix=None, prefix=None, dir=None)
