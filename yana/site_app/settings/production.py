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

# Allow configuring DEBUG via env; default to False in production
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Hosts and CSRF from env (comma-separated), fallback to existing defaults
_default_allowed_hosts = [
    '35.194.60.34',
    'localhost',
    '127.0.0.1',
    '10.128.0.2',
    '34.8.224.201',
    'youare-notalone.duckdns.org',
    '34.95.113.90'
]
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', ','.join(_default_allowed_hosts)).split(',') if h.strip()]

_default_csrf_trusted = [
    'http://34.8.224.201',
    'http://localhost:5173',
    'http://127.0.0.1:8000',
]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', ','.join(_default_csrf_trusted)).split(',') if o.strip()]

# CORS settings (override base.py)
_default_cors_origins = [
    'http://localhost:5173',
    'https://yana-front.vercel.app',
]
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', ','.join(_default_cors_origins)).split(',') if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# Optional FRONTEND_URL override via env
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

SECURE_REDIRECT_EXEMPT = ['/health']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL', '')

# Parse the database URL
db_url = urlparse(DATABASE_URL) if DATABASE_URL else urlparse('')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_url.path[1:] if db_url.path else None,  # Remove leading slash
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
logger.info(
    f"Database configuration: host={DATABASES['default']['HOST']}, "
    f"port={DATABASES['default']['PORT']}, name={DATABASES['default']['NAME']}, "
    f"user={DATABASES['default']['USER']}"
)