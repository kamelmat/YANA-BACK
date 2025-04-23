from django.db import models
from django.conf import settings
from encryption.fields.float import EncryptedSafeFloatField  # custom encrypted float field

class Emotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SharedEmotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    latitude = EncryptedSafeFloatField()
    longitude = EncryptedSafeFloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.emotion.name} at ({self.latitude}, {self.longitude})"