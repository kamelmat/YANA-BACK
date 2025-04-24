from django.db import models
from django.core.exceptions import ValidationError
from .utils import get_crypter
from cryptography.fernet import InvalidToken
import logging

logger = logging.getLogger(__name__)

class EncryptedTextField(models.TextField):
    """
    Custom field to encrypt and decrypt string values using Fernet.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return get_crypter().decrypt(value.encode()).decode()
        except InvalidToken:
            logger.error("Invalid encryption token while decrypting from DB: %s", value)
        except Exception as e:
            logger.exception("Unexpected error during from_db_value: %s", e)
        return None

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                # If the value is already encrypted, try to decrypt it
                return get_crypter().decrypt(value.encode()).decode()
            except (InvalidToken, ValueError, TypeError):
                # If decryption fails, assume it's a plain string
                return value
            except Exception as e:
                logger.exception("Unexpected error in to_python: %s", e)
                return value
        return str(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        try:
            # Convert to string and encode before encryption
            value_str = str(value)
            encrypted = get_crypter().encrypt(value_str.encode()).decode()
            return encrypted
        except Exception as e:
            logger.exception("Error encrypting string value %s: %s", value, e)
            raise ValueError("Could not encrypt value")

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return self.get_prep_value(value)

    def get_internal_type(self):
        return 'TextField'

    def get_db_prep_save(self, value, connection):
        return self.get_db_prep_value(value, connection)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

class EncryptedFloatField(models.TextField):
    """
    Campo personalizado para cifrar y descifrar valores float usando Fernet.
    Incluye manejo detallado de errores.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            decrypted = get_crypter().decrypt(value.encode()).decode()
            return float(decrypted)
        except InvalidToken:
            logger.error("Invalid encryption token while decrypting from DB: %s", value)
        except (ValueError, TypeError) as e:
            logger.error("Error converting decrypted value to float: %s (%s)", value, e)
        except Exception as e:
            logger.exception("Unexpected error during from_db_value: %s", e)
        return None

    def clean(self, value, model_instance):
        if value is None:
            return value
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Could not convert {value} to float")

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, float):
            return value
            
        # First try to convert to float to validate the input
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            # If it's not a valid float, try to decrypt it
            try:
                decrypted = get_crypter().decrypt(value.encode()).decode()
                return float(decrypted)
            except (InvalidToken, ValueError, TypeError):
                # If both conversion and decryption fail, raise ValueError
                raise ValueError(f"Could not convert {value} to float")
            except Exception as e:
                logger.exception("Unexpected error in to_python: %s", e)
                raise ValueError(f"Could not convert {value} to float")
                
        return float_value

    def get_prep_value(self, value):
        if value is None:
            return None
        try:
            # Convert to string and encode before encryption
            value_str = str(value)
            encrypted = get_crypter().encrypt(value_str.encode()).decode()
            return encrypted
        except Exception as e:
            logger.exception("Error encrypting float value %s: %s", value, e)
            raise ValueError("Could not encrypt value")

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return self.get_prep_value(value)
