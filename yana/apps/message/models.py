from django.db import models
from django.conf import settings

class SupportMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.CharField(
        max_length=100,
        default="You are not alone, I’m here, I feel you",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
