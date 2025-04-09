from .base import *
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=BASE_DIR / ".env")

# Use PostgreSQL for testing with a test-specific database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME") + '_test',  # Append _test to create a test database
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'TEST': {
            'NAME': os.getenv("DB_NAME") + '_test',
        },
    }
}

# Other test-specific settings
DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend' 