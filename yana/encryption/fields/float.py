from .base import EncryptedField

class EncryptedSafeFloatField(EncryptedField):
    def to_python(self, value):
        if isinstance(value, float):
            return value
        try:
            decrypted = super().to_python(value)
            return float(decrypted)
        except Exception:
            return None

    def get_prep_value(self, value):
        if value is None:
            return None
        return super().get_prep_value(str(float(value)))
