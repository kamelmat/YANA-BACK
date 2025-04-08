from django.db import models
from django.conf import settings

    
class Emotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class UserEmotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
