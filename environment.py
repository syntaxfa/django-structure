# environment.py
import os
from dotenv import load_dotenv

load_dotenv()


match os.getenv("DJANGO_ENV"):
    case "production":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    case "test":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
    case _:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
