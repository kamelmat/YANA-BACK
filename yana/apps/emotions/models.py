from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .fields import EncryptedTextField

    
class Emotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SharedEmotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    latitude = EncryptedTextField()
    longitude = EncryptedTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        # Basic validation to ensure values are not empty
        if not self.latitude:
            raise ValidationError({'latitude': 'Latitude cannot be empty'})
        if not self.longitude:
            raise ValidationError({'longitude': 'Longitude cannot be empty'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)