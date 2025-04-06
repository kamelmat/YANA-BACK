from django.db import models
from django.conf import settings


    
class Emotion(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return  "f{self.name} {self.image}"
    
