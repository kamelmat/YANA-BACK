from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class UserEmotionListSerializer(serializers.ModelSerializer):
    emotion = serializers.StringRelatedField()
    class Meta:
        model = UserEmotion
        fields = ['id', 'emotion', 'timestamp']

