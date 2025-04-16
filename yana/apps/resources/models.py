from django.db import models


class HelpResource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
