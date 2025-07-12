# pylint: disable=wildcard-import, missing-module-docstring, duplicate-code, import-error
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

from django.utils.translation import gettext_lazy as _

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECURITY_KEY")

# GENERAL
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LOCALE_PATH = [BASE_DIR / "locale"]
LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Persian')),
)

# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
    'django_celery_beat',
]

LOCAL_APPS = [
    "apps.api.apps.ApiConfig",
    "apps.common.apps.CommonConfig",
    # "apps.authentication.apps.AuthenticationConfig"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# STATIC
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# MIDDLEWARES
# ------------------------------------------------------------------------------
BASE_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


def insert_middleware(middleware_list, middleware_to_add, position):
    middleware_list.insert(position, middleware_to_add)
    return middleware_list


MIDDLEWARE = BASE_MIDDLEWARE.copy()

# DRF
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SWAGGER
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'SYNTAX-FA API',
    'DESCRIPTION': 'syntax fa apis',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # OTHER SETTINGS
    'PLUGINS': [
        'drf_spectacular.plugins.AuthPlugin',
    ],
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
    # Auth with session only in docs without effect to api
    'SERVE_AUTHENTICATION': ["rest_framework.authentication.SessionAuthentication",
                             "rest_framework_simplejwt.authentication.JWTAuthentication"],
}

# PROJECT ADMIN EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_VERIFICATION_URL_TIMEOUT = 60 * 3  # seconds
EMAIL_USE_SSL = True

# Accounts config
# ------------------------------------------------------------------------------
# AUTH_USER_MODEL = "accounts.User"
SITE_ID = 1

# JWT
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60)
}

# LOGGER
LOGGER_NAME = os.getenv("LOGGER_NAME")
