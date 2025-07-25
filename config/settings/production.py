# pylint: disable=wildcard-import, missing-module-docstring, unused-wildcard-import, duplicate-code, import-error
import os

from dotenv import load_dotenv
from corsheaders.defaults import default_headers, default_methods
from config.settings.base import *

load_dotenv()

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

# APPS
# ------------------------------------------------------------------------------
APPS = [
]
INSTALLED_APPS += APPS

# DATABASES
# ------------------------------------------------------------------------------
DB_NAME = os.getenv('POSTGRES_DB_NAME')
DB_USER = os.getenv('POSTGRES_USERNAME')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
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

# HOSTS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS] + [f"http://{host}" for host in ALLOWED_HOSTS]

# CORS
# ------------------------------------------------------------------------------
CORS_ALLOW_METHODS = (
    *default_methods,
)

CORS_ALLOW_HEADERS = (
    *default_headers,
    # "my-custom-header",
)

# TODO - change it when production ready!!!
CORS_ORIGIN_ALLOW_ALL = True

# MIDDLEWARE
# ------------------------------------------------------------------------------
insert_middleware(MIDDLEWARE, "corsheaders.middleware.CorsMiddleware", 2)

# CACHE
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",
        'OPTIONS': {
            'PASSWORD': os.getenv('REDIS_PASSWORD'),
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# CELERY
CELERY_BROKER_URL = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"
CELERY_PREFETCH_MULTIPLIER = int(os.getenv("CELERY_PREFETCH_MULTIPLIER"))
