from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from cryptography.fernet import Fernet, InvalidToken
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class EncryptedFloatField(models.Field):
    description = "A field that encrypts a float value"

    def __init__(self, *args, **kwargs):
        if not hasattr(settings, 'FIELD_ENCRYPTION_KEY'):
            raise ImproperlyConfigured(
                "FIELD_ENCRYPTION_KEY must be set in settings to use EncryptedFloatField"
            )
        
        try:
            self.cipher = Fernet(settings.FIELD_ENCRYPTION_KEY.encode())
        except Exception as e:
            logger.error(f"Failed to initialize Fernet cipher: {str(e)}")
            raise
        
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        
        try:
            decrypted = self.cipher.decrypt(value.encode()).decode()
            return float(decrypted)
        except InvalidToken:
            logger.error("Invalid token when decrypting value")
            return None
        except ValueError as e:
            logger.error(f"Decryption failed: {str(e)}")
            return None

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, float):
            return value
        if isinstance(value, int):
            return float(value)
        
        try:
            decrypted = self.cipher.decrypt(value.encode()).decode()
            return float(decrypted)
        except (InvalidToken, ValueError) as e:
            logger.error(f"Conversion to Python failed: {str(e)}")
            raise ValidationError("Invalid encrypted value")

    def get_prep_value(self, value):
        if value is None:
            return value
        
        try:
            encrypted = self.cipher.encrypt(str(float(value)).encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Value preparation failed: {str(e)}")
            raise ValidationError("Value could not be encrypted")

    def get_db_prep_value(self, value, connection, prepared=False):
        return self.get_prep_value(value)