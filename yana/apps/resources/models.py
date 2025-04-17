from django.db import models



class HelpResource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
