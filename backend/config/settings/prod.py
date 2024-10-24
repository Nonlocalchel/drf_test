from .base import *
from .simple_jwt_config import SIMPLE_JWT
from .swagger_config import SWAGGER_SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'database',
        'PORT': 5432
    }
}