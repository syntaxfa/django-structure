# pylint: disable=wildcard-import, missing-module-docstring, unused-wildcard-import, duplicate-code, import-error
from .base import *

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES["default"]["ATOMIC_REQUESTS"] = True

# APPS
# ------------------------------------------------------------------------------
APPS = [
]
INSTALLED_APPS += APPS

# HOSTS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# MIDDLEWARE
# ------------------------------------------------------------------------------

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
