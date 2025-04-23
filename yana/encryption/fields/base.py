from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken
from django.db import models
from django.core.exceptions import ImproperlyConfigured, ValidationError
import logging

logger = logging.getLogger(__name__)


class EncryptedField(models.TextField):
    def __init__(self, *args, **kwargs):
        if not hasattr(settings, 'FIELD_ENCRYPTION_KEY'):
            raise ImproperlyConfigured("FIELD_ENCRYPTION_KEY must be set in settings")
        try:
            self.cipher = Fernet(settings.FIELD_ENCRYPTION_KEY)
        except Exception as e:
            logger.error(f"Fernet init failed: {e}")
            raise
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if value is None or isinstance(value, str):
            return value
        try:
            decrypted = self.cipher.decrypt(value.encode()).decode()
            return decrypted
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValidationError("Invalid encrypted value")

    def get_prep_value(self, value):
        if value is None:
            return None
        try:
            value_str = str(value)
            encrypted = self.cipher.encrypt(value_str.encode()).decode()
            return encrypted
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise ValidationError("Could not encrypt value")
