from django.db import models
from django.conf import settings
from .fields import EncryptedFloatField

    
class Emotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SharedEmotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    latitude = EncryptedFloatField()
    longitude = EncryptedFloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)