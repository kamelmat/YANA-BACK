from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

#emociones que agrega el usuario:
class UserEmotionSerializer(serializers.ModelSerializer):
    emotion_name = serializers.CharField(source='emotion.name', read_only=True)

    class Meta:
        model = UserEmotion
        fields = ['id', 'emotion', 'timestamp', 'emotion_name']

