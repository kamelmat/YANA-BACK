from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Emotion
        fields = ['id', 'name', 'image']



