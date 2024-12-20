from .base import *
from .simple_jwt_config import SIMPLE_JWT
from .swagger_config import SWAGGER_SETTINGS
from .cors_headers import CORS_ALLOWED_ORIGINS, CORS_ALLOWED_ORIGIN_REGEXES, CORS_ALLOW_METHODS

LOGGING = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': '',
        'PORT': 5432,
        'CONN_MAX_AGE': 60
    }
}
