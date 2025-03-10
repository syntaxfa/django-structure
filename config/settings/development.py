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
