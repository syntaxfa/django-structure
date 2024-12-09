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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
