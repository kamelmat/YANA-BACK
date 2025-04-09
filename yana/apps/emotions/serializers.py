from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class SharedEmotionSerializer(serializers.ModelSerializer):
    emotion = serializers.CharField(source='emotion.name', read_only=True)
    emotion_id = serializers.PrimaryKeyRelatedField(queryset=Emotion.objects.all(), write_only=True, source='emotion')

    class Meta:
        model = SharedEmotion
        fields = ['emotion', 'emotion_id', "latitude", "longitude", "created_at", "is_active"]