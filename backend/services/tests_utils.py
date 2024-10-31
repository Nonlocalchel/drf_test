import tempfile


def get_temp_file():
    """Create fake temp file for media for in tests"""
    return tempfile.mkdtemp(suffix=None, prefix=None, dir=None)
