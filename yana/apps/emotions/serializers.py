from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class UserEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmotion
        fields = ['id', 'emotion', 'timestamp']