from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Emotion
        fields = ['id', 'name', 'icon_url']

    def get_icon_url(self, obj):
        return f"/media/emotions/{obj.name}.svg"

class UserEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmotion
        fields = ['id', 'emotion', 'timestamp']