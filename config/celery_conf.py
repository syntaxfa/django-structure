# pylint: skip-file
import os
from datetime import timedelta

from django.conf import settings
from celery import Celery
from dotenv import load_dotenv

load_dotenv()


match os.getenv("DJANGO_ENV"):
    case "production":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    case _:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

celery_app = Celery('A')
celery_app.autodiscover_tasks()

broker_url = getattr(settings, "CELERY_BROKER_URL")
celery_app.conf.broker_url = broker_url

celery_app.conf.result_backend = broker_url
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_expires = timedelta(hours=12)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = int(getattr(settings, "CELERY_PREFETCH_MULTIPLIER", 12))
