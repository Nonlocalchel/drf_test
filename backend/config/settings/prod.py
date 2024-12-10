from .base import *
from .simple_jwt_config import SIMPLE_JWT
from .swagger_config import SWAGGER_SETTINGS

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': 5432,
        'CONN_MAX_AGE': 60
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': "django_redis.cache.RedisCache",
#         'LOCATION': os.getenv('REDIS_URL'),
#         "OPTIONS": {
#             "PASSWORD": os.getenv('REDIS_PASSWORD'),
#         }
#     }
# }

INSTALLED_APPS += [
    'cachalot'
]
