from django.db import models
from .utils import get_crypter
from cryptography.fernet import InvalidToken
import logging

logger = logging.getLogger(__name__)

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

    def to_python(self, value):
        if value is None or isinstance(value, float):
            return value
        try:
            decrypted = get_crypter().decrypt(value.encode()).decode()
            return float(decrypted)
        except InvalidToken:
            logger.warning("Invalid encryption token in to_python: %s", value)
        except (ValueError, TypeError) as e:
            logger.warning("Error converting to float in to_python: %s (%s)", value, e)
        except Exception as e:
            logger.exception("Unexpected error in to_python: %s", e)
        return float(value)  # Asume que el valor ya es un número legible

    def get_prep_value(self, value):
        if value is None:
            return value
        try:
            encrypted = get_crypter().encrypt(str(value).encode()).decode()
            return encrypted
        except Exception as e:
            logger.exception("Error encrypting float value %s: %s", value, e)
            raise ValueError("Could not encrypt value")
