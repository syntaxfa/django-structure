# pylint: disable=wildcard-import, missing-module-docstring, unused-wildcard-import, duplicate-code, import-error
import os

from dotenv import load_dotenv
from .base import *

load_dotenv()

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

# DATABASES
# ------------------------------------------------------------------------------
DB_NAME = os.getenv('POSTGRES_DB_NAME')
DB_USER = os.getenv('POSTGRES_USERNAME')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST_DEBUG')
DB_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_CONN_MAX_AGE = int(os.getenv('POSTGRES_CONN_MAX_AGE'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': POSTGRES_CONN_MAX_AGE,
    }
}

# DATABASES["default"]["ATOMIC_REQUESTS"] = True

# APPS
# ------------------------------------------------------------------------------
APPS = [
    "debug_toolbar"
]
INSTALLED_APPS += APPS

# HOSTS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# MIDDLEWARE
# ------------------------------------------------------------------------------
insert_middleware(MIDDLEWARE, "debug_toolbar.middleware.DebugToolbarMiddleware", 2)

# DJANGO DEBUG
# ------------------------------------------------------------------------------
INTERNAL_IPS = [
    "127.0.0.1",
]

# CACHE
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST_DEBUG')}:{os.getenv('REDIS_PORT')}/1",
        'OPTIONS': {
            'PASSWORD': os.getenv('REDIS_PASSWORD'),
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# CELERY
CELERY_BROKER_URL = (f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST_DEBUG')}"
                     f":{os.getenv('REDIS_PORT')}/0")
CELERY_PREFETCH_MULTIPLIER = int(os.getenv("CELERY_PREFETCH_MULTIPLIER"))
