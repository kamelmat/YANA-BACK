from .base import *
from dotenv import load_dotenv
import os
from pathlib import Path
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Llega hasta yana/
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    '35.194.60.34'
]

CSRF_TRUSTED_ORIGINS = [
    'http://35.194.60.34',
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Parse the database URL
db_url = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_url.path[1:],  # Remove leading slash
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.hostname,
        'PORT': db_url.port,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Log database configuration (without password)
logger.info(f"Database configuration: host={DATABASES['default']['HOST']}, port={DATABASES['default']['PORT']}, name={DATABASES['default']['NAME']}, user={DATABASES['default']['USER']}")