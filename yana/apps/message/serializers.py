from rest_framework import serializers
from .models import *
from apps.emotions.models import SharedEmotion

class SendSupportMessageSerializer(serializers.Serializer):
    shared_emotion = serializers.PrimaryKeyRelatedField(queryset=SharedEmotion.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=SupportMessageTemplate.objects.all())

class SupportMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['template', 'created_at']