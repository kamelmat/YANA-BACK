from django.db import models
from django.conf import settings

    
class Emotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return  f"{self.name}"

