from .base import *
import os
from pathlib import Path

# Development settings
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')

ALLOWED_HOSTS = ['*']

# File-based SQLite DB at project root
SQLITE_DB_PATH = (Path(__file__).resolve().parent.parent.parent / 'db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(SQLITE_DB_PATH),
    }
} 