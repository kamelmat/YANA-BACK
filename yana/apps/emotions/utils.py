from django.conf import settings
from cryptography.fernet import Fernet

def get_crypter():
    return Fernet(settings.FIELD_ENCRYPTION_KEY.encode())