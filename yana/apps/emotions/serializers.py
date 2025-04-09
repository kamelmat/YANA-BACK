from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class SharedEmotionSerializer(serializers.ModelSerializer):
    emotion_name = serializers.CharField(source='emotion.name', read_only=True)

    class Meta:
        model = SharedEmotion
        fields = ['id', 'emotion', "latitude", "longitude", "created_at", "is_active"]