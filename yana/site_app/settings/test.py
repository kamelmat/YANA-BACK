from .base import *
from datetime import timedelta

# Security settings for testing
SECRET_KEY = 'django-insecure-test-key-for-testing-only'

# Database settings for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Test-specific settings
DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# JWT settings for testing
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
}

# Use the same encryption key as in base settings
FIELD_ENCRYPTION_KEY = "p9kZ1JXx9fqCRxFbKz6vgf3acQeQWpzqd7TWzr5r7JU=" 